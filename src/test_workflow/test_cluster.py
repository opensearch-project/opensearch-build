# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
from contextlib import contextmanager


class TestCluster(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """

    @classmethod
    @contextmanager
    def create(cls, *args):
        """
        Set up the cluster. When this method returns, the cluster must be available to take requests.
        Throws ClusterCreationException if the cluster could not start for some reason. If this exception is thrown, the caller does not need to call "destroy".
        """
        cluster = cls(*args)
        try:
            cluster.create_cluster()
            yield cluster.endpoint(), cluster.port()
        finally:
            cluster.destroy()

    @abc.abstractmethod
    def destroy(self, test_recorder):
        """
        Tear down the cluster and record server logs. If the cluster is already destroyed or has not yet been created then this is a no-op.
        :param test_recorder: The test recorder to register server logs with.
        """
        pass

    @abc.abstractmethod
    def endpoint(self):
        """
        Get the endpoint that this cluster is listening on, e.g. 'localhost' or 'some.ip.address'.
        """
        pass

    @abc.abstractmethod
    def port(self):
        """
        Get the port that this cluster is listening on.
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
