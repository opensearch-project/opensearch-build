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

from run_test_report import main


class TestRunTestReport(unittest.TestCase):

    TEST_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__),
        "tests_report_workflow",
        "data",
        "test_manifest.yml"
    )

    @pytest.fixture(autouse=True)
    def getCapfd(self, capfd: CaptureFixture) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_test_report.py", "--help"])
    def test_usage(self, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_test_report.py", TEST_MANIFEST_PATH, "-p", "opensearch=foo"])
    @patch('run_test_report.TestRunRunner')
    def test_main(self, runner_mock: Mock, *mocks: Any) -> None:

        main()
        runner_mock.assert_called()
