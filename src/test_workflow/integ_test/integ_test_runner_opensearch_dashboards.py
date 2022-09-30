# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from pathlib import Path

from manifests.test_manifest import TestComponent, TestManifest
from test_workflow.integ_test.integ_test_runner import IntegTestRunner
from test_workflow.integ_test.integ_test_start_properties_opensearch import IntegTestStartPropertiesOpenSearch
from test_workflow.integ_test.integ_test_start_properties_opensearch_dashboards import IntegTestStartPropertiesOpenSearchDashboards
from test_workflow.integ_test.integ_test_suite_opensearch_dashboards import IntegTestSuiteOpenSearchDashboards
from test_workflow.test_args import TestArgs


class IntegTestRunnerOpenSearchDashboards(IntegTestRunner):
    properties: IntegTestStartPropertiesOpenSearchDashboards
    properties_dependency: IntegTestStartPropertiesOpenSearch

    def __init__(self, args: TestArgs, test_manifest: TestManifest) -> None:
        self.properties_dependency = IntegTestStartPropertiesOpenSearch(args.paths.get("opensearch", os.getcwd()))
        self.properties = IntegTestStartPropertiesOpenSearchDashboards(args.paths.get("opensearch-dashboards", os.getcwd()))
        super().__init__(args, test_manifest, self.properties.build_manifest.components)
        logging.info("Entering integ test for OpenSearch Dashboards")

    def __create_test_suite__(self, component: TestComponent, test_config: TestComponent, work_dir: Path) -> IntegTestSuiteOpenSearchDashboards:
        return IntegTestSuiteOpenSearchDashboards(
            self.properties_dependency.dependency_installer,
            self.properties.dependency_installer,
            component,
            test_config,
            self.properties_dependency.bundle_manifest,
            self.properties.bundle_manifest,
            self.properties_dependency.build_manifest,
            self.properties.build_manifest,
            work_dir,
            self.test_recorder
        )
