# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from manifests.test_manifest import TestManifest
from system import console
from report_workflow.test_run_runner import TestRunRunner
from report_workflow.report_args import ReportArgs


def main() -> int:
    args = ReportArgs()

    # Any logging.info call preceding to next line in the execution chain will make the console output not displaying logs in console.
    console.configure(level=args.logging_level)

    test_manifest = TestManifest.from_path(args.test_manifest_path)

    test_run_runner = TestRunRunner(args, test_manifest)

    test_run_data = test_run_runner.update_data()

    test_run = test_run_runner.generate_report(test_run_data)

    # test_run = test_run_runner.generate_report(test_run_data, "with/path")

    return test_run

    # all_results = IntegTestRunners.from_test_manifest(args, test_manifest).run()
    #
    # all_results.log()
    #
    # if all_results.failed():
    #     return 1
    # else:
    #     return 0


if __name__ == "__main__":
    sys.exit(main())
