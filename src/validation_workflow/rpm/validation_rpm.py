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
