# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os

from git.git_repository import GitRepository
from paths.script_finder import ScriptFinder
from paths.tree_walker import walk
from system.execute import execute
from test_workflow.test_recorder.test_result_data import TestResultData


class IntegTestSuite(abc.ABC):
    """
    Kicks off integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(
        self,
        work_dir,
        component,
        test_config,
        test_recorder,
        dependency_installer,
        bundle_manifest,
        build_manifest
    ):
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
    def execute_tests(self):
        pass

    def execute_integtest_sh(self, endpoint, port, security, test_config):
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
            logging.info(f"{script} does not exist. Skipping integ tests for {self.component.name}")

    def is_security_enabled(self, config):
        if config in ["with-security", "without-security"]:
            return True if config == "with-security" else False
        else:
            raise InvalidTestConfigError("Unsupported test config: " + config)

    def pretty_print_message(self, message):
        logging.info("===============================================")
        logging.info(message)
        logging.info("===============================================")


class InvalidTestConfigError(Exception):
    pass
