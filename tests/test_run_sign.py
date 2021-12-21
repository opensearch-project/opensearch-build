# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

import pytest

from run_sign import main


class TestRunSign(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_sign.py", "--help"])
    def test_usage(self, *mocks):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

    BUILD_MANIFEST = os.path.join(DATA_PATH, "opensearch-build-1.1.0.yml")

    @patch("argparse._sys.argv", ["run_sign.py", BUILD_MANIFEST])
    @patch("run_sign.SignArtifacts")
    @patch("run_sign.Signer")
    def test_main(self, mock_signer, mock_sign_artifacts, *mocks):
        main()

        mock_sign_artifacts.from_path.assert_called_once()
        mock_sign_artifacts.from_path.return_value.sign.assert_called_once()
