# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from test_workflow.integ_test.distribution_deb import DistributionDeb


class TestDistributionDeb(unittest.TestCase):
    def setUp(self) -> None:
        self.work_dir = os.path.join(os.path.dirname(__file__), "data")
        self.distribution_deb = DistributionDeb("opensearch", "1.3.0", self.work_dir)
        self.distribution_deb_dashboards = DistributionDeb("opensearch-dashboards", "1.3.0", self.work_dir)

    def test_distribution_deb_vars(self) -> None:
        self.assertEqual(self.distribution_deb.filename, "opensearch")
        self.assertEqual(self.distribution_deb.version, "1.3.0")
        self.assertEqual(self.distribution_deb.work_dir, self.work_dir)
        self.assertEqual(self.distribution_deb.require_sudo, True)

    def test_install_dir(self) -> None:
        self.assertEqual(self.distribution_deb.install_dir, os.path.join(os.sep, "usr", "share", "opensearch"))
        self.assertEqual(self.distribution_deb_dashboards.install_dir, os.path.join(os.sep, "usr", "share", "opensearch-dashboards"))

    def test_config_path(self) -> None:
        self.assertEqual(self.distribution_deb.config_path, os.path.join(os.sep, "etc", "opensearch", "opensearch.yml"))
        self.assertEqual(self.distribution_deb_dashboards.config_path, os.path.join(os.sep, "etc", "opensearch-dashboards", "opensearch_dashboards.yml"))

    def test_data_dir(self) -> None:
        self.assertEqual(self.distribution_deb.data_dir, os.path.join(os.sep, "var", "lib", "opensearch"))
        self.assertEqual(self.distribution_deb_dashboards.data_dir, os.path.join(os.sep, "var", "lib", "opensearch-dashboards"))

    def test_log_dir(self) -> None:
        self.assertEqual(self.distribution_deb.log_dir, os.path.join(os.sep, "var", "log", "opensearch"))
        self.assertEqual(self.distribution_deb_dashboards.log_dir, os.path.join(os.sep, "var", "log", "opensearch-dashboards"))

    @patch("subprocess.check_call")
    def test_install(self, check_call_mock: Mock) -> None:
        self.distribution_deb.install("opensearch.deb")
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(
            (
                "sudo dpkg --purge opensearch && "
                f"sudo rm -rf {os.path.dirname(self.distribution_deb.config_path)} {self.distribution_deb.data_dir} {self.distribution_deb.log_dir} && "
                "sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123! "
                "dpkg --install opensearch.deb && "
                f"sudo chmod 0666 {self.distribution_deb.config_path} {os.path.dirname(self.distribution_deb.config_path)}/jvm.options && "
                f"sudo chmod 0755 {os.path.dirname(self.distribution_deb.config_path)} {self.distribution_deb.log_dir} && "
                f"sudo usermod -a -G opensearch `whoami` && "
                f"sudo usermod -a -G adm `whoami`"
            ),
            args_list[0][0][0],
        )

    @patch("subprocess.check_call")
    def test_install_opensearch_dashboards(self, check_call_mock: Mock) -> None:
        self.distribution_deb_dashboards.install("opensearch-dashboards.deb")
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(
            (
                "sudo dpkg --purge opensearch-dashboards && "
                f"sudo rm -rf {os.path.dirname(self.distribution_deb_dashboards.config_path)} {self.distribution_deb_dashboards.data_dir} {self.distribution_deb_dashboards.log_dir} && "
                "sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123! "
                "dpkg --install opensearch-dashboards.deb && "
                f"sudo chmod 0666 {self.distribution_deb_dashboards.config_path} && "
                f"sudo chmod 0755 {os.path.dirname(self.distribution_deb_dashboards.config_path)} {self.distribution_deb_dashboards.log_dir} && "
                f"sudo usermod -a -G opensearch-dashboards `whoami` && "
                f"sudo usermod -a -G adm `whoami`"
            ),
            args_list[0][0][0],
        )

    def test_start_cmd(self) -> None:
        self.assertEqual(self.distribution_deb.start_cmd, "sudo systemctl start opensearch")
        self.assertEqual(self.distribution_deb_dashboards.start_cmd, "sudo systemctl start opensearch-dashboards")

    @patch("subprocess.check_call")
    def test_uninstall(self, check_call_mock: Mock) -> None:
        self.distribution_deb.uninstall()
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(
            (
                "sudo dpkg --purge opensearch && "
                f"sudo rm -rf {os.path.dirname(self.distribution_deb.config_path)} {self.distribution_deb.data_dir} {self.distribution_deb.log_dir}"
            ),
            args_list[0][0][0],
        )
