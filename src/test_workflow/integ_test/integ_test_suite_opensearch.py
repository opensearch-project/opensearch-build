# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import logging
import os
from pathlib import Path
from typing import Any

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.integ_test.integ_test_suite import IntegTestSuite, InvalidTestConfigError
from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuiteOpenSearch(IntegTestSuite):
    dependency_installer: DependencyInstallerOpenSearch

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
        with LocalTestCluster.create(
            self.dependency_installer,
            self.work_dir,
            self.component.name,
            self.additional_cluster_config,
            self.bundle_manifest,
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
            "opensearch-integ-test": os.path.join(self.repo_work_dir, "build", "reports", "tests", "integTest")
        }
