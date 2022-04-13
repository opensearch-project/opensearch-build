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
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK and returns the private IP.
    """

    def __init__(self, bundle_manifest, config, stack_name, security, current_workspace):
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(current_workspace, "opensearch-cluster", "cdk", "single-node")
        self.current_workspace = current_workspace
        self.stack_name = stack_name
        self.cluster_endpoint = None
        self.cluster_port = None
        self.output_file = "output.json"
        self.private_ip = None
        self.security = security
        role = config["Constants"]["Role"]
        params_dict = {
            "url": self.manifest.build.location,
            "security_group_id": config["Constants"]["SecurityGroupId"],
            "vpc_id": config["Constants"]["VpcId"],
            "account_id": config["Constants"]["AccountId"],
            "region": config["Constants"]["Region"],
            "stack_name": self.stack_name,
            "security": "enable" if self.security else "disable",
            "platform": self.manifest.build.platform,
            "architecture": self.manifest.build.architecture,
            "public_ip": config["Constants"].get("PublicIp", "disable")
        }
        params_list = []
        for key, value in params_dict.items():
            params_list.append(f" -c {key}={value}")
        role_params = (
            f" --require-approval=never --plugin cdk-assume-role-credential-plugin"
            f" -c assume-role-credentials:writeIamRoleName={role} -c assume-role-credentials:readIamRoleName={role} "
        )
        self.params = "".join(params_list) + role_params
        self.cluster_endpoint = None
        self.public_ip = None

    def start(self):
        os.chdir(self.work_dir)
        command = f"cdk deploy {self.params} --outputs-file {self.output_file}"
        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
        with open(self.output_file, "r") as read_file:
            load_output = json.load(read_file)
        self.private_ip = load_output[self.stack_name]["PrivateIp"]
        logging.info(f"Private IP: {self.private_ip}")
        self.public_ip = load_output[self.stack_name].get("PublicIp", None)

    def endpoint(self):
        if self.cluster_endpoint is None:
            scheme = "https://" if self.security else "http://"
            # If instances are configured to have public ip, use that instead.
            host = self.private_ip if self.public_ip is None else self.public_ip
            if host is not None:
                self.cluster_endpoint = "".join([scheme, host, ":", str(self.port())])
        return self.cluster_endpoint

    def port(self):
        self.cluster_port = 443 if self.security else 9200
        return self.cluster_port

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
        if self.public_ip is None:
            return
        url = "".join([self.endpoint(), "/_cluster/health"])
        retry_call(requests.get, fkwargs={"url": url, "auth": HTTPBasicAuth('admin', 'admin'), "verify": False},
                   tries=tries, delay=delay, backoff=backoff)

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
