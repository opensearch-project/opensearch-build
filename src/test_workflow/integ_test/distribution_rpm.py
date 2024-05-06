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
        self.require_sudo = True

    @property
    def install_dir(self) -> str:
        return os.path.join(os.sep, "usr", "share", self.filename)

    @property
    def config_path(self) -> str:
        return os.path.join(os.sep, "etc", self.filename, self.config_filename)

    @property
    def log_dir(self) -> str:
        return os.path.join(os.sep, "var", "log", self.filename)

    def install(self, bundle_name: str) -> None:
        logging.info(f"Installing {bundle_name} in {self.install_dir}")
        logging.info("rpm installation requires sudo, script will exit if current user does not have sudo access")
        rpm_install_cmd = " ".join(
            [
                'sudo',
                'yum',
                'remove',
                '-y',
                self.filename,
                '&&',
                'sudo',
                'env',
                'OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123!',
                'yum',
                'install',
                '-y',
                bundle_name,
                '&&',
                f'sudo chmod 0666 {self.config_path} {os.path.dirname(self.config_path)}/jvm.options',
                '&&',
                f'sudo chmod 0755 {os.path.dirname(self.config_path)} {self.log_dir}',
                '&&',
                f'sudo usermod -a -G {self.filename} `whoami`',
                '&&',
                'sudo usermod -a -G adm `whoami`'
            ]
        )
        subprocess.check_call(rpm_install_cmd, cwd=self.work_dir, shell=True)

    @property
    def start_cmd(self) -> str:
        return f"sudo systemctl start {self.filename}"

    def uninstall(self) -> None:
        logging.info(f"Uninstall {self.filename} package after the test")
        subprocess.check_call(f"sudo yum remove -y {self.filename} && sudo rm -rf {os.path.dirname(self.config_path)} {self.log_dir}", shell=True)
