# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import subprocess
from typing import Any

"""
This class is to check if the client (Mac or Linux) has the docker daemon running.
If the docker daemon is not running, the called shell script will try to bring up the docker daemon.
It retun 0 if the script runs without error.
"""


class DockerDaemonRunning:
    @staticmethod
    def is_container_daemon_running() -> Any:
        check_docker_bash = "./src/validation_docker_workflow/check_docker_daemon.sh"
        result = subprocess.call([check_docker_bash])
        return (result)
