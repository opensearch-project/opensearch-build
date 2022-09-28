#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from manifests.test_manifest import TestManifest
from system import console
from test_workflow.bwc_test.bwc_test_runners import BwcTestRunners
from test_workflow.test_args import TestArgs


def main() -> int:
    args = TestArgs()

    # Any logging.info call preceding to next line in the execution chain will make the console output not displaying logs in console.
    console.configure(level=args.logging_level)

    test_manifest = TestManifest.from_path(args.test_manifest_path)

    all_results = BwcTestRunners.from_test_manifest(args, test_manifest).run()

    all_results.log()

    if all_results.failed():
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
