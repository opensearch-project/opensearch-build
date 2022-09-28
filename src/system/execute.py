# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import subprocess
from typing import Any, Tuple


def execute(command: str, dir: str, capture: bool = True, raise_on_failure: bool = True) -> Tuple[int, Any, Any]:
    """
    Execute a shell command inside a directory.
    :param capture:
    :param raise_on_failure:
    :param command: The shell command to execute.
    :param dir: The full path to the directory that the command should be executed in.
    :returns a tuple containing the exit code, stdout, and stderr.
    """
    logging.info(f'Executing "{command}" in {dir}')
    result = subprocess.run(command, cwd=dir, shell=True, capture_output=capture, text=True)
    if raise_on_failure:
        result.check_returncode()
    return result.returncode, result.stdout, result.stderr
