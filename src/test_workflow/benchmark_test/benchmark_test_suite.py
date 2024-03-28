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
    args: BenchmarkArgs
    command: str
    password: str

    """
    Represents a performance test suite. This class runs rally test on the deployed cluster with the provided IP.
    """

    def __init__(
            self,
            endpoint: Any,
            security: bool,
            args: BenchmarkArgs,
            password: str
    ) -> None:
        self.endpoint = endpoint
        self.security = security
        self.args = args
        self.password = password

        # Pass the cluster endpoints with -t for multi-cluster use cases(e.g. cross-cluster-replication)
        self.command = 'docker run --rm'
        if self.args.benchmark_config:
            self.command += f" -v {args.benchmark_config}:/opensearch-benchmark/.benchmark/benchmark.ini"
        self.command += f" opensearchproject/opensearch-benchmark:latest execute-test --workload={self.args.workload} " \
                        f"--pipeline=benchmark-only --target-hosts={endpoint}"

        if self.args.workload_params:
            logging.info(f"Workload Params are {args.workload_params}")
            self.command += f" --workload-params '{args.workload_params}'"

        if self.args.test_procedure:
            self.command += f" --test-procedure=\"{self.args.test_procedure}\""

        if self.args.exclude_tasks:
            self.command += f" --exclude-tasks=\"{self.args.exclude_tasks}\""

        if self.args.include_tasks:
            self.command += f" --include-tasks=\"{self.args.include_tasks}\""

        if self.args.user_tag:
            user_tag = f"--user-tag=\"{args.user_tag}\""
            self.command += f" {user_tag}"

        if self.args.telemetry:
            self.command += " --telemetry "
            for value in self.args.telemetry:
                self.command += f"{value},"
            if self.args.telemetry_params:
                self.command += f" --telemetry-params '{self.args.telemetry_params}'"

    def execute(self) -> None:
        if self.security:
            self.command += f' --client-options="timeout:300,use_ssl:true,verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'{self.password}\'"'
        else:
            self.command += ' --client-options="timeout:300"'
        logging.info(f"Executing {self.command}")
        subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
