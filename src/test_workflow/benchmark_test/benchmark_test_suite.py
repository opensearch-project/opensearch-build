# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import json
import logging
import os
import shutil
import subprocess
from typing import Any

import pandas as pd

from system.temporary_directory import TemporaryDirectory
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
        self.command = f'docker run --name docker-container-{self.args.stack_suffix}'
        if self.args.benchmark_config:
            self.command += f" -v {args.benchmark_config}:/opensearch-benchmark/.benchmark/benchmark.ini"
        self.command += f" opensearchproject/opensearch-benchmark:1.6.0 execute-test --workload={self.args.workload} " \
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

        if self.security:
            self.command += (f' --client-options="timeout:300,use_ssl:true,verify_certs:false,basic_auth_user:\'{self.args.username}\','
                             f'basic_auth_password:\'{self.password}\'" --results-file=final_result.md')
        else:
            self.command += ' --client-options="timeout:300" --results-file=final_result.md'

    def execute(self) -> None:
        log_info = f"Executing {self.command.replace(self.endpoint, len(self.endpoint) * '*').replace(self.args.username, len(self.args.username) * '*')}"
        logging.info(log_info.replace(self.password, len(self.password) * '*') if self.password else log_info)
        try:
            subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
            if self.args.cluster_endpoint or self.args.distribution_url:
                self.convert()
        finally:
            self.cleanup()

    def convert(self) -> None:
        with TemporaryDirectory() as work_dir:
            subprocess.check_call(f"docker cp docker-container-{self.args.stack_suffix}:opensearch-benchmark"
                                  f"/test_executions/. {str(work_dir.path)}", cwd=os.getcwd(), shell=True)
            subprocess.check_call(f"docker cp docker-container-{self.args.stack_suffix}:opensearch-benchmark"
                                  f"/final_result.md {str(work_dir.path)}", cwd=os.getcwd(), shell=True)
            file_path = glob.glob(os.path.join(str(work_dir.path), "*", "test_execution.json"))
            final_results_file = glob.glob(os.path.join(str(work_dir.path), "final_result.md"))
            shutil.copy(file_path[0], os.path.join('/tmp', f"test_execution_{self.args.stack_suffix}.json"))
            shutil.copy(final_results_file[0], os.path.join('/tmp', f"final_result_{self.args.stack_suffix}.md"))
            with open(file_path[0]) as file:
                data = json.load(file)
                formatted_data = pd.json_normalize(data["results"]["op_metrics"])
                formatted_data.to_csv(os.path.join(os.getcwd(), f"test_execution_{self.args.stack_suffix}.csv"), index=False)
                df = pd.read_csv(os.path.join(os.getcwd(), f"test_execution_{self.args.stack_suffix}.csv"))
                pd.set_option('display.width', int(2 * shutil.get_terminal_size().columns))
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                logging.info(f"\n{df}")

    def cleanup(self) -> None:
        subprocess.check_call(f"docker rm docker-container-{self.args.stack_suffix}", cwd=os.getcwd(), shell=True)
