# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import json
import logging
import subprocess
from typing import Any

import requests
from requests.auth import HTTPBasicAuth
from retry.api import retry_call  # type: ignore

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.integ_test.utils import get_password


class BenchmarkTestCluster:
    args: BenchmarkArgs
    cluster_endpoint: str
    cluster_endpoint_with_port: str
    secondary_cluster_endpoint: str
    secondary_cluster_endpoint_with_port: str
    password: str

    def __init__(
            self,
            args: BenchmarkArgs

    ) -> None:
        self.args = args
        self.cluster_endpoint = self.args.cluster_endpoint
        self.cluster_endpoint_with_port = None
        self.secondary_cluster_endpoint = self.args.secondary_endpoint
        self.secondary_cluster_endpoint_with_port = None
        self.password = self.args.password if self.args.password else get_password('2.12.0')

    def start(self) -> None:
        if not self.args.sigv4:
            res_dict = self.fetch_cluster_info(self.cluster_endpoint)
            self.args.distribution_version = res_dict['version']['number']
            self.wait_for_processing()
            self.cluster_endpoint_with_port = "".join([self.cluster_endpoint, ":", str(self.port)])
            if self.secondary_cluster_endpoint:
                # The version is only read off the primary cluster, both clusters of a multi-cluster
                # run are expected to be on the same version.
                self.fetch_cluster_info(self.secondary_cluster_endpoint)
                self.wait_for_processing(endpoint=self.secondary_cluster_endpoint)
                self.secondary_cluster_endpoint_with_port = "".join([self.secondary_cluster_endpoint, ":", str(self.port)])
        else:
            self.args.distribution_version = "2.17.0"
            self.cluster_endpoint_with_port = "".join([self.cluster_endpoint, ":", str(self.port)])
            if self.secondary_cluster_endpoint:
                self.secondary_cluster_endpoint_with_port = "".join([self.secondary_cluster_endpoint, ":", str(self.port)])

    def fetch_cluster_info(self, endpoint: str) -> Any:
        command = f"curl -fsSL http://{endpoint}" if self.args.insecure else f"curl -fsSL https://{endpoint} -ku '{self.args.username}:{self.password}'"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, timeout=30)
        except subprocess.TimeoutExpired:
            raise TimeoutError("Time out! Couldn't connect to the cluster")

        if not result.stdout:
            raise Exception("Empty response retrieved from the curl command")

        return json.loads(result.stdout)

    @property
    def endpoint(self) -> str:
        return self.cluster_endpoint

    @property
    def endpoint_with_port(self) -> str:
        return self.cluster_endpoint_with_port

    @property
    def secondary_endpoint(self) -> str:
        return self.secondary_cluster_endpoint

    @property
    def secondary_endpoint_with_port(self) -> str:
        return self.secondary_cluster_endpoint_with_port

    @property
    def target_hosts(self) -> Any:
        """
        A single endpoint is passed to opensearch-benchmark as a plain 'host:port' string. When a secondary
        endpoint is given the hosts are passed as a role -> hosts mapping instead, where opensearch-benchmark
        addresses the primary cluster as 'default' and the secondary one as 'follower'.
        """
        if not self.secondary_cluster_endpoint:
            return self.cluster_endpoint_with_port

        return {
            "default": [{"host": self.cluster_endpoint, "port": self.port}],
            "follower": [{"host": self.secondary_cluster_endpoint, "port": self.port}],
        }

    @property
    def port(self) -> int:
        return 80 if self.args.insecure else 443

    def fetch_password(self) -> str:
        return self.password

    def wait_for_processing(self, tries: int = 10, delay: int = 30, backoff: int = 1, endpoint: str = None) -> None:
        logging.info("Waiting for domain ******* to be up")
        protocol = "http://" if self.args.insecure else "https://"
        url = "".join([protocol, endpoint if endpoint else self.endpoint, "/_cluster/health"])
        request_args = {"url": url} if self.args.insecure else {"url": url, "auth": HTTPBasicAuth(self.args.username, self.password),  # type: ignore
                                                                "verify": False}  # type: ignore
        retry_call(requests.get, fkwargs=request_args, tries=tries, delay=delay, backoff=backoff)
