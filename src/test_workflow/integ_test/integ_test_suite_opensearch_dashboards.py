# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from pathlib import Path

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestComponent
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards
from test_workflow.integ_test.integ_test_suite import IntegTestSuite
from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuiteOpenSearchDashboards(IntegTestSuite):
    dependency_installer_opensearch_dashboards: DependencyInstallerOpenSearchDashboards
    bundle_manifest_opensearch_dashboards: BundleManifest
    build_manifest_opensearch_dashboards: BuildManifest

    def __init__(
        self,
        dependency_installer_opensearch: DependencyInstallerOpenSearch,
        dependency_installer_opensearch_dashboards: DependencyInstallerOpenSearchDashboards,
        component: TestComponent,
        test_config: TestComponent,
        bundle_manifest_opensearch: BundleManifest,
        bundle_manifest_opensearch_dashboards: BundleManifest,
        build_manifest_opensearch: BuildManifest,
        build_manifest_opensearch_dashboards: BuildManifest,
        work_dir: Path,
        test_recorder: TestRecorder
    ) -> None:

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

    def execute_tests(self) -> TestComponentResults:
        test_results = TestComponentResults()

        for config in self.test_config.integ_test["test-configs"]:
            status = self.__setup_cluster_and_execute_test_config(config)

            test_results.append(TestResult(self.component.name, config, status))
        return test_results

    def __setup_cluster_and_execute_test_config(self, config: str) -> int:
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
        ) as (endpoint, port):
            self.pretty_print_message("Running integration tests for " + self.component.name)
            os.chdir(self.work_dir)
            return self.execute_integtest_sh(endpoint, port, security, config)

    @property
    def test_artifact_files(self) -> dict:
        return {
            "cypress-videos": os.path.join(self.repo_work_dir, "cypress", "videos"),
            "cypress-screenshots": os.path.join(self.repo_work_dir, "cypress", "screenshots"),
            "cypress-report": os.path.join(self.repo_work_dir, "cypress", "results"),
        }
