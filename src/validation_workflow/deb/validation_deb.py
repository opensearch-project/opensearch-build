# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from system.execute import execute
from test_workflow.integ_test.utils import get_password
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateDeb(Validation, DownloadUtils):
    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)

    def installation(self) -> bool:
        try:
            for project in self.args.projects:
                set_password = f' env OPENSEARCH_INITIAL_ADMIN_PASSWORD={get_password(str(self.args.version))}' if project == "opensearch" else ""
                execute(f'sudo dpkg --purge {project}', ".")
                execute(f'sudo {set_password} dpkg -i {os.path.basename(self.args.file_path.get(project))}', str(self.tmp_dir.path))
        except:
            raise Exception("Failed to install OpenSearch/OpenSearch-Dashboards")
        return True

    def start_cluster(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl enable {project}', ".")
                execute(f'sudo systemctl start {project}', ".")
                execute(f'sudo systemctl status {project}', ".")
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
                raise Exception(f'Not all tests Pass : {counter}')
        else:
            raise Exception("Cluster is not ready for API test")

    def cleanup(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo dpkg --purge {project}', ".")
        except Exception as e:
            raise Exception(f'Exception occurred either while attempting to stop cluster or removing OpenSearch/OpenSearch-Dashboards. {str(e)}')
        return True
