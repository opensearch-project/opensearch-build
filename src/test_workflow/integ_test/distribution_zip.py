# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

from system.zip_file import ZipFile
from test_workflow.integ_test.distribution import Distribution


class DistributionZip(Distribution):
    def __init__(self, filename: str, version: str, work_dir: str) -> None:
        super().__init__(filename, version, work_dir)

    @property
    def install_dir(self) -> str:
        return os.path.join(self.work_dir, f"{self.filename}-{self.version}")

    @property
    def config_dir(self) -> str:
        return os.path.join(self.install_dir, "config")

    def install(self, bundle_name: str) -> None:
        logging.info(f"Installing {bundle_name} in {self.install_dir}")
        with ZipFile(bundle_name, "r") as zip:
            zip.extractall(self.work_dir)

    @property
    def start_cmd(self) -> str:
        start_cmd_map = {
            "opensearch": "./opensearch-windows-install.bat",
            "opensearch-dashboards": "./opensearch-dashboards.bat",
        }
        return start_cmd_map[self.filename]

    def uninstall(self) -> None:
        logging.info(f"Cleanup {self.work_dir}/* content after the test")
        subprocess.check_call(f"rm -rf {self.work_dir}/*", shell=True)
