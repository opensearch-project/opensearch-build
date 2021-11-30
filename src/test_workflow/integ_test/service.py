# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os
import time
from os import walk

import requests

from system.process import Process
from test_workflow.test_cluster import ClusterCreationException


class Service(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """

    def __init__(self, work_dir, version, security_enabled, additional_config, dependency_installer):
        self.work_dir = work_dir
        self.version = version
        self.security_enabled = security_enabled
        self.additional_config = additional_config
        self.dependency_installer = dependency_installer

        self.process_handler = Process()
        self.install_dir = ""

    @abc.abstractmethod
    def start(self):
        """
        Start a service.
        """
        pass

    def terminate(self):
        if not self.process_handler.started:
            logging.info("Process is not started")
            return

        self.return_code = self.process_handler.terminate()

        log_files = walk(os.path.join(self.install_dir, "logs"))

        return ServiceTerminationResult(self.return_code, self.process_handler.stdout_data, self.process_handler.stderr_data, log_files)

    def endpoint(self):
        return "localhost"

    @abc.abstractmethod
    def port(self):
        """
        Get the port that this service is listening on.
        """
        pass

    @abc.abstractmethod
    def get_service_response(self):
        """
        Get response from the service endpoint.
        """
        pass

    def service_alive(self):
        response = self.get_service_response()
        logging.info(f"{response.status_code}: {response.text}")
        if response.status_code == 200 and (('"status":"green"' in response.text) or ('"status":"yellow"' in response.text)):
            logging.info("Service is available")
            return True
        else:
            return False

    def wait_for_service(self):
        logging.info("Waiting for service to become available")

        for attempt in range(10):
            try:
                logging.info(f"Pinging service attempt {attempt}")
                if self.service_alive():
                    return
            except requests.exceptions.ConnectionError:
                logging.info("Service not available yet")
                logging.info("- stdout:")
                logging.info(self.process_handler.stdout_data)

                logging.info("- stderr:")
                logging.info(self.process_handler.stderr_data)

            time.sleep(10)
        raise ClusterCreationException("Cluster is not available after 10 attempts")


class ServiceTerminationResult:
    def __init__(self, return_code, stdout_data, stderr_data, log_files):
        self.return_code = return_code
        self.stdout_data = stdout_data
        self.stderr_data = stderr_data
        self.log_files = log_files
