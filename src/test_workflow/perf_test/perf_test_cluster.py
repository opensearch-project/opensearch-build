# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import abc
import json
import logging
import os
import subprocess
from contextlib import contextmanager
from typing import Any, Generator, List

import requests
from requests.auth import HTTPBasicAuth
from retry.api import retry_call  # type: ignore

from manifests.bundle_manifest import BundleManifest
from test_workflow.integ_test.service import Service
from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig
from test_workflow.test_cluster import TestCluster


class PerfTestCluster(TestCluster):
    manifest: BundleManifest
    work_dir: str
    current_workspace: str
    stack_name: str
    output_file: str
    cluster_config: PerfTestClusterConfig
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
        bundle_manifest: BundleManifest,
        config: dict,
        stack_name: str,
        cluster_config: PerfTestClusterConfig,
        current_workspace: str,
        work_dir: str
    ) -> None:
        self.manifest = bundle_manifest
        self.work_dir = work_dir
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
        self.cluster_endpoint = None
        self.cluster_endpoint_with_port = None

    def start(self) -> None:
        os.chdir(self.work_dir)
        command = f"cdk deploy {self.params} --outputs-file {self.output_file}"
        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
        with open(self.output_file, "r") as read_file:
            load_output = json.load(read_file)
            self.create_endpoint(load_output)

    @abc.abstractmethod
    def create_endpoint(self, cdk_output: dict) -> None:
        pass

    @property
    def endpoint(self) -> str:
        return self.cluster_endpoint

    @property
    def endpoint_with_port(self) -> str:
        return self.cluster_endpoint_with_port

    @property
    def port(self) -> int:
        return 443 if self.cluster_config.security else 80

    def terminate(self) -> None:
        os.chdir(self.work_dir)
        command = f"cdk destroy {self.params} --force"
        logging.info(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)

    def service(self) -> Service:
        return None

    def dependencies(self) -> List[Service]:
        return []

    def wait_for_processing(self, tries: int = 3, delay: int = 15, backoff: int = 2) -> None:
        # Should be invoked only if the endpoint is public.
        assert self.is_endpoint_public, "wait_for_processing should be invoked only when cluster is public"
        logging.info("Waiting for domain to be up")
        url = "".join([self.endpoint_with_port, "/_cluster/health"])
        retry_call(requests.get, fkwargs={"url": url, "auth": HTTPBasicAuth('admin', 'admin'), "verify": False},
                   tries=tries, delay=delay, backoff=backoff)

    @abc.abstractmethod
    def setup_cdk_params(self, config: dict) -> dict:
        pass

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
