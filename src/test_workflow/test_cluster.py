# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import os
from contextlib import contextmanager

from test_workflow.test_recorder.test_result_data import TestResultData


class TestCluster(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """

    def __init__(
        self,
        work_dir,
        component_name,
        component_test_config,
        security_enabled,
        additional_cluster_config,
        save_logs
    ):
        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        self.component_name = component_name
        self.component_test_config = component_test_config
        self.security_enabled = security_enabled
        self.additional_cluster_config = additional_cluster_config
        self.save_logs = save_logs

        self.all_services = []
        self.termination_result = None

    @classmethod
    @contextmanager
    def create(cls, *args):
        """
        Set up the cluster. When this method returns, the cluster must be available to take requests.
        Throws ClusterCreationException if the cluster could not start for some reason. If this exception is thrown, the caller does not need to call "destroy".
        """
        cluster = cls(*args)
        try:
            cluster.start()
            yield cluster.endpoint(), cluster.port()
        finally:
            cluster.terminate()

    def start(self):
        os.makedirs(self.work_dir, exist_ok=True)

        self.all_services = [self.service] + self.dependencies

        for service in self.all_services:
            service.start()

        for service in self.all_services:
            service.wait_for_service()

    def terminate(self):
        if self.service:
            self.termination_result = self.service.terminate()

        for service in self.dependencies:
            service.terminate()

        if not self.termination_result:
            raise ClusterServiceNotInitializedException()

        self.__save_test_result_data()

    def __save_test_result_data(self):

        test_result_data = TestResultData(
            self.component_name,
            self.component_test_config,
            self.termination_result.return_code,
            self.termination_result.stdout_data,
            self.termination_result.stderr_data,
            self.termination_result.log_files
        )

        self.save_logs.save_test_result_data(test_result_data)

    def endpoint(self):
        return "localhost"

    @abc.abstractmethod
    def port(self):
        """
        Get the port that this cluster is listening on.
        """
        pass

    @abc.abstractproperty
    def service(self):
        """
        The main service running in this cluster.
        """
        pass

    @abc.abstractproperty
    def dependencies(self):
        """
        The dependencies running in this cluster.
        """
        pass


class ClusterCreationException(Exception):
    """
    Indicates that cluster creation failed for some reason.
    """

    pass


class ClusterServiceNotInitializedException(Exception):
    """
    Indicates that the service running in the cluster is not initialized.
    """

    def __init__(self):
        super().__init__("Service is not initialized")
