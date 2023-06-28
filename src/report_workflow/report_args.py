# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import argparse
import logging

from test_workflow.test_kwargs import TestKwargs


class ReportArgs:
    test_run_id: str
    keep: bool
    test_manifest_path: str
    artifact_paths: dict
    test_type: str
    logging_level: int

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Generate test report for given test data")
        parser.add_argument("test_manifest_path", type=str, help="Specify a test manifest path.")
        parser.add_argument("-p", "--artifact-paths", nargs='*', action=TestKwargs, default={},
                            help="Specify aritfacts paths for OpenSearch and OpenSearch Dashboards.")
        # e.g. --base-path https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/1234<test-run-id>/integ-test use more to save arguments number
        parser.add_argument("--base-path", type=str, default="",
                            help="Specify base paths for the integration test logs.")
        parser.add_argument("--test-type", type=str, default="integ-test", help="Specify test type of this.")
        parser.add_argument("--output-path", type=str, help="Specify the path location for the test-run manifest.")
        parser.add_argument("--test-run-id", type=int, help="The unique execution id for the test")
        parser.add_argument("--component", type=str, dest="components", nargs='*', help="Test a specific component or components instead of the entire distribution.")
        parser.add_argument(
            "-v", "--verbose", help="Show more verbose output.", action="store_const", default=logging.INFO, const=logging.DEBUG, dest="logging_level"
        )

        args = parser.parse_args()
        self.test_run_id = args.test_run_id
        self.logging_level = args.logging_level
        self.test_manifest_path = args.test_manifest_path
        self.artifact_paths = args.artifact_paths
        self.base_path = args.base_path
        self.test_type = args.test_type
        self.components = args.components
        self.output_path = args.output_path
