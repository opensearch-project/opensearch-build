# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from test_workflow.benchmark_test.benchmark_test_suite_compare import BenchmarkTestSuiteCompare


class TestBenchmarkTestSuiteCompare(unittest.TestCase):

    def setUp(self) -> None:
        self.args = Mock()
        self.args.command = "compare"
        self.args.stack_suffix = "test-suffix"
        self.args.baseline = "baseline-id"
        self.args.contender = "contender-id"
        self.args.results_format = "markdown"
        self.args.results_numbers_align = "right"
        self.args.show_in_results = "all"

    @patch('subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.copy_comparison_results_to_local')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.cleanup')
    def test_execute(self, mock_cleanup: Mock, mock_copy_results: Mock, mock_check_call: Mock) -> None:
        self.args.benchmark_config = None
        compare = BenchmarkTestSuiteCompare(self.args)
        compare.execute()
        mock_check_call.assert_called_once()

        self.assertEqual(compare.command, 'docker run --name docker-container-test-suffix '
                                          'opensearchproject/opensearch-benchmark:1.6.0 compare '
                                          '--baseline=baseline-id --contender=contender-id --results-format=markdown '
                                          '--results-numbers-align=right --results-file=final_result.md '
                                          '--show-in-results=all ')
        mock_copy_results.assert_called_once()
        mock_cleanup.assert_called_once()

    @patch('subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.copy_comparison_results_to_local')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.cleanup')
    def test_execute_with_benchmark_config(self, mock_cleanup: Mock, mock_copy_results: Mock, mock_check_call: Mock) -> None:
        self.args.benchmark_config = '/some/path/benchmark.ini'
        compare = BenchmarkTestSuiteCompare(self.args)
        compare.execute()
        mock_check_call.assert_called_once()
        self.assertEqual(compare.command, 'docker run --name docker-container-test-suffix  -v '
                                          '/some/path/benchmark.ini:/opensearch-benchmark/.benchmark/benchmark.ini '
                                          'opensearchproject/opensearch-benchmark:1.6.0 compare '
                                          '--baseline=baseline-id --contender=contender-id --results-format=markdown '
                                          '--results-numbers-align=right --results-file=final_result.md '
                                          '--show-in-results=all ')
        mock_copy_results.assert_called_once()
        mock_cleanup.assert_called_once()

    @patch('subprocess.check_call')
    @patch('logging.info')
    def test_copy_comparison_results_to_local(self, mock_logging_info: Mock, mock_check_call: Mock) -> None:
        compare = BenchmarkTestSuiteCompare(self.args)
        cwd = os.getcwd()

        compare.copy_comparison_results_to_local()

        mock_check_call.assert_called_once_with(
            f"docker cp docker-container-{self.args.stack_suffix}:opensearch-benchmark"
            f"/final_result.md {cwd}/final_result_{self.args.stack_suffix}.md",
            cwd=cwd,
            shell=True,
        )

        expected_log_message = f"Final results copied to {cwd}/final_result_{self.args.stack_suffix}.md"
        mock_logging_info.assert_called_once_with(expected_log_message)

    def test_from_args_compare(self) -> None:
        from test_workflow.benchmark_test.benchmark_test_suite_runners import BenchmarkTestSuiteRunners

        runner = BenchmarkTestSuiteRunners.from_args(self.args)

        self.assertIsInstance(runner, BenchmarkTestSuiteCompare)
        self.assertEqual(runner.args, self.args)


if __name__ == '__main__':
    unittest.main()
