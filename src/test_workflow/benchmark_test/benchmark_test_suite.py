# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_base import BenchmarkTestBase
from test_workflow.benchmark_test.benchmark_test_suite_compare import CompareTestSuite
from test_workflow.benchmark_test.benchmark_test_suite_execute import ExecuteTestSuite


class BenchmarkTestSuite:
    test_suite: BenchmarkTestBase

    def __init__(
            self,
            endpoint: Any,
            security: bool,
            args: BenchmarkArgs,
            password: str
    ) -> None:
        if args.command == 'execute-test':
            self.test_suite = ExecuteTestSuite(endpoint, security, args, password)
        elif args.command == 'compare':
            self.test_suite = CompareTestSuite(endpoint, security, args, password)
        else:
            raise ValueError(f"Invalid command: {args.command}")

    def execute(self) -> None:
        self.test_suite.execute()
