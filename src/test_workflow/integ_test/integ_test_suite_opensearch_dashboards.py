# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from test_workflow.integ_test.integ_test_suite import IntegTestSuite
from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuiteOpenSearchDashboards(IntegTestSuite):

    def __init__(
        self,
        dependency_installer_opensearch,
        dependency_installer_opensearch_dashboards,
        component,
        test_config,
        bundle_manifest_opensearch,
        bundle_manifest_opensearch_dashboards,
        build_manifest_opensearch,
        build_manifest_opensearch_dashboards,
        work_dir,
        test_recorder
    ):

        super().__init__(
            work_dir,
            component,
            test_config,
            test_recorder,
            dependency_installer_opensearch,
            bundle_manifest_opensearch,
            build_manifest_opensearch
        )

        self.dependency_installer_opensearch_dashboards = dependency_installer_opensearch_dashboards
        self.bundle_manifest_opensearch_dashboards = bundle_manifest_opensearch_dashboards
        self.build_manifest_opensearch_dashboards = build_manifest_opensearch_dashboards

    def execute_tests(self):
        test_results = TestComponentResults()

        for config in self.test_config.integ_test["test-configs"]:
            status = self.__setup_cluster_and_execute_test_config(config)

            test_results.append(TestResult(self.component.name, config, status))
        return test_results

    def __setup_cluster_and_execute_test_config(self, config):
        security = self.is_security_enabled(config)

        with LocalTestClusterOpenSearchDashboards.create(
            self.dependency_installer,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component.name,
            {},
            self.bundle_manifest,
            self.bundle_manifest_opensearch_dashboards,
            security,
            config,
            self.test_recorder,
        ) as (test_cluster_endpoint, test_cluster_port):
            self.pretty_print_message("Running integration tests for " + self.component.name)
            os.chdir(self.work_dir)
            return self.execute_integtest_sh(test_cluster_endpoint, test_cluster_port, security, config)
