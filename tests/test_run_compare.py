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
from test_workflow.benchmark_test.benchmark_test_suite_compare import CompareTestSuite


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

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", ""])
    @patch.object(BenchmarkTestSuite, "execute")
    def test_compare_without_contender_id(self, mock_benchmark_test_suite_execute: Mock, *mocks: Any) -> None:
        with self.assertRaises(ValueError) as cm:
            main()

        # assert that the execute method of BenchmarkTestSuite was not called
        mock_benchmark_test_suite_execute.assert_not_called()

        # assert that the correct error message is raised
        self.assertEqual(str(cm.exception), "Both 'baseline' and 'contender' arguments are required for the 'compare' command.")

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", "54321", "--results-format", "markdown",
                                  "--results-numbers-align", "right", "--results-file", "comparison_results.md", "--show-in-results", "all"])
    @patch.object(BenchmarkTestSuite, "execute")
    def test_execute_compare_test_with_all_params(self, mock_benchmark_test_suite_execute: Mock, *mocks: Any) -> None:
        # mock the BenchmarkArgs instance and set the command attribute
        mock_benchmark_args = Mock(spec=BenchmarkArgs)
        mock_benchmark_args.command = "compare"
        mock_benchmark_args.baseline = "12345"
        mock_benchmark_args.contender = "54321"
        mock_benchmark_args.results_format = "markdown"
        mock_benchmark_args.results_numbers_align = "right"
        mock_benchmark_args.results_file = "comparison_results.md"
        mock_benchmark_args.show_in_results = "all"
        mock_benchmark_args.stack_suffix = "stack_suffix"

        expected_command = (
            "docker run --name docker-container-stack_suffix "
            "-v ~/.benchmark/benchmark.ini:/opensearch-benchmark/.benchmark/benchmark.ini "
            "opensearchproject/opensearch-benchmark:1.6.0 "
            "compare --baseline=12345 --contender=54321 "
            "--results-format=markdown "
            "--results-numbers-align=right "
            "--results-file=final_result.md "
            "--show-in-results=all "
        )

        with patch("test_workflow.benchmark_test.benchmark_args.BenchmarkArgs", return_value=mock_benchmark_args):
            main()

        # assert that the execute method of BenchmarkTestSuite was called
        mock_benchmark_test_suite_execute.assert_called_once()

        # assert that the command was formed correctly
        benchmark_test_suite = BenchmarkTestSuite("", False, mock_benchmark_args, "")
        compare_test_suite = benchmark_test_suite.test_suite
        assert isinstance(compare_test_suite, CompareTestSuite)
        compare_test_suite.form_command(mock_benchmark_args)  # Call the form_command method
        assert compare_test_suite.command == expected_command
