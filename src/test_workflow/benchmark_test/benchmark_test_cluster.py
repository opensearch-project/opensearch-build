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
from typing import Any, Generator, Union

import requests
from requests.auth import HTTPBasicAuth
from retry.api import retry_call  # type: ignore

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs


class BenchmarkTestCluster:
    manifest: Union[BundleManifest, BuildManifest]
    work_dir: str
    current_workspace: str
    args: BenchmarkArgs
    output_file: str
    params: str
    is_endpoint_public: bool
    cluster_endpoint: str
    cluster_endpoint_with_port: str

    """
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK. Supports both single
    and multi-node clusters
    """

    def __init__(
            self,
            bundle_manifest: Union[BundleManifest, BuildManifest],
            config: dict,
            args: BenchmarkArgs,
            current_workspace: str
    ) -> None:
        self.manifest = bundle_manifest
        self.current_workspace = current_workspace
        self.args = args
        self.output_file = "output.json"
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
        self.is_endpoint_public = False
        self.cluster_endpoint = None
        self.cluster_endpoint_with_port = None
        self.stack_name = f"opensearch-infra-stack-{self.args.stack_suffix}-{self.manifest.build.id}-{self.manifest.build.architecture}"

    def start(self) -> None:
        command = f"npm install && cdk deploy \"*\" {self.params} --outputs-file {self.output_file}"

        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
        with open(self.output_file, "r") as read_file:
            load_output = json.load(read_file)
            self.create_endpoint(load_output)
        self.wait_for_processing()

    def create_endpoint(self, cdk_output: dict) -> None:
        loadbalancer_url = cdk_output[self.stack_name].get('loadbalancerurl', None)
        if loadbalancer_url is None:
            raise RuntimeError("Unable to fetch the cluster endpoint from cdk output")
        self.cluster_endpoint = loadbalancer_url
        self.cluster_endpoint_with_port = "".join([loadbalancer_url, ":", str(self.port)])

    @property
    def endpoint(self) -> str:
        return self.cluster_endpoint

    @property
    def endpoint_with_port(self) -> str:
        return self.cluster_endpoint_with_port

    @property
    def port(self) -> int:
        return 80 if self.args.insecure else 443

    def terminate(self) -> None:
        command = f"cdk destroy {self.stack_name} {self.params} --force"
        logging.info(f'Executing "{command}" in {os.getcwd()}')

        subprocess.check_call(command, cwd=os.getcwd(), shell=True)

    def wait_for_processing(self, tries: int = 3, delay: int = 15, backoff: int = 2) -> None:
        logging.info(f"Waiting for domain at {self.endpoint} to be up")
        protocol = "http://" if self.args.insecure else "https://"
        url = "".join([protocol, self.endpoint, "/_cluster/health"])
        request_args = {"url": url} if self.args.insecure else {"url": url, "auth": HTTPBasicAuth("admin", "admin"), "verify": False}  # type: ignore
        retry_call(requests.get, fkwargs=request_args,
                   tries=tries, delay=delay, backoff=backoff)

    def setup_cdk_params(self, config: dict) -> dict:
        if self.args.stack_suffix:
            suffix = self.args.stack_suffix + '-' + self.manifest.build.id + '-' + self.manifest.build.architecture
        else:
            suffix = self.manifest.build.id + '-' + self.manifest.build.architecture
        return {
            "distributionUrl": self.manifest.build.location if isinstance(self.manifest, BundleManifest) else
            f"https://artifacts.opensearch.org/snapshots/core/opensearch/{self.manifest.build.version}/opensearch-min-"
            f"{self.manifest.build.version}-linux-{self.manifest.build.architecture}-latest.tar.gz",
            "vpcId": config["Constants"]["VpcId"],
            "account": config["Constants"]["AccountId"],
            "region": config["Constants"]["Region"],
            "suffix": suffix,
            "securityDisabled": str(self.args.insecure).lower(),
            "cpuArch": self.manifest.build.architecture,
            "singleNodeCluster": str(self.args.single_node).lower(),
            "distVersion": self.manifest.build.version,
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
            "jvmSysProps": self.args.jvm_sys_props,
            "use50PercentHeap": str(self.args.use_50_percent_heap).lower(),
            "isInternal": config["Constants"]["isInternal"],
            "enableRemoteStore": str(self.args.enable_remote_store).lower()
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
            cluster.terminate()
