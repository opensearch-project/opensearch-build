# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from typing import Any
from unittest.mock import Mock, patch

import pytest
from pytest import CaptureFixture

from run_smoke_test import main


class TestRunSmokeTest(unittest.TestCase):

    TEST_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__),
        "tests_test_workflow",
        "test_smoke_workflow",
        "smoke_test",
        "data",
        "test_manifest.yml"
    )

    @pytest.fixture(autouse=True)
    def getCapfd(self, capfd: CaptureFixture) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_smoke_test.py", "--help"])
    def test_usage(self, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_smoke_test.py", TEST_MANIFEST_PATH, "--paths", "opensearch=foo"])
    @patch('run_smoke_test.SmokeTestRunners')
    def test_main(self, mock_runners: Mock, *mocks: Any) -> None:

        main()
        mock_runners.from_test_manifest.assert_called()
