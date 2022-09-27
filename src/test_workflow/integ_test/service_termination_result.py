# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Dict


class ServiceTerminationResult:
    return_code: int
    stdout_data: str
    stderr_data: str
    log_files: Dict[str, str]

    def __init__(
        self,
        return_code: int,
        stdout_data: str,
        stderr_data: str,
        log_files: Dict[str, str]
    ) -> None:
        self.return_code = return_code
        self.stdout_data = stdout_data
        self.stderr_data = stderr_data
        self.log_files = log_files
