
import os
from contextlib import contextmanager

from test_workflow.perf_test.perf_test_cluster import PerfTestCluster


class PerfSingleNodeCluster(PerfTestCluster):
    """
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK. Supports both single
    and multi-node clusters
    """
    def __init__(self, bundle_manifest, config, stack_name, cluster_config, current_workspace):
        assert cluster_config.is_single_node_cluster(), "Cluster is not a single node cluster"
        work_dir = os.path.join(current_workspace, "opensearch-cluster", "cdk", "single-node")
        super().__init__(bundle_manifest, config, stack_name, cluster_config, current_workspace, work_dir)

    def create_endpoint(self, cdk_output):
        scheme = "https://" if self.cluster_config.security else "http://"
        private_ip = cdk_output[self.stack_name]["PrivateIp"]
        public_ip = cdk_output[self.stack_name].get("PublicIp", None)
        self.is_endpoint_public = public_ip is not None
        host = public_ip if public_ip is not None else private_ip
        if host is not None:
            self.endpoint = host
            self.cluster_endpoint_with_port = "".join([scheme, host, ":", str(self.port)])

    def setup_cdk_params(self, config):
        return {
            "url": self.manifest.build.location,
            "security_group_id": config["Constants"]["SecurityGroupId"],
            "vpc_id": config["Constants"]["VpcId"],
            "account_id": config["Constants"]["AccountId"],
            "region": config["Constants"]["Region"],
            "stack_name": self.stack_name,
            "security": "enable" if self.cluster_config.security else "disable",
            "platform": self.manifest.build.platform,
            "architecture": self.manifest.build.architecture,
            "public_ip": config["Constants"].get("PublicIp", "disable")
        }

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
            yield cluster
        finally:
            cluster.terminate()
