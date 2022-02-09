# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import abc
import logging
import os

from git.git_repository import GitRepository
from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult


class BwcTestSuite(abc.ABC):

    def __init__(
        self,
        work_dir,
        component,
        test_config,
        test_recorder,
        manifest
    ):
        self.work_dir = work_dir
        self.component = component
        self.test_config = test_config
        self.test_recorder = test_recorder
        self.manifest = manifest

        self.repo = GitRepository(
            self.component.repository,
            self.component.commit_id,
            os.path.join(self.work_dir, self.component.name),
            test_config.working_directory
        )

        self.save_logs = test_recorder.test_results_logs

    def execute_tests(self):
        test_results = TestComponentResults()

        for config in self.test_config.bwc_test["test-configs"]:
            status = self.execute_bwctest_sh(config)

            test_results.append(TestResult(self.component.name, config, status))
        return test_results

    def execute_bwctest_sh(self, config):
        security = self.is_security_enabled(config)
        script = ScriptFinder.find_bwc_test_script(self.component.name, self.repo.working_directory)
        if os.path.exists(script):
            cmd = self.get_cmd(script, security, self.manifest.build.location)
            self.repo_work_dir = os.path.join(
                self.repo.dir, self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, self.repo_work_dir, True, False)

            test_result_data = TestResultData(
                self.component.name,
                self.test_config,
                status,
                stdout,
                stderr,
                self.test_artifact_files
            )
            self.save_logs.save_test_result_data(test_result_data)
            if stderr:
                logging.info("BWC test run failed for component " + self.component.name)
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

    @abc.abstractmethod
    def get_cmd(self):
        pass

    @property
    @abc.abstractmethod
    def test_artifact_files(self):
        pass


class InvalidTestConfigError(Exception):
    pass
