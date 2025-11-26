# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_test_cluster import PerfTestCluster
from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig


class PerfMultiNodeCluster(PerfTestCluster):
    """
    Represents a performance multi node test cluster. This class deploys the opensearch bundle with CDK.
    """
    def __init__(
        self,
        bundle_manifest: BundleManifest,
        config: dict,
        stack_name: str,
        cluster_config: PerfTestClusterConfig,
        current_workspace: str
    ) -> None:
        assert not cluster_config.is_single_node_cluster, "Cluster is a single node configuration"
        work_dir = os.path.join(current_workspace, "opensearch-cluster", "cdk", "multi-node")
        super().__init__(bundle_manifest, config, stack_name, cluster_config, current_workspace, work_dir)

    def create_endpoint(self, cdk_output: dict) -> None:
        scheme = "https://" if self.cluster_config.security else "http://"
        host = cdk_output[self.stack_name].get("LoadBalancerEndpoint", None)
        self.is_endpoint_public = True
        if host is None:
            raise RuntimeError("Unable to fetch the cluster endpoint from cdk output")
        self.cluster_endpoint = host
        self.cluster_endpoint_with_port = "".join([scheme, host, ":", str(self.port)])

    def setup_cdk_params(self, config: dict) -> dict:
        return {
            "url": self.manifest.build.location,
            "security_group_id": config["Constants"]["SecurityGroupId"],
            "vpc_id": config["Constants"]["VpcId"],
            "account_id": config["Constants"]["AccountId"],
            "region": config["Constants"]["Region"],
            "cluster_stack_name": self.stack_name,
            "security": "enable" if self.cluster_config.security else "disable",
            "architecture": self.manifest.build.architecture,
            "master_node_count": int(self.cluster_config.master_nodes),
            "data_node_count": int(self.cluster_config.data_nodes),
            "ingest_node_count": int(self.cluster_config.ingest_nodes),
            "client_node_count": int(self.cluster_config.client_nodes),
            "use_50_percent_heap": self.cluster_config.use_50_percent_heap
        }
