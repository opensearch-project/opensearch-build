# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from dataclasses import dataclass


@dataclass
class TestRecorderBuilder:
    """
    Class that will hold all the required params for test_recorder module
    Record the test cluster logs.
    component_name: component that is under test right now.
    component_test_config: component_config under consideration for test eg: with/without-security.
    exit_code: int
    stdout: A string containing the stdout stream from the test process.
    stderr: A string containing the stderr stream from the test process.
    log_files: A generator that yields tuples containing test cluster log files, in the form (absolute_path, relative_path).
    log_file_location: str = None
    """
    component_name: str
    component_test_config: str
    exit_code: int
    stdout: str
    stderr: str
    log_files: tuple = None
    log_file_location: str = None

