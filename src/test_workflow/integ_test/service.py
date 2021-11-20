# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging

import requests
import time
from test_workflow.test_cluster import ClusterCreationException


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

    @abc.abstractmethod
    def terminate(self):
        """
        Terminate this service.
        """
        pass

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
