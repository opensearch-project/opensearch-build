# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import re
import time

from system.execute import execute
from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateYum(Validation, DownloadUtils):

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)
        self.base_url_production = "https://artifacts.opensearch.org/releases/bundle/"
        self.base_url_staging = "https://ci.opensearch.org/ci/dbc/distribution-build-"
        self.tmp_dir = TemporaryDirectory()

    def download_artifacts(self) -> bool:
        isFilePathEmpty = bool(self.args.file_path)
        for project in self.args.projects:
            if (isFilePathEmpty):
                if ("https:" not in self.args.file_path.get(project)):
                    self.copy_artifact(self.args.file_path.get(project), str(self.tmp_dir.path))
                else:
                    self.args.version = re.search(r'(\d+\.\d+\.\d+)', os.path.basename(self.args.file_path.get(project))).group(1)
                    self.check_url(self.args.file_path.get(project))

            else:
                if (self.args.artifact_type == "staging"):
                    self.args.file_path[project] = f"{self.base_url_staging}{project}/{self.args.version}/{self.args.build_number[project]}/linux/{self.args.arch}/rpm/dist/{project}/{project}-{self.args.version}.staging.repo"  # noqa: E501
                else:
                    self.args.file_path[project] = f"{self.base_url_production}{project}/{self.args.version[0:1]}.x/{project}-{self.args.version[0:1]}.x.repo"

                self.check_url(self.args.file_path.get(project))
        return True

    def installation(self) -> bool:
        try:
            execute('sudo rpm --import https://artifacts.opensearch.org/publickeys/opensearch.pgp', str(self.tmp_dir.path), True, False)
            for project in self.args.projects:
                execute(f'sudo yum remove {project} -y', ".")
                logging.info('Removed previous versions of Opensearch')
                urllink = f"{self.args.file_path.get(project)} -o /etc/yum.repos.d/{os.path.basename(self.args.file_path.get(project))}"
                execute(f'sudo curl -SL {urllink}', ".")
                execute(f"sudo yum install '{project}-{self.args.version}' -y", ".")
        except:
            raise Exception('Failed to install Opensearch')
        return True

    def start_cluster(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl start {project}', ".")
                time.sleep(20)
                execute(f'sudo systemctl status {project}', ".")
        except:
            raise Exception('Failed to Start Cluster')
        return True

    def validation(self) -> bool:
        test_result, counter = ApiTestCases().test_apis(self.args.projects)
        if (test_result):
            logging.info(f'All tests Pass : {counter}')
            return True
        else:
            raise Exception(f'Some test cases failed : {counter}')

    def cleanup(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl stop {project}', ".")
                execute(f'sudo yum remove {project} -y', ".")
        except Exception as e:
            raise Exception(f'Exception occurred either while attempting to stop cluster or removing OpenSearch/OpenSearch-Dashboards. {str(e)}')
        return True
