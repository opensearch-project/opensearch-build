# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_suite_compare import BenchmarkTestSuiteCompare
from test_workflow.benchmark_test.benchmark_test_suite_execute import BenchmarkTestSuiteExecute
from test_workflow.benchmark_test.benchmark_test_suite_runners import BenchmarkTestSuiteRunners


class TestBenchmarkTestSuiteRunners(unittest.TestCase):
    @patch.object(BenchmarkTestSuiteExecute, '__init__', return_value=None)
    def test_from_args_execute_test(self, mock_execute_init: Mock) -> None:
        args = Mock(BenchmarkArgs)
        args.command = 'execute-test'
        endpoint = 'https://example.com'
        security = True
        password = 'password'

        runner = BenchmarkTestSuiteRunners.from_args(args, endpoint, security, password)

        mock_execute_init.assert_called_once_with(endpoint, security, args, password)
        self.assertIsInstance(runner, BenchmarkTestSuiteExecute)

    @patch.object(BenchmarkTestSuiteCompare, '__init__', return_value=None)
    def test_from_args_compare(self, mock_compare_init: Mock) -> None:
        args = Mock(BenchmarkArgs)
        args.command = 'compare'

        runner = BenchmarkTestSuiteRunners.from_args(args)

        mock_compare_init.assert_called_once_with(args)
        self.assertIsInstance(runner, BenchmarkTestSuiteCompare)

    def test_from_args_unknown_command(self) -> None:
        args = Mock(BenchmarkArgs)
        args.command = 'unknown'

        with self.assertRaises(ValueError) as cm:
            BenchmarkTestSuiteRunners.from_args(args)

        self.assertEqual(str(cm.exception), "Unknown command: unknown")

    def test_from_args_unexpected_test_class(self) -> None:
        with patch.dict(BenchmarkTestSuiteRunners.SUITES, {'unknown': object}):
            args = Mock(BenchmarkArgs)
            args.command = 'unknown'

            with self.assertRaises(ValueError) as cm:
                BenchmarkTestSuiteRunners.from_args(args)

            self.assertEqual(str(cm.exception), "Unexpected test class type for command: unknown")
