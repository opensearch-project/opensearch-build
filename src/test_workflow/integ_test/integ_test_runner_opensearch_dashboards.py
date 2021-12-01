# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards
from test_workflow.integ_test.integ_test_runner import IntegTestRunner
from test_workflow.integ_test.integ_test_suite_opensearch_dashboards import IntegTestSuiteOpenSearchDashboards
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


class IntegTestRunnerOpenSearchDashboards(IntegTestRunner):

    def __init__(self, args, test_manifest):
        super().__init__(args, test_manifest)

        self.bundle_manifest_opensearch_dashboards = BundleManifest.from_urlpath("/".join([args.path.rstrip("/"), "dist/opensearch-dashboards/manifest.yml"]))
        self.build_manifest_opensearch_dashboards = BuildManifest.from_urlpath("/".join([args.path.rstrip("/"), "builds/opensearch-dashboards/manifest.yml"]))
        self.dependency_installer_opensearch_dashboards = DependencyInstallerOpenSearchDashboards(
            args.path, self.build_manifest_opensearch_dashboards, self.bundle_manifest_opensearch_dashboards)

    def run(self):
        logging.info("Running integ test for OpenSearch Dashboards")

        tests_dir = os.path.join(os.getcwd(), "test-results", "opensearch-dashboards")
        os.makedirs(tests_dir, exist_ok=True)
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            test_recorder = TestRecorder(self.args.test_run_id, "integ-test", tests_dir)

            all_results = TestSuiteResults()
            for component in self.build_manifest_opensearch_dashboards.components.select(focus=self.args.component):
                if component.name in self.test_manifest.components:
                    test_config = self.test_manifest.components[component.name]
                    if test_config.integ_test:
                        test_suite = IntegTestSuiteOpenSearchDashboards(
                            self.dependency_installer,
                            self.dependency_installer_opensearch_dashboards,
                            component,
                            test_config,
                            self.bundle_manifest,
                            self.bundle_manifest_opensearch_dashboards,
                            self.build_manifest,
                            self.build_manifest_opensearch_dashboards,
                            work_dir.name,
                            test_recorder
                        )
                        test_results = test_suite.execute_tests()
                        all_results.append(component.name, test_results)
                    else:
                        logging.info(f"Skipping integ-tests for {component.name}, as it is currently not supported")
                else:
                    logging.info(f"Skipping integ-tests for {component.name}, as it is currently not declared in the test manifest")

        return all_results
