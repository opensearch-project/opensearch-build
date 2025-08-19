# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import json
import logging
import subprocess

import requests
from requests.auth import HTTPBasicAuth
from retry.api import retry_call  # type: ignore

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.integ_test.utils import get_password


class BenchmarkTestCluster:
    args: BenchmarkArgs
    cluster_endpoint: str
    cluster_endpoint_with_port: str
    password: str

    def __init__(
            self,
            args: BenchmarkArgs

    ) -> None:
        self.args = args
        self.cluster_endpoint = self.args.cluster_endpoint
        self.cluster_endpoint_with_port = None
        self.password = self.args.password if self.args.password else get_password('2.12.0')

    def start(self) -> None:
        if self.args.sigv4:
            # For SigV4, skip username/password authentication
            command = f"curl https://{self.cluster_endpoint}"
        else:
            command = f"curl http://{self.cluster_endpoint}" if self.args.insecure else f"curl https://{self.cluster_endpoint} -ku '{self.args.username}:{self.password}'"

        try:
            result = subprocess.run(command, shell=True, capture_output=True, timeout=30)
        except subprocess.TimeoutExpired:
            raise TimeoutError("Time out! Couldn't connect to the cluster")

        if result.stdout:
            res_dict = json.loads(result.stdout)
            self.args.distribution_version = res_dict['version']['number']
            self.wait_for_processing()
            self.cluster_endpoint_with_port = "".join([self.cluster_endpoint, ":", str(self.port)])
        else:
            raise Exception("Empty response retrieved from the curl command")

    @property
    def endpoint(self) -> str:
        return self.cluster_endpoint

    @property
    def endpoint_with_port(self) -> str:
        return self.cluster_endpoint_with_port

    @property
    def port(self) -> int:
        return 80 if self.args.insecure else 443

    def fetch_password(self) -> str:
        return self.password

    def wait_for_processing(self, tries: int = 3, delay: int = 15, backoff: int = 2) -> None:
        logging.info("Waiting for domain ******* to be up")
        protocol = "http://" if self.args.insecure else "https://"
        url = "".join([protocol, self.endpoint, "/_cluster/health"])

        try:
            if hasattr(self.args, 'sigv4') and self.args.sigv4:
                request_args = {"url": url}
            elif self.args.insecure:
                request_args = {"url": url}
            else:
                request_args = {"url": url, "auth": HTTPBasicAuth(self.args.username, self.password), "verify": False}

            retry_call(requests.get, fkwargs=request_args, tries=tries, delay=delay, backoff=backoff)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logging.info("404 response indicates serverless collection, skipping health checks")
                return
            else:
                raise
