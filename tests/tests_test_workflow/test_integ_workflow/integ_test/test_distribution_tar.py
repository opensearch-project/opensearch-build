# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

from test_workflow.integ_test.distribution_tar import DistributionTar


class TestDistributionTar(unittest.TestCase):

    def setUp(self) -> None:

        self.work_dir = os.path.join(os.path.dirname(__file__), "data")
        self.distribution_tar = DistributionTar("opensearch", "1.3.0", self.work_dir)
        self.distribution_tar_dashboards = DistributionTar("opensearch-dashboards", "1.3.0", self.work_dir)

    def test_distribution_tar_vars(self) -> None:
        self.assertEqual(self.distribution_tar.filename, 'opensearch')
        self.assertEqual(self.distribution_tar.version, '1.3.0')
        self.assertEqual(self.distribution_tar.work_dir, self.work_dir)

    def test_install_dir(self) -> None:
        self.assertEqual(self.distribution_tar.install_dir, os.path.join(self.work_dir, "opensearch-1.3.0"))

    def test_config_dir(self) -> None:
        self.assertEqual(self.distribution_tar.config_dir, os.path.join(self.work_dir, "opensearch-1.3.0", "config"))

    def test_install(self) -> None:
        with patch("tarfile.open") as mock_tarfile_open:
            mock_tarfile_extractall = MagicMock()
            mock_tarfile_open.return_value.__enter__.return_value.extractall = mock_tarfile_extractall

            self.distribution_tar.install(os.path.join(self.work_dir, "artifacts", "dist", "opensearch-min-1.3.0-linux-x64.tar.gz"))

            mock_tarfile_open.assert_called_with(os.path.join(self.work_dir, "artifacts", "dist", "opensearch-min-1.3.0-linux-x64.tar.gz"), "r:gz")
            mock_tarfile_extractall.assert_called_with(self.work_dir)

    def test_start_cmd(self) -> None:
        self.assertEqual(self.distribution_tar.start_cmd, "./opensearch-tar-install.sh")
        self.assertEqual(self.distribution_tar_dashboards.start_cmd, "./opensearch-dashboards")

    @patch("subprocess.check_call")
    def test_uninstall(self, check_call_mock: Mock) -> None:
        self.distribution_tar.uninstall()
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"rm -rf {self.work_dir}/*", args_list[0][0][0])
