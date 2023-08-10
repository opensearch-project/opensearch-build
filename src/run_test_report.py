# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os.path
import sys
from typing import Any

from manifests.test_manifest import TestManifest
from report_workflow.report_args import ReportArgs
from report_workflow.test_report_runner import TestReportRunner
from system import console


def main() -> Any:
    args = ReportArgs()

    console.configure(level=args.logging_level)

    test_manifest = TestManifest.from_path(args.test_manifest_path)

    test_report_runner = TestReportRunner(args, test_manifest)

    test_report_data = test_report_runner.update_data()

    test_run = test_report_runner.generate_report(test_report_data, args.output_path or os.getcwd())

    return test_run


if __name__ == "__main__":
    sys.exit(main())
