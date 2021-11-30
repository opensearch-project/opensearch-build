# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from paths.script_finder import ScriptFinder
from paths.tree_walker import walk
from system.execute import execute
from test_workflow.integ_test.integ_test_suite import IntegTestSuite
from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuiteOpenSearchDashboards(IntegTestSuite):
    """
    Kicks of integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

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
        # self.__install_build_dependencies()
        for config in self.test_config.integ_test["test-configs"]:
            status = self.__setup_cluster_and_execute_test_config(config)

            logging.info(f"__setup_cluster_and_execute_test_config status is {status}")
            test_results.append(TestResult(self.component.name, config, status))
        return test_results

    def __setup_cluster_and_execute_test_config(self, config):
        security = self.is_security_enabled(config)
        # if "additional-cluster-configs" in self.test_config.integ_test.keys():
        #     self.additional_cluster_config = self.test_config.integ_test.get("additional-cluster-configs")
        #     logging.info(f"Additional config found: {self.additional_cluster_config}")
        with LocalTestClusterOpenSearchDashboards.create(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component.name,
            {},
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            security,
            config,
            self.test_recorder,
        ) as (test_cluster_endpoint, test_cluster_port):
            self.pretty_print_message("Running integration tests for " + self.component.name)
            os.chdir(self.work_dir)
            return self.__execute_integtest_sh(test_cluster_endpoint, test_cluster_port, security, config)

    def __execute_integtest_sh(self, endpoint, port, security, test_config):
        script = ScriptFinder.find_integ_test_script(self.component.name, self.repo.working_directory)
        if os.path.exists(script):
            cmd = f"{script} -b {endpoint} -p {port} -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            work_dir = os.path.join(self.repo.dir, self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, work_dir, True, False)

            logging.info(f"status,  is {status}")
            logging.info(f"stdout is {stdout}")

            logging.info(f"stderr is {stderr}")

            results_dir = os.path.join(work_dir, "build", "reports", "tests", "integTest")
            test_result_data = TestResultData(
                self.component.name,
                test_config,
                status,
                stdout,
                stderr,
                walk(results_dir)
            )
            self.save_logs.save_test_result_data(test_result_data)
            if stderr:
                logging.info("Integration test run failed for component " + self.component.name)
                logging.info(stderr)
            return status
        else:
            logging.info(f"{script} does not exist. Skipping integ tests for {self.name}")
