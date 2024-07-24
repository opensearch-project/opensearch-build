# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from typing import Any
from unittest.mock import Mock, patch

import pytest

from run_benchmark_test import main
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_suite import BenchmarkTestSuite


class TestRunBenchmarkTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "--help"])
    def test_usage(self) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", "54321"])
    @patch.object(BenchmarkTestSuite, "execute")
    def test_default_execute_compare_test(self, mock_benchmark_test_suite_execute: Mock, *mocks: Any) -> None:
        # mock the BenchmarkArgs instance and set the command attribute
        mock_benchmark_args = Mock(spec=BenchmarkArgs)
        mock_benchmark_args.command = "compare"

        with patch("test_workflow.benchmark_test.benchmark_args.BenchmarkArgs", return_value=mock_benchmark_args):
            main()

        # assert that the execute method of BenchmarkTestSuite was called
        mock_benchmark_test_suite_execute.assert_called_once()

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", "54321", "--results-format", "markdown", "--results-numbers-align", "right"])
    @patch.object(BenchmarkTestSuite, "execute")
    def test_execute_compare_test_with_params(self, mock_benchmark_test_suite_execute: Mock, *mocks: Any) -> None:
        # mock the BenchmarkArgs instance and set the command attribute
        mock_benchmark_args = Mock(spec=BenchmarkArgs)
        mock_benchmark_args.command = "compare"

        with patch("test_workflow.benchmark_test.benchmark_args.BenchmarkArgs", return_value=mock_benchmark_args):
            main()

        # assert that the execute method of BenchmarkTestSuite was called
        mock_benchmark_test_suite_execute.assert_called_once()

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345"])
    @patch.object(BenchmarkTestSuite, "execute")
    def test_compare_without_contender_id(self, mock_benchmark_test_suite_execute: Mock, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

        # assert that the execute method of BenchmarkTestSuite was not called
        mock_benchmark_test_suite_execute.assert_not_called()

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "copmare"])
    def test_invalid_command(self, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

        _, err = self.capfd.readouterr()
        self.assertIn("argument command: invalid choice", err)
