# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import json
import logging
import os
from pathlib import Path
from typing import Any

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.integ_test.integ_test_suite import IntegTestSuite, InvalidTestConfigError
from test_workflow.integ_test.topology import NodeEndpoint, Topology
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuiteOpenSearch(IntegTestSuite):
    dependency_installer: DependencyInstallerOpenSearch
    repo: GitRepository

    def __init__(
        self,
        dependency_installer_opensearch: DependencyInstallerOpenSearch,
        component: Any,
        test_config: Any,
        bundle_manifest_opensearch: BundleManifest,
        build_manifest_opensearch: BuildManifest,
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
        self.repo = GitRepository(
            self.component.repository,
            self.component.commit_id,
            os.path.join(self.work_dir, self.component.name),
            test_config.working_directory
        )

    def execute_tests(self) -> TestComponentResults:
        test_results = TestComponentResults()
        self.__install_build_dependencies()
        for config in self.test_config.integ_test["test-configs"]:
            status = self.__setup_cluster_and_execute_test_config(config)
            test_results.append(TestResult(self.component.name, config, status))
        return test_results

    def __install_build_dependencies(self) -> None:
        if "build-dependencies" in self.test_config.integ_test:
            dependency_list = self.test_config.integ_test["build-dependencies"]
            if len(dependency_list) == 1 and "job-scheduler" in dependency_list:
                self.__copy_job_scheduler_artifact()
            else:
                raise InvalidTestConfigError("Integration test job only supports job-scheduler build dependency at present.")

    def __copy_job_scheduler_artifact(self) -> None:
        custom_local_path = os.path.join(self.repo.dir, "src", "test", "resources", "job-scheduler")
        for file in glob.glob(os.path.join(custom_local_path, "opensearch-job-scheduler-*.zip")):
            os.unlink(file)
        job_scheduler = self.build_manifest.components["job-scheduler"]
        self.dependency_installer.install_build_dependencies({"opensearch-job-scheduler": job_scheduler.version}, custom_local_path)

    def __setup_cluster_and_execute_test_config(self, config: str) -> int:
        security = self.is_security_enabled(config)
        if "additional-cluster-configs" in self.test_config.integ_test.keys():
            self.additional_cluster_config = self.test_config.integ_test.get("additional-cluster-configs")
            logging.info(f"Additional config found: {self.additional_cluster_config}")
        if self.additional_cluster_config is None:
            self.additional_cluster_config = {"cluster.name": "opensearch1"}
        with Topology.create(
            self.test_config.topology.cluster_configs,
            self.dependency_installer,
            self.work_dir,
            self.component.name,
            self.additional_cluster_config,
            self.bundle_manifest,
            security,
            config,
            self.test_recorder
        ) as (endpoints):
            os.chdir(self.work_dir)
            self.pretty_print_message("Running integration tests for " + self.component.name + " " + config)
            return self.multi_execute_integtest_sh(endpoints, security, config)

    def multi_execute_integtest_sh(self, cluster_endpoints: list, security: bool, test_config: str) -> int:
        script = ScriptFinder.find_integ_test_script(self.component.name, self.repo.working_directory)

        def custom_node_endpoint_encoder(node_endpoint: NodeEndpoint) -> dict:
            return {"endpoint": node_endpoint.endpoint, "port": node_endpoint.port, "transport": node_endpoint.transport}
        if os.path.exists(script):
            if len(cluster_endpoints) == 1:
                single_data_node = cluster_endpoints[0].data_nodes[0]
                cmd = f"bash {script} -b {single_data_node.endpoint} -p {single_data_node.port} -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            else:
                endpoints_list = []
                for cluster_details in cluster_endpoints:
                    endpoints_list.append(cluster_details.__dict__)
                endpoints_string = json.dumps(endpoints_list, indent=0, default=custom_node_endpoint_encoder).replace("\n", "")
                cmd = f"bash {script} -e '"
                cmd = cmd + endpoints_string + "'"
                cmd = cmd + f" -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            self.repo_work_dir = os.path.join(
                self.repo.dir, self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, self.repo_work_dir, True, False)
            test_result_data_local = TestResultData(
                self.component.name,
                test_config,
                status,
                stdout,
                stderr,
                self.test_artifact_files
            )
            self.save_logs.save_test_result_data(test_result_data_local)
            self.test_result_data.append(test_result_data_local)
            if stderr:
                logging.info("Stderr reported for component: " + self.component.name)
                logging.info(stderr)
            return status
        else:
            logging.info(f"{script} does not exist. Skipping integ tests for {self.component.name}")
            return 0

    @property
    def test_artifact_files(self) -> dict:
        return {
            "opensearch-integ-test": os.path.join(self.repo_work_dir, "build", "reports", "tests", "integTest")
        }
