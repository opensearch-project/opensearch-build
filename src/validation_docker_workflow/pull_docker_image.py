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
                result_remove = subprocess.run(local_remove, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                logging.info('Image is removed at local : ' + image_name + ":" + image_version)
            except (RuntimeError, TypeError, NameError) as e:
                logging.info("Error: %s - %s." % (e.strerror))
        except (RuntimeError, TypeError, NameError) as e:
            logging.info("Error: %s - %s." % (e.strerror))
        finally:
            logging.info('Proceed with pulling from the dockerHub')

        # Pulling image from dockerHub and return the image Id
        # logging.info('Pulling ' + image_name + ":" + image_version + ' from the dockerHub')
        # result_pull = subprocess.run(dockerHub_pull, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        # if (result_pull.returncode == 0):
        #     result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        #     logging.info('Image is pulled at local : ' + result_inspect.stdout + ' : ' + image_name + ":" + image_version)
        #     return (result_inspect.stdout)
        # else:
        #     return ('error on pulling image : return code ' + str(result_remove.returncode))
        try:
            result_pull = subprocess.run(dockerHub_pull, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            try:
                result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                logging.info('Image is pulled at local : ' + result_inspect.stdout + ' : ' + image_name + ":" + image_version)
                return (result_inspect.stdout)
            except (RuntimeError, TypeError, NameError) as e:
                logging.info("Error: %s - %s." % (e.strerror))
        except (RuntimeError, TypeError, NameError) as e:
            logging.info("Error: %s - %s." % (e.strerror))
