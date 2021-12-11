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
import os
import uuid

from manifests.test_manifest import TestManifest
from test_workflow.test_kwargs import TestKwargs


class TestArgs:
    test_run_id: int
    component: str
    keep: bool
    logging_level: int

    def __init__(self):
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
        parser.add_argument("test_manifest_path", type=str, help="Specify a test manifest path.")
        parser.add_argument("-p", "--paths", nargs='*', action=TestKwargs, help="Specify paths for OpenSearch and OpenSearch Dashboards.")
        parser.add_argument("--test-run-id", type=int, help="The unique execution id for the test")
        parser.add_argument("--component", type=str, help="Test a specific component instead of the entire distribution.")
        parser.add_argument("--keep", dest="keep", action="store_true", help="Do not delete the working temporary directory.")
        parser.add_argument(
            "-v", "--verbose", help="Show more verbose output.", action="store_const", default=logging.INFO, const=logging.DEBUG, dest="logging_level"
        )
        args = parser.parse_args()
        self.test_run_id = args.test_run_id or uuid.uuid4().hex
        self.component = args.component
        self.keep = args.keep
        self.logging_level = args.logging_level
        self.test_manifest = TestManifest.from_path(args.test_manifest_path)

        cwd = os.getcwd()
        self.opensearch_path = args.paths.get("opensearch", cwd) if args.paths else cwd

        if self.test_manifest.name == "OpenSearch Dashboards":
            self.opensearch_dashboards_path = args.paths.get("opensearch-dashboards", cwd) if args.paths else cwd


TestArgs.__test__ = False  # type:ignore
