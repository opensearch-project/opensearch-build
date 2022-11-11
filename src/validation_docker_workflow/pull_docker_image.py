# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import subprocess
from subprocess import PIPE
from typing import Any

"""
This class is to pull the artifact from the dockerHub.
If the image is currently existing at local, we want to remove it and download a fresh one as the artifact may have been renewed at hub.
"""


class PullDockerImage():

    @classmethod
    def pull_image(self, image_name: str, image_version: str) -> Any:
        local_inspect = "docker image inspect -f '{{ .Id }}' " + image_name + ":" + image_version
        local_remove = "docker image rm -f " + image_name + ":" + image_version
        dockerHub_pull = "docker pull " + image_name + ":" + image_version

        try:
            result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            logging.info('Image exists at local : ' + result_inspect.stdout + ' : ' + image_name + ":" + image_version)
            logging.info('removing the local image and pulling a fresh one from DockerHub')
            try:
                subprocess.run(local_remove, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                logging.info('Image is removed at local : ' + image_name + ":" + image_version)
            except (RuntimeError, TypeError, NameError):
                logging.info("Error: Fatil to remove image")
        except (RuntimeError, TypeError, NameError):
            logging.info("Error: Fail to inspect image")
        finally:
            logging.info('Proceed with pulling from the dockerHub')

        try:
            subprocess.run(dockerHub_pull, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            try:
                result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                logging.info('Image is pulled at local : ' + result_inspect.stdout + ' : ' + image_name + ":" + image_version)
                return (result_inspect.stdout)
            except (RuntimeError, TypeError, NameError):
                logging.info("Error: Fail to inspect image")
        except (RuntimeError, TypeError, NameError):
            logging.info("Error: Fail to pull image")
