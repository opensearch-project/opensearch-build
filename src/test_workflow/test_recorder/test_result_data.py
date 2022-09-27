# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from dataclasses import dataclass


@dataclass
class TestResultData:
    """
    Class that will hold all the required params for test_recorder module
    Record the test cluster logs.
    component_name: Name of the component that is being tested.
    component_test_config: component_config under consideration for test eg: with/without-security.
    exit_code: An exit code in the form of an integer
    stdout: A string containing the stdout stream from the test process.
    stderr: A string containing the stderr stream from the test process.
    log_files: A generator that yields tuples containing test cluster log files, in the form (absolute_path, relative_path).
    """

    component_name: str
    component_test_config: str
    exit_code: int
    stdout: str
    stderr: str
    log_files: dict
