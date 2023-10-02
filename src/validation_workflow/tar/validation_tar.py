# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import time

from system.execute import execute
from system.process import Process
from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateTar(Validation, DownloadUtils):

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)
        self.base_url_production = "https://artifacts.opensearch.org/releases/bundle/"
        self.base_url_staging = "https://ci.opensearch.org/ci/dbc/distribution-build-"
        self.tmp_dir = TemporaryDirectory()
        self.os_process = Process()
        self.osd_process = Process()

    def download_artifacts(self) -> bool:
        isFilePathEmpty = bool(self.args.file_path)
        for project in self.args.projects:
            if (isFilePathEmpty):
                if ("https:" not in self.args.file_path.get(project)):
                    self.copy_artifact(self.args.file_path.get(project), str(self.tmp_dir.path))
                else:
                    self.check_url(self.args.file_path.get(project))
            else:
                if (self.args.artifact_type == "staging"):
                    self.args.file_path[project] = f"{self.base_url_staging}{project}/{self.args.version}/{self.args.build_number[project]}/linux/{self.args.arch}/{self.args.distribution}/dist/{project}/{project}-{self.args.version}-linux-{self.args.arch}.tar.gz"  # noqa: E501
                else:
                    self.args.file_path[project] = f"{self.base_url_production}{project}/{self.args.version}/{project}-{self.args.version}-linux-{self.args.arch}.tar.gz"
                self.check_url(self.args.file_path.get(project))
        return True

    def installation(self) -> bool:
        try:
            for project in self.args.projects:
                self.filename = os.path.basename(self.args.file_path.get(project))
                execute('mkdir ' + os.path.join(self.tmp_dir.path, project) + ' | tar -xzf ' + os.path.join(str(self.tmp_dir.path), self.filename) + ' -C ' + os.path.join(self.tmp_dir.path, project) + ' --strip-components=1', ".", True, False)  # noqa: E501
        except:
            raise Exception('Failed to install Opensearch')
        return True

    def start_cluster(self) -> bool:
        try:
            self.os_process.start(os.path.join(self.tmp_dir.path, "opensearch", "opensearch-tar-install.sh"), ".")
            time.sleep(85)
            if ("opensearch-dashboards" in self.args.projects):
                self.osd_process.start(os.path.join(str(self.tmp_dir.path), "opensearch-dashboards", "bin", "opensearch-dashboards"), ".")
                time.sleep(20)
            logging.info('Started cluster')
        except:
            raise Exception('Failed to Start Cluster')
        return True

    def validation(self) -> bool:
        test_result, counter = ApiTestCases().test_apis(self.args.projects)
        if (test_result):
            logging.info(f'All tests Pass : {counter}')
        else:
            raise Exception(f'Not all tests Pass : {counter}')
        return True

    def cleanup(self) -> bool:
        try:
            self.os_process.terminate()
            if ("opensearch-dashboards" in self.args.projects):
                self.osd_process.terminate()
        except:
            raise Exception('Failed to terminate the processes that started OpenSearch and OpenSearch-Dashboards')
        return True
