# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.topology import ClusterEndpoint, NodeEndpoint
from test_workflow.test_recorder.log_recorder import LogRecorder
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults


class IntegTestSuite(abc.ABC):
    work_dir: Path
    component: Any
    test_config: Any
    test_recorder: TestRecorder
    dependency_installer: DependencyInstaller
    bundle_manifest: BundleManifest
    build_manifest: BuildManifest
    repo: GitRepository
    save_logs: LogRecorder
    additional_cluster_config: dict

    """
    Kicks off integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(
        self,
        work_dir: Path,
        component: Any,
        test_config: Any,
        test_recorder: TestRecorder,
        dependency_installer: DependencyInstaller,
        bundle_manifest: BundleManifest,
        build_manifest: BuildManifest
    ) -> None:
        self.work_dir = work_dir
        self.component = component
        self.test_config = test_config
        self.test_recorder = test_recorder

        self.dependency_installer = dependency_installer
        self.bundle_manifest = bundle_manifest
        self.build_manifest = build_manifest

        self.repo = GitRepository(
            self.component.repository,
            self.component.commit_id,
            os.path.join(self.work_dir, self.component.name),
            test_config.working_directory
        )

        self.save_logs = test_recorder.test_results_logs
        self.additional_cluster_config = None

    @abc.abstractmethod
    def execute_tests(self) -> TestComponentResults:
        pass

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
                endpoints_string = json.dumps(endpoints_list, indent=0, default=custom_node_endpoint_encoder)
                cmd = f"bash {script} -e '"
                cmd = cmd + endpoints_string + "'"
                cmd = cmd + f" -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            self.repo_work_dir = os.path.join(
                self.repo.dir, self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, self.repo_work_dir, True, False)
            test_result_data = TestResultData(
                self.component.name,
                test_config,
                status,
                stdout,
                stderr,
                self.test_artifact_files
            )
            self.save_logs.save_test_result_data(test_result_data)
            if stderr:
                logging.info("Integration test run failed for component " + self.component.name)
                logging.info(stderr)
            return status
        else:
            logging.info(f"{script} does not exist. Skipping integ tests for {self.component.name}")
            return 0

    def execute_integtest_sh(self, endpoint: str, port: int, security: bool, test_config: str) -> int:
        cluster_endpoint_port = [ClusterEndpoint("cluster1", [NodeEndpoint(endpoint, port, 9300)], [])]
        return self.multi_execute_integtest_sh(cluster_endpoint_port, security, test_config)

    def is_security_enabled(self, config: str) -> bool:
        if config in ["with-security", "without-security"]:
            return True if config == "with-security" else False
        else:
            raise InvalidTestConfigError("Unsupported test config: " + config)

    def pretty_print_message(self, message: str) -> None:
        logging.info("===============================================")
        logging.info(message)
        logging.info("===============================================")

    @property
    @abc.abstractmethod
    def test_artifact_files(self) -> Dict[str, str]:
        pass


class InvalidTestConfigError(Exception):
    pass
