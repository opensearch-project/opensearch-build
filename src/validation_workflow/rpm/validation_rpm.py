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
from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateRpm(Validation, DownloadUtils):

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)
        self.base_url = "https://artifacts.opensearch.org/releases/bundle/"
        self.tmp_dir = TemporaryDirectory()

    def download_artifacts(self) -> bool:
        architectures = ["x64", "arm64"]
        for project in self.args.projects:
            for architecture in architectures:
                url = f"{self.base_url}{project}/{self.args.version}/{project}-{self.args.version}-linux-{architecture}.rpm"
                if ValidateRpm.is_url_valid(url) and ValidateRpm.download(url, self.tmp_dir):
                    logging.info(f"Valid URL - {url} and Download Successful !")
                else:
                    logging.info(f"Invalid URL - {url}")
                    raise Exception(f"Invalid url - {url}")
        return True

    def installation(self) -> bool:
        try:
            execute('sudo rpm --import https://artifacts.opensearch.org/publickeys/opensearch.pgp', str(self.tmp_dir.path), True, False)
            for project in self.args.projects:
                execute(f'sudo yum remove {project} -y', ".")
                path = os.path.join(self.tmp_dir.path, project + "-" + self.args.version + "-linux-" + self.args.arch + ".rpm")
                execute(f'sudo rpm -ivh {path}', str(self.tmp_dir.path), True, False)
        except:
            raise Exception('Failed to install Opensearch')
        return True

    def start_cluster(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl enable {project}', ".")
                execute(f'sudo systemctl start {project}', ".")
                time.sleep(20)
                (stdout, stderr, status) = execute(f'sudo systemctl status {project}', ".")
                if(status == 0):
                    logging.info(stdout)
                else:
                    logging.info(stderr)

        except:
            raise Exception('Failed to Start Cluster')
        return True

    def validation(self) -> bool:
        test_result, counter = ApiTestCases().test_cases()
        if (test_result):
            logging.info(f'All tests Pass : {counter}')
            return True
        else:
            raise Exception(f'Not all tests Pass : {counter}')

    def cleanup(self) -> bool:
        try:
            for project in self.args.projects:
                execute(f'sudo systemctl stop {project}', ".")
        except:
            raise Exception('Failed to Stop Cluster')
        return True
