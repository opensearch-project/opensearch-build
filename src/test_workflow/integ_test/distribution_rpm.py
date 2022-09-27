# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

from test_workflow.integ_test.distribution import Distribution


class DistributionRpm(Distribution):
    def __init__(self, filename: str, version: str, work_dir: str) -> None:
        super().__init__(filename, version, work_dir)

    @property
    def install_dir(self) -> str:
        return os.path.join(os.sep, "usr", "share", self.filename)

    @property
    def config_dir(self) -> str:
        return os.path.join(os.sep, "etc", self.filename)

    def install(self, bundle_name: str) -> None:
        logging.info(f"Installing {bundle_name} in {self.install_dir}")
        logging.info("rpm installation requires sudo, script will exit if current user does not have sudo access")
        rpm_install_cmd = " ".join(
            [
                'yum',
                'remove',
                '-y',
                self.filename,
                '&&',
                'yum',
                'install',
                '-y',
                bundle_name
            ]
        )
        subprocess.check_call(rpm_install_cmd, cwd=self.work_dir, shell=True)

    @property
    def start_cmd(self) -> str:
        return f"systemctl start {self.filename}"

    def uninstall(self) -> None:
        logging.info("Uninstall {self.filename} package after the test")
        subprocess.check_call(f"yum remove -y {self.filename}", shell=True)
