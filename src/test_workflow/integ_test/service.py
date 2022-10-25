# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os
import time
from typing import Dict

import requests
from requests.models import Response

from system.process import Process
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.service_termination_result import ServiceTerminationResult


class Service(abc.ABC):
    work_dir: str
    version: str
    distribution: str
    security_enabled: bool
    additional_config: dict
    dependency_installer: DependencyInstaller

    """
    Abstract base class for all types of test clusters.
    """

    def __init__(
        self,
        work_dir: str,
        version: str,
        distribution: str,
        security_enabled: bool,
        additional_config: dict,
        dependency_installer: DependencyInstaller
    ) -> None:
        self.work_dir = work_dir
        self.version = version
        self.distribution = distribution
        self.security_enabled = security_enabled
        self.additional_config = additional_config
        self.dependency_installer = dependency_installer

        self.process_handler = Process()
        self.install_dir = ""

    @abc.abstractmethod
    def start(self) -> None:
        """
        Start a service.
        """
        pass

    def terminate(self) -> ServiceTerminationResult:
        if not self.process_handler.started:
            logging.info("Process is not started")
            return None

        self.return_code = self.process_handler.terminate()

        self.uninstall()

        return ServiceTerminationResult(
            self.return_code,
            self.process_handler.stdout_data,
            self.process_handler.stderr_data,
            self.log_files
        )

    def endpoint(self) -> str:
        return "localhost"

    @abc.abstractmethod
    def port(self) -> int:
        """
        Get the port that this service is listening on.
        """
        pass

    @abc.abstractmethod
    def get_service_response(self) -> Response:
        """
        Get response from the service endpoint.
        """
        pass

    @abc.abstractmethod
    def check_service_response_text(self, response_text: str) -> bool:
        """
        Check response text from the service endpoint.
        """
        pass

    def service_alive(self) -> bool:
        response = self.get_service_response()
        logging.info(f"{response.status_code}: {response.text}")

        # TODO: https://github.com/opensearch-project/opensearch-build/issues/1217
        if response.status_code == 200 and self.check_service_response_text(response.text):
            logging.info("Service is available")
            return True
        else:
            return False

    def download(self) -> str:
        logging.info("Downloading bundle artifact")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")
        return bundle_name

    def wait_for_service(self) -> None:
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
    def log_files(self) -> Dict[str, str]:
        pass

    @abc.abstractmethod
    def uninstall(self) -> None:
        pass


class ClusterCreationException(Exception):
    """
    Indicates that cluster creation failed for some reason.
    """

    pass
