# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from pathlib import Path

from manifests.build_manifest import BuildComponent
from manifests.test_manifest import TestComponent, TestManifest
from test_workflow.bwc_test.bwc_test_runner import BwcTestRunner
from test_workflow.bwc_test.bwc_test_start_properties_opensearch_dashboards import BwcTestStartPropertiesOpenSearchDashboards
from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite
from test_workflow.bwc_test.bwc_test_suite_opensearch_dashboards import BwcTestSuiteOpenSearchDashboards
from test_workflow.test_args import TestArgs


class BwcTestRunnerOpenSearchDashboards(BwcTestRunner):

    def __init__(self, args: TestArgs, test_manifest: TestManifest) -> None:
        self.properties = BwcTestStartPropertiesOpenSearchDashboards(args.paths.get("opensearch-dashboards", os.getcwd()))
        super().__init__(args, test_manifest, self.properties.build_manifest.components)
        logging.info("Entering BWC test for OpenSearch Dashboards")

    def __create_test_suite__(self, component: BuildComponent, test_config: TestComponent, work_dir: Path) -> BwcTestSuite:
        return BwcTestSuiteOpenSearchDashboards(
            work_dir,
            component,
            test_config,
            self.test_recorder,
            self.properties.bundle_manifest,
        )
