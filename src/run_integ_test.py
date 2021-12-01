#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import sys

from manifests.test_manifest import TestManifest
from system import console
from test_workflow.integ_test.integ_test_runner_opensearch import IntegTestRunnerOpenSearch
from test_workflow.integ_test.integ_test_runner_opensearch_dashboards import IntegTestRunnerOpenSearchDashboards
from test_workflow.test_args import TestArgs


def main():
    args = TestArgs()

    console.configure(level=args.logging_level)

    test_manifest = TestManifest.from_path(args.test_manifest_path)

    all_results = None

    if test_manifest.name == "OpenSearch Dashboards":
        all_results = IntegTestRunnerOpenSearchDashboards(args, test_manifest).run()
    else:
        all_results = IntegTestRunnerOpenSearch(args, test_manifest).run()

    all_results.log()

    if all_results.failed():
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
