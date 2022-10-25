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
        self.assertEqual(self.distribution_rpm.filename, 'opensearch')
        self.assertEqual(self.distribution_rpm.version, '1.3.0')
        self.assertEqual(self.distribution_rpm.work_dir, self.work_dir)

    def test_install_dir(self) -> None:
        self.assertEqual(self.distribution_rpm.install_dir, os.path.join(os.sep, "usr", "share", "opensearch"))

    def test_config_dir(self) -> None:
        self.assertEqual(self.distribution_rpm.config_dir, os.path.join(os.sep, "etc", "opensearch"))

    @patch("subprocess.check_call")
    def test_install(self, check_call_mock: Mock) -> None:
        self.distribution_rpm.install("opensearch.rpm")
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual("yum remove -y opensearch && yum install -y opensearch.rpm", args_list[0][0][0])

    def test_start_cmd(self) -> None:
        self.assertEqual(self.distribution_rpm.start_cmd, "systemctl start opensearch")
        self.assertEqual(self.distribution_rpm_dashboards.start_cmd, "systemctl start opensearch-dashboards")

    @patch("subprocess.check_call")
    def test_uninstall(self, check_call_mock: Mock) -> None:
        self.distribution_rpm.uninstall()
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual("yum remove -y opensearch", args_list[0][0][0])
