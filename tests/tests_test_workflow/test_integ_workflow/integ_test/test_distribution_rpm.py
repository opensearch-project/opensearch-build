# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from test_workflow.integ_test.distribution_rpm import DistributionRpm


class TestDistributionRpm(unittest.TestCase):
    def setUp(self) -> None:
        self.work_dir = os.path.join(os.path.dirname(__file__), "data")
        self.distribution_rpm = DistributionRpm("opensearch", "1.3.0", self.work_dir)
        self.distribution_rpm_dashboards = DistributionRpm("opensearch-dashboards", "1.3.0", self.work_dir)

    def test_distribution_rpm_vars(self) -> None:
        self.assertEqual(self.distribution_rpm.filename, "opensearch")
        self.assertEqual(self.distribution_rpm.version, "1.3.0")
        self.assertEqual(self.distribution_rpm.work_dir, self.work_dir)
        self.assertEqual(self.distribution_rpm.require_sudo, True)

    def test_install_dir(self) -> None:
        self.assertEqual(self.distribution_rpm.install_dir, os.path.join(os.sep, "usr", "share", "opensearch"))
        self.assertEqual(self.distribution_rpm_dashboards.install_dir, os.path.join(os.sep, "usr", "share", "opensearch-dashboards"))

    def test_config_path(self) -> None:
        self.assertEqual(self.distribution_rpm.config_path, os.path.join(os.sep, "etc", "opensearch", "opensearch.yml"))
        self.assertEqual(self.distribution_rpm_dashboards.config_path, os.path.join(os.sep, "etc", "opensearch-dashboards", "opensearch_dashboards.yml"))

    def test_data_dir(self) -> None:
        self.assertEqual(self.distribution_rpm.data_dir, os.path.join(os.sep, "var", "lib", "opensearch"))
        self.assertEqual(self.distribution_rpm_dashboards.data_dir, os.path.join(os.sep, "var", "lib", "opensearch-dashboards"))

    def test_log_dir(self) -> None:
        self.assertEqual(self.distribution_rpm.log_dir, os.path.join(os.sep, "var", "log", "opensearch"))
        self.assertEqual(self.distribution_rpm_dashboards.log_dir, os.path.join(os.sep, "var", "log", "opensearch-dashboards"))

    @patch("subprocess.check_call")
    def test_install(self, check_call_mock: Mock) -> None:
        self.distribution_rpm.install("opensearch.rpm")
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(
            (
                "sudo yum remove -y opensearch && "
                f"sudo rm -rf {os.path.dirname(self.distribution_rpm.config_path)} {self.distribution_rpm.data_dir} {self.distribution_rpm.log_dir} && "
                "sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123! "
                "yum install -y opensearch.rpm && "
                f"sudo chmod 0666 {self.distribution_rpm.config_path} {os.path.dirname(self.distribution_rpm.config_path)}/jvm.options && "
                f"sudo chmod 0755 {os.path.dirname(self.distribution_rpm.config_path)} {self.distribution_rpm.log_dir} && "
                f"sudo usermod -a -G opensearch `whoami` && "
                f"sudo usermod -a -G adm `whoami`"
            ),
            args_list[0][0][0],
        )

    @patch("subprocess.check_call")
    def test_install_opensearch_dashboards(self, check_call_mock: Mock) -> None:
        self.distribution_rpm_dashboards.install("opensearch-dashboards.rpm")
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(
            (
                "sudo yum remove -y opensearch-dashboards && "
                f"sudo rm -rf {os.path.dirname(self.distribution_rpm_dashboards.config_path)} {self.distribution_rpm_dashboards.data_dir} {self.distribution_rpm_dashboards.log_dir} && "
                "sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123! "
                "yum install -y opensearch-dashboards.rpm && "
                f"sudo chmod 0666 {self.distribution_rpm_dashboards.config_path} && "
                f"sudo chmod 0755 {os.path.dirname(self.distribution_rpm_dashboards.config_path)} {self.distribution_rpm_dashboards.log_dir} && "
                f"sudo usermod -a -G opensearch-dashboards `whoami` && "
                f"sudo usermod -a -G adm `whoami`"
            ),
            args_list[0][0][0],
        )

    def test_start_cmd(self) -> None:
        self.assertEqual(self.distribution_rpm.start_cmd, "sudo systemctl start opensearch")
        self.assertEqual(self.distribution_rpm_dashboards.start_cmd, "sudo systemctl start opensearch-dashboards")

    @patch("subprocess.check_call")
    def test_uninstall(self, check_call_mock: Mock) -> None:
        self.distribution_rpm.uninstall()
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(
            (
                "sudo yum remove -y opensearch && "
                f"sudo rm -rf {os.path.dirname(self.distribution_rpm.config_path)} {self.distribution_rpm.data_dir} {self.distribution_rpm.log_dir}"
            ),
            args_list[0][0][0],
        )
