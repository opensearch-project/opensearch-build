# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
from typing import Any

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs


class BenchmarkTestSuite:
    endpoint: str
    security: bool
    current_workspace: str
    args: BenchmarkArgs
    command: str

    """
    Represents a performance test suite. This class runs rally test on the deployed cluster with the provided IP.
    """

    def __init__(
            self,
            endpoint: Any,
            security: bool,
            args: BenchmarkArgs,
    ) -> None:
        self.endpoint = endpoint
        self.security = security
        self.args = args
        # Pass the cluster endpoints with -t for multi-cluster use cases(e.g. cross-cluster-replication)
        self.command = 'docker run --rm'
        if args.benchmark_config:
            self.command += f" -v {args.benchmark_config}:/opensearch-benchmark/.benchmark/benchmark.ini"
        self.command += f" opensearchproject/opensearch-benchmark:latest execute-test --workload={self.args.workload} " \
                        f"--pipeline=benchmark-only --target-hosts={endpoint}"

        if args.workload_params:
            logging.info(f"Workload Params are {args.workload_params}")
            self.command += f" --workload-params '{args.workload_params}'"

        if args.user_tag:
            user_tag = f"--user-tag=\"{args.user_tag}\""
            self.command += f" {user_tag}"

        if args.telemetry:
            self.command += " --telemetry "
            for value in args.telemetry:
                self.command += f"{value},"

    def execute(self) -> None:
        if self.security:
            self.command += ' --client-options="timeout:300,use_ssl:true,verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'admin\'"'
        else:
            self.command += ' --client-options="timeout:300"'
        logging.info(f"Executing {self.command}")
        subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
