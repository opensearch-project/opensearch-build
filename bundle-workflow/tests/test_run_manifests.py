# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, call, patch

import pytest

from run_manifests import main


class TestRunManifests(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_manifests.py", "--help"])
    def test_usage(self):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_manifests.py", "list"])
    @patch("run_manifests.logging", return_value=MagicMock())
    def test_main_list(self, mock_logging, *mocks):
        main()

        mock_logging.info.assert_has_calls(
            [
                call("OpenSearch 1.0.0"),
                call("OpenSearch 1.0.1"),
                call("OpenSearch 1.1.0"),
                call("OpenSearch 1.2.0"),
                call("OpenSearch 2.0.0"),
            ]
        )

        mock_logging.info.assert_has_calls([call("Done.")])

    @patch("argparse._sys.argv", ["run_manifests.py", "update"])
    @patch("run_manifests.InputManifests", return_value=MagicMock())
    def test_main_update(self, mock_manifests, *mocks):
        main()
        mock_manifests.return_value.update.assert_called()
