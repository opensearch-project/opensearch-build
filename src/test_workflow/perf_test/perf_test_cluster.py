import json
import logging
import os
import subprocess
from contextlib import contextmanager

import requests
from requests.auth import HTTPBasicAuth
from retry.api import retry_call

from test_workflow.test_cluster import TestCluster


class PerfTestCluster(TestCluster):
    """
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK. Supports both single
    and multi-node clusters
    """

    def __init__(self, bundle_manifest, config, stack_name, cluster_config, current_workspace):
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(current_workspace, "opensearch-cluster", "cdk",
                                     "single-node" if cluster_config.is_single_node_cluster() else "multi-node")
        self.current_workspace = current_workspace
        self.stack_name = stack_name
        self.output_file = "output.json"
        self.cluster_config = cluster_config
        role = config["Constants"]["Role"]
        params_dict = self.setup_cdk_params(config)
        params_list = []
        for key, value in params_dict.items():
            params_list.append(f" -c {key}={value}")
        role_params = (
            f" --require-approval=never --plugin cdk-assume-role-credential-plugin"
            f" -c assume-role-credentials:writeIamRoleName={role} -c assume-role-credentials:readIamRoleName={role} "
        )
        self.params = "".join(params_list) + role_params
        self.is_endpoint_public = False
        self.cluster_endpoint_with_port = None
        self.endpoint = None

    def start(self):
        os.chdir(self.work_dir)
        command = f"cdk deploy {self.params} --outputs-file {self.output_file}"
        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
        with open(self.output_file, "r") as read_file:
            load_output = json.load(read_file)
            self.create_endpoint(load_output)

    def create_endpoint(self, cdk_output):
        scheme = "https://" if self.cluster_config.security else "http://"
        if self.cluster_config.is_single_node_cluster():
            private_ip = cdk_output[self.stack_name]["PrivateIp"]
            public_ip = cdk_output[self.stack_name].get("PublicIp", None)
            self.is_endpoint_public = public_ip is not None
            host = public_ip if public_ip is not None else private_ip
        else:
            host = cdk_output[self.stack_name]["LoadBalancerEndpoint"]
            self.is_endpoint_public = True

        if host is not None:
            self.endpoint = host
            self.cluster_endpoint_with_port = "".join([scheme, host, ":", str(self.port())])

    def endpoint_with_port(self):
        return self.cluster_endpoint_with_port

    def endpoint(self):
        return self.endpoint

    def port(self):
        return 443 if self.cluster_config.security else 80

    def terminate(self):
        os.chdir(os.path.join(self.current_workspace, self.work_dir))
        command = f"cdk destroy {self.params} --force"
        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)

    def service(self):
        return []

    def dependencies(self):
        return []

    def wait_for_processing(self, tries=3, delay=15, backoff=2):
        # Should be invoked only if the endpoint is public.
        assert self.is_endpoint_public, "wait_for_processing should be invoked only when cluster is public"
        print("Waiting for domain to be up")
        url = "".join([self.endpoint_with_port(), "/_cluster/health"])
        retry_call(requests.get, fkwargs={"url": url, "auth": HTTPBasicAuth('admin', 'admin'), "verify": False},
                   tries=tries, delay=delay, backoff=backoff)

    def setup_cdk_params(self, config):
        if self.cluster_config.is_single_node_cluster():
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
        else:
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
                "client_node_count": int(self.cluster_config.client_nodes)
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
