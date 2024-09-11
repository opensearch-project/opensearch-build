# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from run_benchmark_test import main
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_suite_compare import BenchmarkTestSuiteCompare
from test_workflow.benchmark_test.benchmark_test_suite_runners import BenchmarkTestSuiteRunners


class TestRunBenchmarkTestCompare(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "--help"])
    @patch("run_benchmark_test.check_docker")
    def test_usage(self, mock_docker: Mock) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", "54321"])
    @patch.object(BenchmarkTestSuiteRunners, "from_args")
    def test_default_execute_compare_test(self, mock_from_args: Mock, *mocks: Any) -> None:
        mock_instance = MagicMock()
        mock_instance.execute = MagicMock()

        mock_from_args.return_value = mock_instance

        # mock the BenchmarkArgs instance and set the command attribute
        mock_benchmark_args = Mock(spec=BenchmarkArgs)
        mock_benchmark_args.command = "compare"

        with patch("test_workflow.benchmark_test.benchmark_args.BenchmarkArgs", return_value=mock_benchmark_args):
            with patch("run_benchmark_test.check_docker", return_value=Mock()):
                main()

        # assert that the execute method of BenchmarkTestSuite was called
        mock_instance.execute.assert_called_once()

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", "54321", "--results-format", "markdown", "--results-numbers-align", "right"])
    @patch.object(BenchmarkTestSuiteRunners, "from_args")
    def test_execute_compare_test_with_params(self, mock_from_args: Mock, *mocks: Any) -> None:
        # mock the instance returned by BenchmarkTestSuiteRunners.from_args
        mock_instance = MagicMock()
        mock_instance.execute = MagicMock()

        # set the return value of BenchmarkTestSuiteRunners.from_args to the mocked instance
        mock_from_args.return_value = mock_instance

        # mock the BenchmarkArgs instance and set the command attribute
        mock_benchmark_args = Mock(spec=BenchmarkArgs)
        mock_benchmark_args.command = "compare"

        with patch("test_workflow.benchmark_test.benchmark_args.BenchmarkArgs", return_value=mock_benchmark_args):
            with patch("run_benchmark_test.check_docker", return_value=Mock()):
                main()

        # assert that the execute method of the mocked instance was called
        mock_instance.execute.assert_called_once()

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", ""])
    @patch.object(BenchmarkTestSuiteRunners, "from_args")
    def test_compare_without_contender_id(self, mock_from_args: Mock, *mocks: Any) -> None:
        # mock the instance returned by BenchmarkTestSuiteRunners.from_args
        mock_instance = MagicMock()
        mock_instance.execute = MagicMock()

        # set the return value of BenchmarkTestSuiteRunners.from_args to the mocked instance
        mock_from_args.return_value = mock_instance

        # mock the BenchmarkArgs instance and set the command attribute
        mock_benchmark_args = Mock(spec=BenchmarkArgs)
        mock_benchmark_args.command = "compare"

        with patch("test_workflow.benchmark_test.benchmark_args.BenchmarkArgs", return_value=mock_benchmark_args):
            with patch("run_benchmark_test.check_docker", return_value=Mock()):
                with self.assertRaises(ValueError) as cm:
                    main()

        # assert that the execute method of the mocked instance was not called
        mock_instance.execute.assert_not_called()

        # assert that the correct error message is raised
        self.assertEqual(str(cm.exception), "Both 'baseline' and 'contender' arguments are required for the 'compare' command.")

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "compare", "12345", "54321", "--results-format", "markdown",
                                  "--results-numbers-align", "right", "--show-in-results", "all"])
    def test_form_compare_command(self, *mocks: Any) -> None:
        # create an actual BenchmarkArgs instance
        args = BenchmarkArgs()

        # create a BenchmarkTestSuiteCompare instance
        compare_test_suite = BenchmarkTestSuiteCompare(args)

        # call form_command directly
        actual_command = compare_test_suite.form_command()

        # define the expected command
        expected_command = (
            f"docker run --name docker-container-{args.stack_suffix} "
            "opensearchproject/opensearch-benchmark:1.8.0 "
            "compare --baseline=12345 --contender=54321 "
            "--results-format=markdown "
            "--results-numbers-align=right "
            "--results-file=final_result.md "
            "--show-in-results=all "
        )

        # assert that the actual command matches the expected command
        self.assertEqual(actual_command, expected_command)
