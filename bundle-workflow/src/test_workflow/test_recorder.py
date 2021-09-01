# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


class TestRecorder:
    def __init__(self, location):
        self.location = location
        print(f"TestRecorder storing results in {location}")

    def record_cluster_logs(self, log_files):
        """
        Record the test cluster logs.
        :param results: A generator that yields tuples containing test cluster log files, in the form (absolute_path, relative_path)
        """
        print(f"Recording log files: {list(log_files)}")

    def record_integ_test_outcome(
        self, component_name, exit_status, stdout, stderr, results
    ):
        """
        Record the outcome of a integration test run.
        :param component_name: The name of the component that ran tests.
        :param exit_code: One of SUCCESS, FAILED, ERROR. SUCCESS means the tests ran and all of them passed.
        FAILED means the tests ran and at least one failed. ERROR means the test suite did not run correctly.
        :param stdout: A string containing the stdout stream from the test process.
        :param stderr: A string containing the stderr stream from the test process.
        :param results: A generator that yields tuples containing test results files, in the form (absolute_path, relative_path).
        """
        print(
            f"Recording test results for {component_name}. Exit status: {exit_status}, stdout: {stdout}, stderr: {stderr}, results files: {results}"
        )
