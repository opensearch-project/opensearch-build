# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os
import time

import requests

from system.process import Process
from test_workflow.test_cluster import ClusterCreationException


class Service(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """

    def __init__(self, work_dir, filename, version, distribution, security_enabled, additional_config, dependency_installer):
        self.filename = filename
        self.work_dir = work_dir
        self.version = version
        self.distribution = distribution
        self.security_enabled = security_enabled
        self.additional_config = additional_config
        self.dependency_installer = dependency_installer

        self.process_handler = Process(self.filename, self.distribution)
        self.install_dir_map = {
            "tar": os.path.join(self.work_dir, f"{self.filename}-{self.version}"),
            "rpm": os.path.join(os.sep, "usr", "share", self.filename)
        }
        self.config_file_map = {
            "tar": os.path.join(self.install_dir_map[self.distribution], "config", f"{self.filename.replace('-', '_')}.yml"),
            "rpm": os.path.join(os.sep, "etc", self.filename, f"{self.filename.replace('-', '_')}.yml")
        }
        self.start_cmd_map = {
            "tar-opensearch": "./opensearch-tar-install.sh",
            "tar-opensearch-dashboards": "./opensearch-dashboards",
            "rpm-opensearch": "systemctl start opensearch",
            "rpm-opensearch-dashboards": "systemctl start opensearch-dashboards"
        }
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

        return ServiceTerminationResult(self.return_code, self.process_handler.stdout_data, self.process_handler.stderr_data, self.log_files)

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

    @abc.abstractmethod
    def check_service_response_text(self):
        """
        Check response text from the service endpoint.
        """
        pass

    def service_alive(self):
        response = self.get_service_response()
        logging.info(f"{response.status_code}: {response.text}")

        # TODO: https://github.com/opensearch-project/opensearch-build/issues/1217
        if response.status_code == 200 and self.check_service_response_text(response.text):
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
                logging.info("Service not available, yet")
                stdout = self.process_handler.stdout_data
                if stdout:
                    logging.info("- stdout:\n{stdout}")
                stderr = self.process_handler.stderr_data
                if stderr:
                    logging.info("- stderr:\n{stderr}")
            time.sleep(10)
        raise ClusterCreationException("Cluster is not available after 10 attempts")

    @property
    @abc.abstractmethod
    def log_files(self):
        pass


class ServiceTerminationResult:
    def __init__(self, return_code, stdout_data, stderr_data, log_files):
        self.return_code = return_code
        self.stdout_data = stdout_data
        self.stderr_data = stderr_data
        self.log_files = log_files
