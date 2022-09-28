# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import os
from contextlib import contextmanager
from typing import Any, Generator, List, Tuple

from test_workflow.integ_test.service import Service
from test_workflow.integ_test.service_termination_result import ServiceTerminationResult
from test_workflow.test_recorder.log_recorder import LogRecorder
from test_workflow.test_recorder.test_result_data import TestResultData


class TestCluster(abc.ABC):
    work_dir: str
    component_name: str
    component_test_config: str
    security_enabled: bool
    additional_cluster_config: dict
    save_logs: LogRecorder
    all_services: List[Service]
    termination_result: ServiceTerminationResult

    """
    Abstract base class for all types of test clusters.
    """

    def __init__(
        self,
        work_dir: str,
        component_name: str,
        component_test_config: str,
        security_enabled: bool,
        additional_cluster_config: dict,
        save_logs: LogRecorder
    ) -> None:
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
    def create(cls, *args: Any) -> Generator[Tuple[str, int], None, None]:
        """
        Set up the cluster. When this method returns, the cluster must be available to take requests.
        Throws ClusterCreationException if the cluster could not start for some reason. If this exception is thrown, the caller does not need to call "destroy".
        """
        cluster = cls(*args)
        try:
            cluster.start()
            yield cluster.endpoint, cluster.port
        finally:
            cluster.terminate()

    def start(self) -> None:
        os.makedirs(self.work_dir, exist_ok=True)

        self.all_services = [self.service] + self.dependencies

        for service in self.all_services:
            service.start()

        for service in self.all_services:
            service.wait_for_service()

    def terminate(self) -> None:
        if self.service:
            self.termination_result = self.service.terminate()

        for service in self.dependencies:
            termination_result = service.terminate()
            self.__save_test_result_data(termination_result)

        if not self.termination_result:
            raise ClusterServiceNotInitializedException()

        self.__save_test_result_data(self.termination_result)

    def __save_test_result_data(self, termination_result: ServiceTerminationResult) -> None:
        test_result_data = TestResultData(
            self.component_name,
            self.component_test_config,
            termination_result.return_code,
            termination_result.stdout_data,
            termination_result.stderr_data,
            termination_result.log_files
        )

        self.save_logs.save_test_result_data(test_result_data)

    @property
    def endpoint(self) -> str:
        """
        Get the host that this cluster is listening on.
        """
        return "localhost"

    @property
    @abc.abstractmethod
    def port(self) -> int:
        """
        Get the port that this cluster is listening on.
        """
        pass

    @property
    @abc.abstractproperty
    def service(self) -> Service:
        """
        The main service running in this cluster.
        """
        pass

    @abc.abstractproperty
    def dependencies(self) -> List[Service]:
        """
        The dependencies running in this cluster.
        """
        pass


class ClusterServiceNotInitializedException(Exception):
    """
    Indicates that the service running in the cluster is not initialized.
    """

    def __init__(self) -> None:
        super().__init__("Service is not initialized")
