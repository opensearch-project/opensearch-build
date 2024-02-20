# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from system.execute import execute
from system.process import Process
from test_workflow.integ_test.utils import get_password
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateTar(Validation, DownloadUtils):

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)
        self.os_process = Process()
        self.osd_process = Process()

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
            self.os_process.start(f'export OPENSEARCH_INITIAL_ADMIN_PASSWORD={get_password(str(self.args.version))} && ./opensearch-tar-install.sh', os.path.join(self.tmp_dir.path, "opensearch"))
            if ("opensearch-dashboards" in self.args.projects):
                self.osd_process.start(os.path.join(str(self.tmp_dir.path), "opensearch-dashboards", "bin", "opensearch-dashboards"), ".")
            logging.info('Started cluster')
        except:
            raise Exception('Failed to Start Cluster')
        return True

    def validation(self) -> bool:
        if self.check_cluster_readiness():
            test_result, counter = ApiTestCases().test_apis(self.args.version, self.args.projects,
                                                            self.check_for_security_plugin(os.path.join(self.tmp_dir.path, "opensearch")) if self.args.allow_http else True)
            if (test_result):
                logging.info(f'All tests Pass : {counter}')
                return True
            else:
                raise Exception(f'Not all tests Pass : {counter}')
        else:
            raise Exception("Cluster is not ready for API test")

    def cleanup(self) -> bool:
        try:
            self.os_process.terminate()
            if ("opensearch-dashboards" in self.args.projects):
                self.osd_process.terminate()
        except:
            raise Exception('Failed to terminate the processes that started OpenSearch and OpenSearch-Dashboards')
        return True
