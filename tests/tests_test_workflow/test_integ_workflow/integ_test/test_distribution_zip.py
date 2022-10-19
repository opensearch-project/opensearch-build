# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

from test_workflow.integ_test.distribution_zip import DistributionZip


class TestDistributionZipOpenSearch(unittest.TestCase):

    def setUp(self) -> None:

        self.work_dir = os.path.join(os.path.dirname(__file__), "data")
        self.product = "opensearch"
        self.version = "2.4.0"
        self.distribution_zip = DistributionZip(self.product, self.version, self.work_dir)

    def test_distribution_zip_vars(self) -> None:
        self.assertEqual(self.distribution_zip.filename, self.product)
        self.assertEqual(self.distribution_zip.version, self.version)
        self.assertEqual(self.distribution_zip.work_dir, self.work_dir)

    def test_install_dir(self) -> None:
        self.assertEqual(self.distribution_zip.install_dir, os.path.join(self.work_dir, f"{self.product}-{self.version}"))

    def test_config_dir(self) -> None:
        self.assertEqual(self.distribution_zip.config_dir, os.path.join(self.work_dir, f"{self.product}-{self.version}", "config"))

    def test_install(self) -> None:
        with patch("test_workflow.integ_test.distribution_zip.ZipFile") as mock_zipfile_open:
            mock_zipfile_extractall = MagicMock()
            mock_zipfile_open.return_value.__enter__.return_value.extractall = mock_zipfile_extractall

            self.distribution_zip.install(os.path.join(self.work_dir, "artifacts", "dist", f"{self.product}-min-{self.version}-windows-x64.zip"))

            mock_zipfile_open.assert_called_with(os.path.join(self.work_dir, "artifacts", "dist", f"{self.product}-min-{self.version}-windows-x64.zip"), "r")
            mock_zipfile_extractall.assert_called_with(self.work_dir)

    def test_start_cmd(self) -> None:
        self.assertEqual(self.distribution_zip.start_cmd, "./opensearch-windows-install.bat")

    @patch("subprocess.check_call")
    def test_uninstall(self, check_call_mock: Mock) -> None:
        self.distribution_zip.uninstall()
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"rm -rf {self.work_dir}/*", args_list[0][0][0])


class TestDistributionZipOpenSearchDashboards(unittest.TestCase):

    def setUp(self) -> None:

        self.work_dir = os.path.join(os.path.dirname(__file__), "data")
        self.product = "opensearch-dashboards"
        self.version = "2.4.0"
        self.distribution_zip = DistributionZip(self.product, self.version, self.work_dir)

    def test_distribution_zip_vars(self) -> None:
        self.assertEqual(self.distribution_zip.filename, self.product)
        self.assertEqual(self.distribution_zip.version, self.version)
        self.assertEqual(self.distribution_zip.work_dir, self.work_dir)

    def test_install_dir(self) -> None:
        self.assertEqual(self.distribution_zip.install_dir, os.path.join(self.work_dir, f"{self.product}-{self.version}"))

    def test_config_dir(self) -> None:
        self.assertEqual(self.distribution_zip.config_dir, os.path.join(self.work_dir, f"{self.product}-{self.version}", "config"))

    def test_install(self) -> None:
        with patch("test_workflow.integ_test.distribution_zip.ZipFile") as mock_zipfile_open:
            mock_zipfile_extractall = MagicMock()
            mock_zipfile_open.return_value.__enter__.return_value.extractall = mock_zipfile_extractall

            self.distribution_zip.install(os.path.join(self.work_dir, "artifacts", "dist", f"{self.product}-min-{self.version}-windows-x64.zip"))

            mock_zipfile_open.assert_called_with(os.path.join(self.work_dir, "artifacts", "dist", f"{self.product}-min-{self.version}-windows-x64.zip"), "r")
            mock_zipfile_extractall.assert_called_with(self.work_dir)

    def test_start_cmd(self) -> None:
        self.assertEqual(self.distribution_zip.start_cmd, "./opensearch-dashboards.bat")

    @patch("subprocess.check_call")
    def test_uninstall(self, check_call_mock: Mock) -> None:
        self.distribution_zip.uninstall()
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"rm -rf {self.work_dir}/*", args_list[0][0][0])
