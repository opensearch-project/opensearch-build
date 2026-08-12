# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import json
import logging
import os
import subprocess
from contextlib import contextmanager
from typing import Any, Dict, Generator, Union

import requests
from requests.auth import HTTPBasicAuth
from retry.api import retry_call  # type: ignore

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_cluster import BenchmarkTestCluster
from test_workflow.integ_test.utils import get_password


class BenchmarkCreateCluster(BenchmarkTestCluster):
    # Cross-cluster-replication aliases, shared by both clusters. The primary (leader) is 'cluster-1'
    # and the secondary (follower) is 'cluster-2'. Each alias doubles as the 'cluster.remote.<alias>.seeds'
    # key pointing at that cluster's seed node, so the two clusters must agree on them.
    PRIMARY_ALIAS = "cluster-1"
    SECONDARY_ALIAS = "cluster-2"
    REPLICATION_RELATIONSHIP = "my-relationship"
    # 'node.name' that opensearch-cluster-cdk assigns to the seed node of a multi-node cluster.
    SEED_NODE_NAME = "seed"

    manifest: Union[BundleManifest, BuildManifest]
    work_dir: str
    current_workspace: str
    output_file: str
    params: str
    is_endpoint_public: bool
    cluster_endpoint: str
    cluster_role: str
    stack_suffix: str
    seed_node_ip: str

    """
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK. Supports both single
    and multi-node clusters
    """

    def __init__(
            self,
            args: BenchmarkArgs,
            bundle_manifest: Union[BundleManifest, BuildManifest],
            config: dict,
            current_workspace: str,
            cluster_role: str = None
    ) -> None:
        super().__init__(args)
        self.manifest = bundle_manifest
        self.current_workspace = current_workspace
        # Role of the cluster in a cross-cluster-replication run, either 'leader' or 'follower'.
        # It is appended to the stack suffix/name to differentiate the two cluster stacks.
        self.cluster_role = cluster_role
        self.output_file = f"output-{cluster_role}.json" if cluster_role else "output.json"
        # Append the cluster role (leader/follower) to the stack suffix so that the two CCR
        # cluster stacks get unique, differentiable names. Does not mutate the shared args.
        self.stack_suffix = f"{self.args.stack_suffix}-{cluster_role}" if cluster_role else self.args.stack_suffix
        role = config["Constants"]["Role"]
        params_dict = self.setup_cdk_params(config)
        params_list = []
        for key, value in params_dict.items():
            if value:
                '''
                TODO: To send json input to typescript code from command line it needs to be enclosed in
                single-quotes, this is a temp fix to achieve that since the quoted string passed from command line in
                tesh.sh wrapper script gets un-quoted and we need to handle it here.
                '''
                if key == 'additionalConfig':
                    params_list.append(f" -c {key}=\'{value}\'")
                else:
                    params_list.append(f" -c {key}={value}")
        role_params = (
            f" --require-approval=never --plugin cdk-assume-role-credential-plugin"
            f" -c assume-role-credentials:writeIamRoleName={role} -c assume-role-credentials:readIamRoleName={role} "
        )
        self.params = "".join(params_list) + role_params
        self.password = None if self.args.insecure else get_password(self.args.distribution_version)
        self.is_endpoint_public = False
        # Private IP of the seed node (single-node ip for a single node cluster), resolved once
        # the cluster is up. Required to apply cross-cluster-replication settings on the follower.
        self.seed_node_ip = None
        self.stack_name = f"opensearch-infra-stack-{self.stack_suffix}"
        if self.manifest:
            self.stack_name += f"-{self.manifest.build.id}-{self.manifest.build.architecture}"

    def start(self) -> None:
        command = f"npm install && cdk deploy \"*\" {self.params} --outputs-file {self.output_file}"

        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
        with open(self.output_file, "r") as read_file:
            load_output = json.load(read_file)
            self.create_endpoint(load_output)
        self.wait_for_processing()
        logging.info("Wait for processing executed")
        # Resolved after the cluster is up, since for a multi-node cluster the seed node address is
        # read from the cluster itself rather than from the cdk output.
        if self.args.ccr_enabled:
            self.seed_node_ip = self.fetch_seed_node_ip(load_output)

    def create_endpoint(self, cdk_output: dict) -> None:
        load_balancer_url = cdk_output[self.stack_name].get('loadbalancerurl', None)
        if load_balancer_url is None:
            raise RuntimeError("Unable to fetch the cluster endpoint from cdk output")
        self.cluster_endpoint = load_balancer_url
        self.cluster_endpoint_with_port = "".join([load_balancer_url, ":", str(self.port)])

    def fetch_seed_node_ip(self, cdk_output: dict) -> str:
        """
        Resolve the private IP of the seed node, which is needed to apply cross-cluster-replication
        settings. For a single-node cluster the IP is exposed directly in the cdk output ('privateip').
        For a multi-node cluster the nodes sit behind autoscaling groups and are not published by cdk,
        so the address is read from the cluster itself over its load balancer. Asking the cluster
        avoids needing EC2 permissions in the cluster's AWS account, which the host running this
        workflow does not have (cdk reaches that account via cdk-assume-role-credential-plugin).
        """
        if self.args.single_node:
            private_ip = cdk_output[self.stack_name].get('privateip', None)
            if private_ip is None:
                raise RuntimeError("Unable to fetch the single-node private ip from cdk output")
            return str(private_ip)

        return self.fetch_seed_node_ip_from_cluster()

    def fetch_seed_node_ip_from_cluster(self) -> str:
        """
        Ask the cluster for the ip of its seed node. opensearch-cluster-cdk names that node 'seed'
        (see nodeConfig 'seed-manager'/'seed-data'), which identifies it unambiguously - matching on
        the cluster_manager role would not, since every dedicated manager node also carries it.

        The seed node has always joined by this point: every asg is deployed with
        Signals.waitForAll(), so cdk deploy does not return until all nodes signal success.
        """
        nodes = self.get("/_cat/nodes?format=json&h=ip,name")
        for node in nodes:
            if node.get("name") == self.SEED_NODE_NAME and node.get("ip"):
                return str(node["ip"])
        raise RuntimeError(f"Unable to find a node named '{self.SEED_NODE_NAME}' in cluster {self.stack_name}")

    def apply_leader_settings(self) -> None:
        """
        Placeholder to apply arrow streaming settings on the leader cluster.
        TODO: Fill in the exact arrow streaming settings once finalized.
        """
        logging.info(f"Applying leader (arrow streaming) settings on cluster {self.stack_name}")

    def apply_follower_settings(self, leader_seed_node_ip: str) -> None:
        """
        Apply cross-cluster-replication settings on the follower (secondary) cluster: connect to the
        leader's seed node under the primary alias, then register this cluster as the SECONDARY end
        of a remote replication relationship with that leader.
        TODO: Add the arrow streaming settings here once finalized.
        """
        if not leader_seed_node_ip:
            raise RuntimeError("Unable to apply follower CCR settings, leader seed node ip is missing")

        logging.info(f"Applying follower (CCR) settings on cluster {self.stack_name} "
                     f"pointing to leader seed node {'*' * len(leader_seed_node_ip)}")

        self.connect_remote_cluster(self.PRIMARY_ALIAS, leader_seed_node_ip)

        # The remote connection above has to exist before the relationship can reference it by alias.
        self.put(
            f"/_remote_replication/cluster/{self.REPLICATION_RELATIONSHIP}",
            {
                "role": "SECONDARY",
                "local_alias": self.SECONDARY_ALIAS,
                "remote_alias": self.PRIMARY_ALIAS
            }
        )

    def apply_leader_reverse_settings(self, follower_seed_node_ip: str) -> None:
        """
        Point the leader (primary) cluster back at the follower's seed node under the secondary alias.
        Both clusters knowing each other's seed node is what makes a later switchover possible; this is
        applied after the follower is up so its seed node ip is known.
        """
        if not follower_seed_node_ip:
            raise RuntimeError("Unable to apply leader reverse CCR settings, follower seed node ip is missing")

        logging.info(f"Applying leader reverse (CCR) settings on cluster {self.stack_name} "
                     f"pointing to follower seed node {'*' * len(follower_seed_node_ip)}")

        self.connect_remote_cluster(self.SECONDARY_ALIAS, follower_seed_node_ip)

    def connect_remote_cluster(self, alias: str, seed_node_ip: str) -> None:
        """Register a remote cluster connection under 'alias', seeded from seed_node_ip's transport port."""
        self.put(
            "/_cluster/settings",
            {
                "persistent": {
                    f"cluster.remote.{alias}.seeds": [f"{seed_node_ip}:9300"]
                }
            }
        )

    def request_args(self, path: str) -> Dict[str, Any]:
        protocol = "http://" if self.args.insecure else "https://"
        request_args: Dict[str, Any] = {"url": "".join([protocol, self.endpoint, path])}
        if not self.args.insecure:
            request_args["auth"] = HTTPBasicAuth(self.args.username, self.password)
            request_args["verify"] = False
        return request_args

    def put(self, path: str, payload: dict) -> None:
        request_args = self.request_args(path)
        request_args["json"] = payload

        def _put() -> None:
            response = requests.put(**request_args)
            response.raise_for_status()

        retry_call(_put, tries=3, delay=15, backoff=2)

    def get(self, path: str) -> Any:
        request_args = self.request_args(path)

        def _get() -> Any:
            response = requests.get(**request_args)
            response.raise_for_status()
            return response.json()

        return retry_call(_get, tries=3, delay=15, backoff=2)

    def terminate(self) -> None:
        command = f"cdk destroy {self.stack_name} {self.params} --force"
        logging.info(f'Executing "{command}" in {os.getcwd()}')

        subprocess.check_call(command, cwd=os.getcwd(), shell=True)

    def setup_cdk_params(self, config: dict) -> dict:
        suffix = ''
        if self.stack_suffix and self.manifest:
            suffix = self.stack_suffix + '-' + self.manifest.build.id + '-' + self.manifest.build.architecture
        elif self.manifest:
            suffix = self.manifest.build.id + '-' + self.manifest.build.architecture
        elif self.stack_suffix:
            suffix = self.stack_suffix

        if self.manifest:
            self.args.distribution_version = self.manifest.build.version
            artifact_url = self.manifest.build.location if isinstance(self.manifest, BundleManifest) else \
                f"https://artifacts.opensearch.org/snapshots/core/opensearch/{self.manifest.build.version}/opensearch-min-" \
                f"{self.manifest.build.version}-linux-{self.manifest.build.architecture}-latest.tar.gz"
        else:
            artifact_url = self.args.distribution_url.strip()

        return {
            "distributionUrl": artifact_url,
            "pluginUrl": self.args.plugin_url,
            "vpcId": config["Constants"]["VpcId"],
            "account": config["Constants"]["AccountId"],
            "region": config["Constants"]["Region"],
            "suffix": suffix,
            "securityDisabled": str(self.args.insecure).lower(),
            "adminPassword": None if self.args.insecure else get_password(self.args.distribution_version),
            "cpuArch": self.manifest.build.architecture if self.manifest else 'x64',
            "singleNodeCluster": str(self.args.single_node).lower(),
            "distVersion": self.args.distribution_version,
            "minDistribution": str(self.args.min_distribution).lower(),
            "serverAccessType": config["Constants"]["serverAccessType"],
            "restrictServerAccessTo": config["Constants"]["restrictServerAccessTo"],
            "additionalConfig": self.args.additional_config,
            "dataInstanceType": self.args.data_instance_type,
            "managerNodeCount": self.args.manager_node_count,
            "dataNodeCount": self.args.data_node_count,
            "clientNodeCount": self.args.client_node_count,
            "ingestNodeCount": self.args.ingest_node_count,
            "mlNodeCount": self.args.ml_node_count,
            "dataNodeStorage": self.args.data_node_storage,
            "mlNodeStorage": self.args.ml_node_storage,
            "useInstanceBasedStorage": str(self.args.enable_instance_storage).lower(),
            "jvmSysProps": self.args.jvm_sys_props,
            "heapSizeInGb": self.args.heap_size_in_gb,
            "isInternal": config["Constants"]["isInternal"],
            "enableRemoteStore": str(self.args.enable_remote_store).lower(),
            "customRoleArn": config["Constants"]["IamRoleArn"]
        }

    @classmethod
    @contextmanager
    def create(cls, *args: Any) -> Generator[Any, None, None]:
        """
        Set up the cluster. When this method returns, the cluster must be available to take requests.
        Throws ClusterCreationException if the cluster could not start for some reason. If this exception is thrown, the caller does not need to call "destroy".
        """
        cluster = cls(*args)

        try:
            cluster.start()
            yield cluster
        finally:
            if cluster.args.preserve_cluster:
                logging.info("Preserving cluster as --preserve-cluster flag is set. Skipping cdk destroy.")
            else:
                cluster.terminate()
