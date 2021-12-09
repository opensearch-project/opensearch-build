# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import ANY, MagicMock, Mock, call, patch

import pytest
from pytest import CaptureFixture

from run_assemble import main


class TestRunAssemble(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def getCapfd(self, capfd: CaptureFixture) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_assemble.py", "--help"])
    def test_usage(self) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    BUILD_MANIFEST = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-1.1.0.yml")

    @patch("os.makedirs")
    @patch("os.getcwd", return_value="curdir")
    @patch("argparse._sys.argv", ["run_assemble.py", BUILD_MANIFEST])
    @patch("run_assemble.Bundles.create")
    @patch("run_assemble.BundleRecorder", return_value=MagicMock())
    def test_main(self, mock_recorder: Mock, mock_bundles: Mock, getcwd: Mock, makeDirs: Mock) -> None:
        mock_bundle = MagicMock(min_dist=MagicMock(archive_path="path"))
        mock_bundles.return_value.__enter__.return_value = mock_bundle

        main()

        mock_bundle.install_min.assert_called()
        mock_bundle.install_plugins.assert_called()

        mock_bundle.package.assert_called_with(os.path.join("curdir", "dist", "opensearch"))

        mock_recorder.return_value.write_manifest.assert_has_calls([
            call("path"),
            call(os.path.join("curdir", "dist", "opensearch"))
        ])  # manifest included in package

        self.assertEqual(getcwd.call_count, 2)
        makeDirs.assert_called_once_with(ANY, exist_ok=True)
