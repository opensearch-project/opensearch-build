# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from system.temporary_directory import TemporaryDirectory
from test_workflow.integ_test.integ_test_runner import IntegTestRunner
from test_workflow.integ_test.integ_test_start_properties_opensearch import IntegTestStartPropertiesOpenSearch
from test_workflow.integ_test.integ_test_start_properties_opensearch_dashboards import IntegTestStartPropertiesOpenSearchDashboards
from test_workflow.integ_test.integ_test_suite_opensearch_dashboards import IntegTestSuiteOpenSearchDashboards
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


class IntegTestRunnerOpenSearchDashboards(IntegTestRunner):

    def __init__(self, args, test_manifest):
        super().__init__(args, test_manifest)

        self.properties_dependency = IntegTestStartPropertiesOpenSearch(args.path)
        self.properties = IntegTestStartPropertiesOpenSearchDashboards(args.path)

    def run(self):
        logging.info("Running integ test for OpenSearch Dashboards")

        tests_dir = os.path.join(os.getcwd(), "test-results", "opensearch-dashboards")
        os.makedirs(tests_dir, exist_ok=True)
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            test_recorder = TestRecorder(self.args.test_run_id, "integ-test", tests_dir)

            all_results = TestSuiteResults()
            for component in self.properties.build_manifest.components.select(focus=self.args.component):
                if component.name in self.test_manifest.components:
                    test_config = self.test_manifest.components[component.name]
                    if test_config.integ_test:
                        test_suite = IntegTestSuiteOpenSearchDashboards(
                            self.properties_dependency.dependency_installer,
                            self.properties.dependency_installer,
                            component,
                            test_config,
                            self.properties_dependency.bundle_manifest,
                            self.properties.bundle_manifest,
                            self.properties_dependency.build_manifest,
                            self.properties.build_manifest,
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
