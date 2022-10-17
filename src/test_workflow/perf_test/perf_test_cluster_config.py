# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

class PerfTestClusterConfig():
    security: bool
    data_nodes: int
    master_nodes: int
    ingest_nodes: int
    client_nodes: int
    _is_single_node_cluster: bool
    use_50_percent_heap: str

    """
    Maintains the cluster level configuration.
    """
    def __init__(self, security: bool = False, data_nodes: int = 1, master_nodes: int = 0, ingest_nodes: int = 0, client_nodes: int = 0, use_50_percent_heap: str = "disable") -> None:
        self.security = security
        self.data_nodes = data_nodes
        self.master_nodes = master_nodes
        self.ingest_nodes = ingest_nodes
        self.client_nodes = client_nodes
        self._is_single_node_cluster = (self.data_nodes == 1 and self.master_nodes == 0
                                        and self.ingest_nodes == 0 and self.client_nodes == 0)
        self.use_50_percent_heap = use_50_percent_heap

    @property
    def is_single_node_cluster(self) -> bool:
        return self._is_single_node_cluster
