# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Dict, Type, Union

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_suite_compare import BenchmarkTestSuiteCompare
from test_workflow.benchmark_test.benchmark_test_suite_execute import BenchmarkTestSuiteExecute


class BenchmarkTestSuiteRunners:
    SUITES: Dict[str, Type[Union[BenchmarkTestSuiteExecute, BenchmarkTestSuiteCompare]]] = {
        "execute-test": BenchmarkTestSuiteExecute,
        "compare": BenchmarkTestSuiteCompare
    }

    @classmethod
    def from_args(
        cls,
        args: BenchmarkArgs,
        endpoint: str = None,
        security: bool = False,
        password: str = ''
    ) -> Union[BenchmarkTestSuiteExecute, BenchmarkTestSuiteCompare]:
        test_class = cls.SUITES.get(args.command)
        if test_class is None:
            raise ValueError(f"Unknown command: {args.command}")

        if issubclass(test_class, BenchmarkTestSuiteExecute):
            return test_class(endpoint, security, args, password)
        elif issubclass(test_class, BenchmarkTestSuiteCompare):
            return test_class(args)
        else:
            raise ValueError(f"Unexpected test class type for command: {args.command}")
