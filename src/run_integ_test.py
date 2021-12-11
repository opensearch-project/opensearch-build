#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from system import console
from test_workflow.integ_test.integ_test_runners import IntegTestRunners
from test_workflow.test_args import TestArgs


def main():
    args = TestArgs()

    console.configure(level=args.logging_level)

    all_results = IntegTestRunners.from_test_manifest(args).run()

    all_results.log()

    if all_results.failed():
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
