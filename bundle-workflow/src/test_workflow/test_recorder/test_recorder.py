# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
from typing import Dict

import yaml

from test_workflow.test_recorder.test_recorder_builder import \
    TestRecorderBuilder


class Singleton(type):
    """Metaclass."""
    _instances: Dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            logging.info("TestRecorder is a singleton class, retrieving existing instance")
        return cls._instances[cls]

    def get_instance(cls):
        if cls._instances is not None:
            return cls._instances[cls]


class TestRecorder(object, metaclass=Singleton):
    ACCEPTABLE_TEST_TYPES = ["integ-test", "bwc-test", "perf-test"]

    def __init__(self, test_run_id, test_type, location):
        self.test_run_id = test_run_id
        self.test_type = test_type
        self.location = os.path.join(location, "test-recorder")
        logging.info(f"TestRecorder recording logs in {self.location}")
        if self.test_type not in self.ACCEPTABLE_TEST_TYPES:
            raise ValueError(
                f"{self.test_type} is not invalid. Accceptable test_type are {self.ACCEPTABLE_TEST_TYPES}")

    def record_cluster_logs(self, cluster_type, test_recorder_builder: TestRecorderBuilder):
        acceptable_cluster_type = ["remote", "local"]
        if cluster_type not in acceptable_cluster_type:
            raise ValueError(f"{cluster_type} is not invalid. Accceptable cluster_type are {acceptable_cluster_type}")
        base = self.__create_base_folder_structure(test_recorder_builder.component_name,
                                                   test_recorder_builder.component_test_config)
        folder_name = cluster_type + "-cluster-logs"
        dest_directory = os.path.join(base, folder_name)
        os.makedirs(dest_directory, exist_ok=False)
        logging.info(
            f"Recording {cluster_type} cluster logs for {test_recorder_builder.component_name} "
            f"with {test_recorder_builder.component_test_config} config in {os.path.realpath(dest_directory)}")
        self.__generate_std_files(test_recorder_builder.stdout, test_recorder_builder.stderr,
                                  os.path.realpath(dest_directory))
        if cluster_type == "local":
            local_cluster_log_files = list(test_recorder_builder.log_files)
            for log_file in local_cluster_log_files:
                dest_file = os.path.join(dest_directory, os.path.basename(log_file[0]))
                shutil.copyfile(log_file[0], dest_file)
        elif cluster_type == "remote":
            if test_recorder_builder.log_file_location is not None:
                exit_status = self.__get_exit_status(test_recorder_builder.exit_code)
                component_yml = self.__generate_yml(test_recorder_builder.component_name,
                                                    test_recorder_builder.component_test_config,
                                                    exit_status,
                                                    test_recorder_builder.log_file_location)
                shutil.copyfile(component_yml, os.path.join(dest_directory, os.path.basename(component_yml)))

    def record_test_outcome(self, test_recorder_builder: TestRecorderBuilder):
        base = self.__create_base_folder_structure(test_recorder_builder.component_name,
                                                   test_recorder_builder.component_test_config)
        dest_directory = os.path.join(base, "test-outcome")
        os.makedirs(dest_directory, exist_ok=False)
        logging.info(
            f"Recording component test results for {test_recorder_builder.component_name} at {os.path.realpath(dest_directory)}")
        self.__generate_std_files(test_recorder_builder.stdout, test_recorder_builder.stderr, dest_directory)
        if test_recorder_builder.log_files is not None:
            results_dir = list(test_recorder_builder.log_files)
            for result in results_dir:
                dest_file = os.path.join(dest_directory, os.path.basename(result[0]))
                shutil.copyfile(result[0], dest_file)
        exit_status = self.__get_exit_status(test_recorder_builder.exit_code)
        component_yml = self.__generate_yml(test_recorder_builder.component_name,
                                            test_recorder_builder.component_test_config, exit_status,
                                            test_recorder_builder.log_file_location)
        shutil.copyfile(component_yml, os.path.join(dest_directory, os.path.basename(component_yml)))

    def __create_base_folder_structure(self, component_name, component_test_config):
        dest_directory = os.path.join(self.location, "tests", str(self.test_run_id), self.test_type,
                                      str(component_name),
                                      str(component_test_config))
        os.makedirs(dest_directory, exist_ok=True)
        return os.path.realpath(dest_directory)

    def __generate_std_files(self, stdout, stderr, output_path):
        with open(os.path.join(output_path, "stdout.txt"), "w") as stdout_file:
            stdout_file.write(stdout)
        with open(os.path.join(output_path, "stderr.txt"), "w") as stderr_file:
            stderr_file.write(stderr)

    def __generate_yml(self, component_name, component_test_config, exit_status, log_file_location):
        outcome = {
            "test_type": self.test_type,
            "test_run_id": self.test_run_id,
            "component_name": component_name,
            "test_config": component_test_config,
            "status": exit_status,
            "log_file_location": log_file_location
        }
        with open("%s.yml" % component_name, "w") as file:
            yaml.dump(outcome, file)
        return os.path.realpath("%s.yml" % component_name)

    def __get_exit_status(self, exit_code):
        if exit_code == 0:
            return "SUCCESS"
        else:
            return "FAILED"
