# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from pathlib import Path

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestComponent
from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards
from test_workflow.integ_test.integ_test_suite import IntegTestSuite
from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards
from test_workflow.integ_test.topology import ClusterEndpoint, NodeEndpoint
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuiteOpenSearchDashboards(IntegTestSuite):
    dependency_installer_opensearch_dashboards: DependencyInstallerOpenSearchDashboards
    bundle_manifest_opensearch_dashboards: BundleManifest
    build_manifest_opensearch_dashboards: BuildManifest
    repo: GitRepository

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

        # Integ-tests for OSD now clones FunctionalTestDashboards Repository by default and points to integtest.sh from FunctionalTestDashboards for all OSD plugins

        self.repo = GitRepository(
            build_manifest_opensearch_dashboards.components['functionalTestDashboards'].repository,
            build_manifest_opensearch_dashboards.components['functionalTestDashboards'].commit_id,
            os.path.join(self.work_dir, self.component.name),
            test_config.working_directory
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
        if "additional-cluster-configs" in self.test_config.integ_test.keys():
            self.additional_cluster_config = self.test_config.integ_test.get("additional-cluster-configs")
            logging.info(f"Additional config found: {self.additional_cluster_config}")

        if self.additional_cluster_config is None:
            self.additional_cluster_config = {}

        with LocalTestClusterOpenSearchDashboards.create(
            self.dependency_installer,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component.name,
            self.additional_cluster_config,
            self.bundle_manifest,
            self.bundle_manifest_opensearch_dashboards,
            security,
            config,
            self.test_recorder,
        ) as (endpoint, port):
            self.pretty_print_message("Running integration tests for " + self.component.name)
            os.chdir(self.work_dir)
            return self.execute_integtest_sh(endpoint, port, security, config)

    def multi_execute_integtest_sh(self, cluster_endpoints: list, security: bool, test_config: str) -> int:
        script = ScriptFinder.find_integ_test_script(self.component.name, self.repo.working_directory)

        def custom_node_endpoint_encoder(node_endpoint: NodeEndpoint) -> dict:
            return {"endpoint": node_endpoint.endpoint, "port": node_endpoint.port, "transport": node_endpoint.transport}
        if os.path.exists(script):
            single_node = cluster_endpoints[0].data_nodes[0]
            cmd = f"bash {script} -b {single_node.endpoint} -p {single_node.port} -s {str(security).lower()} -t {self.component.name} -v {self.bundle_manifest.build.version} -o default"
            self.repo_work_dir = os.path.join(
                self.repo.dir, self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, self.repo_work_dir, True, False)
            self.test_result_data.append(
                TestResultData(
                    self.component.name,
                    test_config,
                    status,
                    stdout,
                    stderr,
                    self.test_artifact_files
                )
            )
            if stderr:
                logging.info("Stderr reported for component: " + self.component.name)
                logging.info(stderr)
            return status
        else:
            logging.info(f"{script} does not exist. Skipping integ tests for {self.component.name}")
            return 0

    def execute_integtest_sh(self, endpoint: str, port: int, security: bool, test_config: str) -> int:
        cluster_endpoint_port = [ClusterEndpoint("cluster1", [NodeEndpoint(endpoint, port, 9300)], [])]
        return self.multi_execute_integtest_sh(cluster_endpoint_port, security, test_config)

    @property
    def test_artifact_files(self) -> dict:
        return {
            "cypress-videos": os.path.join(self.repo_work_dir, "cypress", "videos"),
            "cypress-screenshots": os.path.join(self.repo_work_dir, "cypress", "screenshots"),
            "cypress-report": os.path.join(self.repo_work_dir, "cypress", "results"),
        }
