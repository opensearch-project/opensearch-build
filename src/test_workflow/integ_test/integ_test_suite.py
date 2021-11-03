# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import logging
import os

from git.git_repository import GitRepository
from paths.script_finder import ScriptFinder
from paths.tree_walker import walk
from system.execute import execute
from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class IntegTestSuite:
    """
    Kicks of integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(
        self,
        dependency_installer,
        component,
        test_config,
        bundle_manifest,
        build_manifest,
        work_dir,
        test_recorder
    ):
        self.dependency_installer = dependency_installer
        self.component = component
        self.bundle_manifest = bundle_manifest
        self.build_manifest = build_manifest
        self.work_dir = work_dir
        self.test_config = test_config
        self.additional_cluster_config = None
        self.test_recorder = test_recorder
        self.repo = GitRepository(
            self.component.repository,
            self.component.commit_id,
            os.path.join(self.work_dir, self.component.name),
            test_config.working_directory
        )
        self.save_logs = test_recorder.test_results_logs

    def execute(self):
        test_results = TestComponentResults()
        self.__install_build_dependencies()
        for config in self.test_config.integ_test["test-configs"]:
            status = self.__setup_cluster_and_execute_test_config(config)
            test_results.append(TestResult(self.component.name, config, status))
        return test_results

    def __install_build_dependencies(self):
        if "build-dependencies" in self.test_config.integ_test:
            dependency_list = self.test_config.integ_test["build-dependencies"]
            if len(dependency_list) == 1 and "job-scheduler" in dependency_list:
                self.__copy_job_scheduler_artifact()
            else:
                raise InvalidTestConfigError("Integration test job only supports job-scheduler build dependency at present.")

    def __copy_job_scheduler_artifact(self):
        custom_local_path = os.path.join(self.repo.dir, "src", "test", "resources", "job-scheduler")
        for file in glob.glob(os.path.join(custom_local_path, "opensearch-job-scheduler-*.zip")):
            os.unlink(file)
        job_scheduler = self.build_manifest.components["job-scheduler"]
        self.dependency_installer.install_build_dependencies({"opensearch-job-scheduler": job_scheduler.version}, custom_local_path)

    @staticmethod
    def __is_security_enabled(config):
        if config in ["with-security", "without-security"]:
            return True if config == "with-security" else False
        else:
            raise InvalidTestConfigError("Unsupported test config: " + config)

    def __setup_cluster_and_execute_test_config(self, config):
        security = self.__is_security_enabled(config)
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
        ) as (test_cluster_endpoint, test_cluster_port):
            self.__pretty_print_message("Running integration tests for " + self.component.name)
            os.chdir(self.work_dir)
            return self.__execute_integtest_sh(test_cluster_endpoint, test_cluster_port, security, config)

    def __execute_integtest_sh(self, endpoint, port, security, test_config):
        script = ScriptFinder.find_integ_test_script(self.component.name, self.repo.working_directory)
        if os.path.exists(script):
            cmd = f"{script} -b {endpoint} -p {port} -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            work_dir = os.path.join(self.repo.dir, self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, work_dir, True, False)
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

    @staticmethod
    def __pretty_print_message(message):
        logging.info("===============================================")
        logging.info(message)
        logging.info("===============================================")


class InvalidTestConfigError(Exception):
    pass
