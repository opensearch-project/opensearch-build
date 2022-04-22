# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

class PerfTestClusterConfig():
    """
    Maintains the cluster level configuration.
    """
    def __init__(self, security=False, data_nodes=1, master_nodes=0, ingest_nodes=0, client_nodes=0):
        self.security = security
        self.data_nodes = data_nodes
        self.master_nodes = master_nodes
        self.ingest_nodes = ingest_nodes
        self.client_nodes = client_nodes
        self._is_single_node_cluster = (self.data_nodes == 1 and self.master_nodes == 0
                                        and self.ingest_nodes == 0 and self.client_nodes == 0)

    @property
    def is_single_node_cluster(self):
        return self._is_single_node_cluster
