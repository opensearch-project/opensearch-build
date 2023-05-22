# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
from typing import Any

import yaml

from paths.tree_walker import walk
from test_workflow.test_recorder.log_recorder import LogRecorder
from test_workflow.test_recorder.test_result_data import TestResultData


class TestRecorder:
    test_run_id: str
    test_type: str
    location: str
    local_cluster_logs: Any
    remote_cluster_logs: Any
    test_results_logs: Any

    def __init__(self, test_run_id: str, test_type: str, tests_dir: str, base_path: str = None) -> None:
        self.test_run_id = test_run_id
        self.test_type = test_type
        self.location = os.path.join(tests_dir, str(self.test_run_id), self.test_type)
        os.makedirs(self.location, exist_ok=True)
        logging.info(f"TestRecorder recording logs in {self.location}")
        self.local_cluster_logs = LocalClusterLogs(self)
        self.remote_cluster_logs = RemoteClusterLogs(self)
        self.test_results_logs = TestResultsLogs(self)
        self.base_path = base_path

    def _get_file_path(self, base_path: str, component_name: str, component_test_config: str) -> str:
        if base_path.startswith("https://"):
            file_path = "/".join([base_path.strip("/"), "test-results", str(self.test_run_id), self.test_type, component_name, component_test_config])
        else:
            file_path = self._create_base_folder_structure(component_name, component_test_config)
        return file_path

    def _create_base_folder_structure(self, component_name: str, component_test_config: str) -> str:
        dest_directory = os.path.join(self.location, component_name, component_test_config)
        os.makedirs(dest_directory, exist_ok=True)
        return os.path.realpath(dest_directory)

    def _generate_std_files(self, stdout: str, stderr: str, output_path: str) -> None:
        with open(os.path.join(output_path, "stdout.txt"), "w") as stdout_file:
            stdout_file.write(stdout)
        with open(os.path.join(output_path, "stderr.txt"), "w") as stderr_file:
            stderr_file.write(stderr)

    def _generate_yml(self, test_result_data: TestResultData, output_path: str) -> str:
        base_file_path = self._get_file_path(self.base_path, test_result_data.component_name, test_result_data.component_test_config)

        components_files = self._get_list_files(output_path)
        test_result_file = self._update_absolute_file_paths(components_files, base_file_path, "")

        outcome = {
            "test_type": self.test_type,
            "run_id": self.test_run_id,
            "component_name": test_result_data.component_name,
            "test_config": test_result_data.component_test_config,
            "test_result": "PASS" if (test_result_data.exit_code == 0) else "FAIL",
            "test_result_files": test_result_file
        }
        with open(os.path.join(output_path, "%s.yml" % test_result_data.component_name), "w") as file:
            yaml.dump(outcome, file)
        return os.path.realpath("%s.yml" % test_result_data.component_name)

    def _update_absolute_file_paths(self, files: list, base_path: str, relative_path: str) -> list:
        return [os.path.join(base_path, relative_path, file) for file in files]

    # get a list of files within directory with relative paths.
    def _get_list_files(self, dir: str) -> list:
        files = []
        for file_paths in walk(dir):
            files.append(file_paths[1])
        return files

    def _copy_log_files(self, log_files: dict, dest_directory: str) -> None:
        if log_files:
            for log_dest_dir_name, source_log_dir in log_files.items():
                if os.path.exists(source_log_dir):
                    dest_dir = os.path.join(dest_directory, log_dest_dir_name)
                    shutil.copytree(source_log_dir, dest_dir)


class LocalClusterLogs(LogRecorder):
    parent_class: TestRecorder

    def __init__(self, parent_class: TestRecorder) -> None:
        self.parent_class = parent_class

    def save_test_result_data(self, test_result_data: TestResultData) -> None:
        base = self.parent_class._create_base_folder_structure(test_result_data.component_name, test_result_data.component_test_config)
        dest_directory = os.path.join(base, "local-cluster-logs")
        os.makedirs(dest_directory, exist_ok=True)
        logging.info(
            f"Recording local cluster logs for {test_result_data.component_name} with test configuration as "
            f"{test_result_data.component_test_config} at {os.path.realpath(dest_directory)}"
        )
        self.parent_class._generate_std_files(
            test_result_data.stdout,
            test_result_data.stderr,
            os.path.realpath(dest_directory),
        )

        self.parent_class._copy_log_files(test_result_data.log_files, dest_directory)


class RemoteClusterLogs(LogRecorder):
    parent_class: TestRecorder

    def __init__(self, parent_class: TestRecorder) -> None:
        self.parent_class = parent_class

    def save_test_result_data(self, test_result_data: TestResultData) -> None:
        base = self.parent_class._create_base_folder_structure(test_result_data.component_name, test_result_data.component_test_config)
        dest_directory = os.path.join(base, "remote-cluster-logs")
        os.makedirs(dest_directory, exist_ok=True)
        logging.info(
            f"Recording remote cluster logs for {test_result_data.component_name} with test configuration as "
            f"{test_result_data.component_test_config} at {os.path.realpath(dest_directory)}"
        )
        self.parent_class._generate_yml(test_result_data, dest_directory)


class TestResultsLogs(LogRecorder):
    __test__ = False    # type:ignore
    parent_class: TestRecorder

    def __init__(self, parent_class: TestRecorder) -> None:
        self.parent_class = parent_class

    def save_test_result_data(self, test_result_data: TestResultData) -> None:
        dest_directory = self.parent_class._create_base_folder_structure(test_result_data.component_name, test_result_data.component_test_config)
        logging.info(f"Recording component test results for {test_result_data.component_name} at " f"{os.path.realpath(dest_directory)}")
        self.parent_class._generate_std_files(test_result_data.stdout, test_result_data.stderr, dest_directory)
        self.parent_class._copy_log_files(test_result_data.log_files, dest_directory)
        self.parent_class._generate_yml(test_result_data, dest_directory)


TestRecorder.__test__ = False  # type:ignore
