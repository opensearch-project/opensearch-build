# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import sys

from test_workflow.compare_benchmark.compare_args import CompareArgs
from test_workflow.compare_benchmark.compare_test_runner import CompareTestRunner


def main() -> int:
    """
    Entry point for Compare Test with two IDs to compare. Will call out in test.sh with compare as argument
    """
    compare_args = CompareArgs()

    compare_test_runner = CompareTestRunner()
    compare_test_runner.run_comparison(compare_args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
