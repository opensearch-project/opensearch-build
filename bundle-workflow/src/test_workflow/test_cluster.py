# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
from contextlib import contextmanager
from test_workflow.perf_test_cluster import PerfTestCluster


class TestCluster(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """
    @staticmethod
    @abc.abstractmethod
    @contextmanager
    def create(cluster_type, *args):
        """
        Set up the cluster. When this method returns, the cluster must be available to take requests.
        Throws ClusterCreationException if the cluster could not start for some reason. If this exception is thrown, the caller does not need to call "destroy".
        """
        if cluster_type == 'PERFORMANCE_TEST':
            test_cluster = PerfTestCluster(args[0], args[1], args[2], args[3])
        try:
            test_cluster.create()
            yield test_cluster.endpoint()
        finally:
            test_cluster.destroy()

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
