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

from test_workflow.test_cluster import ClusterCreationException
from test_workflow.test_recorder.test_result_data import TestResultData


class Service(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """

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

        self.__test_result_data()

    def __test_result_data(self):
        log_files = walk(os.path.join(self.install_dir, "logs"))
        test_result_data = TestResultData(
            self.component_name, self.component_test_config, self.return_code, self.process_handler.stdout_data, self.process_handler.stderr_data, log_files
        )
        self.save_logs.save_test_result_data(test_result_data)

    @abc.abstractmethod
    def endpoint(self):
        """
        Get the endpoint that this service is listening on, e.g. 'localhost' or 'some.ip.address'.
        """
        pass

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
        if response.status_code == 200 and ('"status":"green"' or '"status":"yellow"' in response.text):
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
