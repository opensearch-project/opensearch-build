# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import logging
import os
import shutil
import tempfile

import yaml


class TestRecorder:
    ACCEPTED_TEST_TYPES = ["integ-test", "bwc-test", "perf-test"]

    def __init__(self, test_run_id, test_type, location=None):
        self.test_type = test_type
        self.test_run_id = test_run_id

        if self.test_type not in self.ACCEPTED_TEST_TYPES:
            raise ValueError(f"test_type is invalid. Acceptable test_type are {self.ACCEPTED_TEST_TYPES}")

        if location is None:
            location = tempfile.TemporaryDirectory()
            self.location = location.name
        else:
            self.location = location
        logging.info(f'TestRecorder storing results in {os.path.realpath(self.location)}')

    def record_local_cluster_logs(self, component_name, component_test_config, stdout, stderr, log_files):
        """
        Record the test cluster logs.
        :param component_name: component that is under test right now.
        :param component_test_config: component_config under consideration for test eg: with/without-security.
        :param stdout: A string containing the stdout stream from the test process.
        :param stderr: A string containing the stderr stream from the test process.
        :param log_files: A generator that yields tuples containing test cluster log files, in the form (absolute_path, relative_path).
        """

        base = self.__create_base_folder_structure(component_name, component_test_config)
        dest_directory = os.path.join(base, "local_cluster_logs")
        os.makedirs(dest_directory, exist_ok=False)
        logging.info(
            f"Recording local cluster logs for {component_name} with {component_test_config} config in {os.path.realpath(dest_directory)}")
        self.__generate_std_files(stdout, stderr, os.path.realpath(dest_directory))
        local_cluster_log_files = list(log_files)
        print(f"Log files are: {local_cluster_log_files}")
        for log_file in local_cluster_log_files:
            dest_file = os.path.join(dest_directory, os.path.basename(log_file[0]))
            shutil.copyfile(log_file[0], dest_file)

    def record_remote_cluster_logs(self, component_name, component_test_config, exit_code, stdout, stderr,
                                   log_file_location, results):
        """
        Record the test cluster logs.
        :param component_name: component that is under test right now.
        :param exit_code: Integer value of the exit code.
        :param stdout: A string containing the stdout stream from the test process.
        :param stderr: A string containing the stderr stream from the test process.
        :param component_test_config: component_config under consideration for test eg: with/without-security.
        :param log_file_location: A string that gives log file location.
        :param results: A generator that yields tuples containing test results files, in the form (absolute_path, relative_path).
        """

        base = self.__create_base_folder_structure(component_name, component_test_config)
        dest_directory = os.path.join(base, "remote_cluster_logs")
        os.makedirs(dest_directory, exist_ok=False)
        logging.info(f"Recording remote cluster logs for {component_name} in {os.path.realpath(dest_directory)}")
        self.__generate_std_files(stdout, stderr, os.path.realpath(dest_directory))
        exit_status = self.__get_exit_status(exit_code)
        component_yml = self.__generate_test_outcome_yml(component_name, component_test_config, exit_status,
                                                         log_file_location)
        shutil.copyfile(component_yml, os.path.join(dest_directory, os.path.basename(component_yml)))
        results_dir = list(results)
        for result in results_dir:
            dest_file = os.path.join(dest_directory, os.path.basename(result[0]))
            shutil.copyfile(result[0], dest_file)

    def record_test_outcome(
            self, component_name, component_test_config, exit_code, stdout, stderr, results
    ):
        """
        Record the outcome of a integration test run.
        :param component_name: The name of the component that ran tests.
        :param component_test_config: component_config under consideration for test eg: with/without-security.
        :param exit_code: Integer value of the exit code.
        :param stdout: A string containing the stdout stream from the test process.
        :param stderr: A string containing the stderr stream from the test process.
        :param results: A generator that yields tuples containing test results files, in the form (absolute_path, relative_path).
        """

        base = self.__create_base_folder_structure(component_name, component_test_config)
        dest_directory = os.path.join(base, "test_outcome")
        os.makedirs(dest_directory, exist_ok=False)
        logging.info(
            f"Recording component test results for {component_name} at {os.path.realpath(dest_directory)}")
        self.__generate_std_files(stdout, stderr, dest_directory)
        results_dir = list(results)
        for result in results_dir:
            dest_file = os.path.join(dest_directory, os.path.basename(result[0]))
            shutil.copyfile(result[0], dest_file)
        exit_status = self.__get_exit_status(exit_code)
        component_yml = self.__generate_test_outcome_yml(component_name, component_test_config, exit_status, "S3")
        shutil.copyfile(component_yml, os.path.join(dest_directory, os.path.basename(component_yml)))

    def __create_base_folder_structure(self, component_name, component_test_config):
        dest_directory = os.path.join(self.location, "tests", self.test_run_id, self.test_type, str(component_name),
                                      str(component_test_config))
        os.makedirs(dest_directory, exist_ok=True)
        return os.path.realpath(dest_directory)

    def __get_exit_status(self, exit_code):
        if exit_code == 0:
            return "SUCCESS"
        else:
            return "FAILED/ERROR"

    def __generate_test_outcome_yml(self, component_name, component_test_config, exit_status, log_file_location):
        dict_file = {
            "test_type": self.test_type,
            "test_run_id": self.test_run_id,
            "component_name": component_name,
            "test_config": component_test_config,
            "status": exit_status,
            "log_file_location": log_file_location
        }
        with open("%s.yml" % component_name, "w") as file:
            yaml.dump(dict_file, file)
        return os.path.realpath("%s.yml" % component_name)

    def __generate_std_files(self, stdout, stderr, location):
        stdout_file = open(os.path.join(location, "stdout.txt"), "w")
        stderr_file = open(os.path.join(location, "stderr.txt"), "w")
        try:
            stdout_file.write(stdout)
            stderr_file.write(stderr)
        finally:
            stdout_file.close()
            stderr_file.close()

    def cleanup(self):
        if self.location:
            logging.info(f"Removing the {os.path.realpath(self.location)} directory")
            os.remove(os.path.realpath(self.location))
