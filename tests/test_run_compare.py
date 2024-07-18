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

from run_compare_tests import main

class TestRunCompareTests(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "--help"])
    def test_usage(self) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))
    
    @patch("argparse._sys.argv", ["run_compare_tests.py"])
    @patch("run_compare_tests.CompareTestRunner.from_args")
    
    def test_default_execute_compare(self, mock_runner: Mock, *mocks: Any) -> None:
        with patch("run_compare_tests.main") as mocked_main:
            main()
            self.assertEqual(1, mock_runner.call_count)