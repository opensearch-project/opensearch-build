# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from system.execute import execute
from system.temporary_directory import TemporaryDirectory
from test_workflow.integ_test.utils import get_password
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateRpm(Validation, DownloadUtils):

    def __init__(self, args: ValidationArgs, tmp_dir: TemporaryDirectory) -> None:
        super().__init__(args, tmp_dir)

    def installation(self) -> bool:
        try:
            execute('sudo rpm --import https://artifacts.opensearch.org/publickeys/opensearch.pgp', str(self.tmp_dir.path), True, False)
            for project in self.args.projects:
                self.filename = os.path.basename(self.args.file_path.get(project))
                self.validate_metadata(project)
                self.validate_signature()
                execute(f'sudo yum remove {project} -y', ".")
                execute(f'sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD={get_password(str(self.args.version))} rpm -ivh {os.path.join(self.tmp_dir.path, self.filename)}', str(self.tmp_dir.path), True, False)  # noqa: 501
        except:
            raise Exception('Failed to install Opensearch')
        return True

    def start_cluster(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl start {project}', ".")
                (stdout, stderr, status) = execute(f'sudo systemctl status {project}', ".")
                if(status == 0):
                    logging.info(stdout)
                else:
                    logging.info(stderr)

        except:
            raise Exception('Failed to Start Cluster')
        return True

    def validation(self) -> bool:
        if self.check_cluster_readiness():
            test_result, counter = ApiTestCases().test_apis(self.args.version, self.args.projects,
                                                            self.check_for_security_plugin(os.path.join(os.sep, "usr", "share", "opensearch")) if self.args.allow_http else True)
            if (test_result):
                logging.info(f'All tests Pass : {counter}')
                return True
            else:
                self.cleanup()
                raise Exception(f'Not all tests Pass : {counter}')
        else:
            raise Exception("Cluster is not ready for API test")

    def cleanup(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl stop {project}', ".")
                execute(f'sudo yum remove {project} -y', ".")
        except Exception as e:
            raise Exception(f'Exception occurred either while attempting to stop cluster or removing OpenSearch/OpenSearch-Dashboards. {str(e)}')
        return True

    def validate_metadata(self, product_type: str) -> None:
        (_, stdout, _) = execute(f'rpm -qip {os.path.join(self.tmp_dir.path, self.filename)}', ".")
        logging.info("Meta data for the RPM distribution is: \n" + stdout)
        ref_map = {}
        ref_map['Name'] = product_type
        ref_map['Version'] = self.args.version
        ref_map['Architecture'] = self.args.arch
        ref_map['Group'] = "Application/Internet"
        ref_map['License'] = "Apache-2.0"
        ref_map['Relocations'] = "(not relocatable)"
        ref_map['URL'] = "https://opensearch.org/"
        # The context the meta data should be based on type OpenSearch or OpenSearchDashBoards
        if product_type == "opensearch":
            ref_map['Summary'] = "An open source distributed and RESTful search engine"
            ref_map[
                'Description'] = "OpenSearch makes it easy to ingest, search, visualize, and analyze your data\nFor more information, see: https://opensearch.org/"
        else:
            ref_map['Summary'] = "Open source visualization dashboards for OpenSearch"
            ref_map[
                'Description'] = "OpenSearch Dashboards is the visualization tool for data in OpenSearch\nFor more information, see: https://opensearch.org/"

        meta_map = {}
        for line in stdout.split('\n'):
            key = line.split(':')[0].strip()
            if key != 'Description':
                meta_map[key] = line.split(':', 1)[1].strip()
            else:
                description_index = stdout.find(line)
                meta_map[key] = stdout[description_index + len(line):].strip()
                break

        for key, value in ref_map.items():
            if key == "Architecture":
                if value == 'x64':
                    assert meta_map.get(key) == 'x86_64'
                elif value == 'arm64':
                    assert meta_map.get(key) == 'aarch64'
            else:
                assert meta_map.get(key) == value
                logging.info(f"Meta data for {key} -> {value} is validated")
        logging.info(f"Validation for {product_type} meta data of RPM distribution completed.")

    def validate_signature(self) -> None:
        (_, stdout, _) = execute(f'rpm -K -v {os.path.join(self.tmp_dir.path, self.filename)}', ".")
        logging.info(stdout)
        key_list = ["Header V4 RSA/SHA512 Signature, key ID 9310d3fc", "Header SHA256 digest", "Header SHA1 digest",
                    "Payload SHA256 digest", "V4 RSA/SHA512 Signature, key ID 9310d3fc", "MD5 digest"]
        present_key = []
        for line in stdout.rstrip('\n').split('\n')[1:]:
            key = line.split(':')[0].strip()
            assert "OK" == line.split(':')[1].strip()
            logging.info(f"{key} is validated as: {line}")
            present_key.append(key)
        logging.info("Validation of all key digests starts: ")
        for digest in key_list:
            assert digest in present_key
            logging.info(f'Key digest "{digest}" is validated to be present.')

        logging.info("Validation for signature of RPM distribution completed.")
