# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import subprocess
from subprocess import PIPE

"""
This class is to pull the artifact from the dockerHub.
If the image is currently existing at local, we want to remove it and download a fresh one as the artifact may have been renewed at hub.
"""


class PullDockerImage():
    @staticmethod
    def pull_image(image_name):
        local_inspect = "docker image inspect -f '{{ .Id }}' " + image_name
        local_remove = "docker image rm -f " + image_name
        dockerHub_pull = "docker pull " + image_name

        # Removing the image if it exists at local
        result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if (result_inspect.returncode == 0):
            logging.info('Image exists at local : ' + result_inspect.stdout + ' : ' + image_name)
            logging.info('removing the local image and pulling a fresh one from DockerHub')
            result_remove = subprocess.run(local_remove, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            if (result_remove.returncode == 0):
                logging.info('Image is removed at local : ' + image_name)
            else:
                logging.info('Image removal fail : return code ' + result_remove.returncode)
        else:
            logging.info('Image does not exist at local, proceed with pull from the dockerHub')

        # Pulling image from dockerHub and return the image Id
        logging.info('Pulling ' + image_name + ' from the dockerHub')
        result_pull = subprocess.run(dockerHub_pull, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if (result_pull.returncode == 0):
            result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            logging.info('Image is pulled at local : ' + result_inspect.stdout + ' : ' + image_name)
            return (result_inspect.stdout)
