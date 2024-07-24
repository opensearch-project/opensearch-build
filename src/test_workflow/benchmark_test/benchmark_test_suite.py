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

        if self.args.command == 'execute-test':
            self.form_benchmark_command()
        elif self.args.command == 'compare':
            self.form_compare_command()

    def execute(self) -> None:
        if self.args.command == "execute-test":
            log_info = f"Executing {self.command.replace(self.endpoint, len(self.endpoint) * '*').replace(self.args.username, len(self.args.username) * '*')}"
            logging.info(log_info.replace(self.password, len(self.password) * "*") if self.password else log_info)
        try:
            subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
            if self.args.command == "compare":
                self.copy_comparison_results_to_local()
            elif self.args.cluster_endpoint:
                self.convert()
        finally:
            self.cleanup()

    def convert(self) -> None:
        with TemporaryDirectory() as work_dir:
            subprocess.check_call(f"docker cp docker-container-{self.args.stack_suffix}:opensearch-benchmark/. {str(work_dir.path)}", cwd=os.getcwd(), shell=True)
            file_path = glob.glob(os.path.join(str(work_dir.path), "test_executions", "*", "test_execution.json"))
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

    def form_benchmark_command(self) -> str:
        # Pass the cluster endpoints with -t for multi-cluster use cases(e.g. cross-cluster-replication)
        self.command = f'docker run --name docker-container-{self.args.stack_suffix}'
        if self.args.benchmark_config:
            self.command += f" -v {self.args.benchmark_config}:/opensearch-benchmark/.benchmark/benchmark.ini"
        self.command += f" opensearchproject/opensearch-benchmark:1.6.0 execute-test --workload={self.args.workload} " \
                        f"--pipeline=benchmark-only --target-hosts={self.endpoint}"

        if self.args.workload_params:
            logging.info(f"Workload Params are {self.args.workload_params}")
            self.command += f" --workload-params '{self.args.workload_params}'"

        if self.args.test_procedure:
            self.command += f" --test-procedure=\"{self.args.test_procedure}\""

        if self.args.exclude_tasks:
            self.command += f" --exclude-tasks=\"{self.args.exclude_tasks}\""

        if self.args.include_tasks:
            self.command += f" --include-tasks=\"{self.args.include_tasks}\""

        if self.args.user_tag:
            user_tag = f"--user-tag=\"{self.args.user_tag}\""
            self.command += f" {user_tag}"

        if self.args.telemetry:
            self.command += " --telemetry "
            for value in self.args.telemetry:
                self.command += f"{value},"
            if self.args.telemetry_params:
                self.command += f" --telemetry-params '{self.args.telemetry_params}'"

        if self.security:
            self.command += f' --client-options="timeout:300,use_ssl:true,verify_certs:false,basic_auth_user:\'{self.args.username}\',basic_auth_password:\'{self.password}\'"'
        else:
            self.command += ' --client-options="timeout:300"'
        return self.command

    def form_compare_command(self) -> str:

        self.command = f'docker run --name docker-container-{self.args.stack_suffix} ' \
            "-v ~/.benchmark/benchmark.ini:/opensearch-benchmark/.benchmark/benchmark.ini " \
            f"opensearchproject/opensearch-benchmark:1.6.0 " \
            f"compare --baseline={self.args.baseline} --contender={self.args.contender} "

        if self.args.results_format:
            self.command += f"--results-format={self.args.results_format} "

        if self.args.results_numbers_align:
            self.command += f"--results-numbers-align={self.args.results_numbers_align} "

        if self.args.results_file:
            self.command += "--results-file=final_result.md "

        if self.args.show_in_results:
            self.command += f"--show-in-results={self.args.show_in_results} "

        return self.command

    def copy_comparison_results_to_local(self) -> None:
        with TemporaryDirectory() as work_dir:
            subprocess.check_call(
                f"docker cp docker-container-{self.args.stack_suffix}:opensearch-benchmark" f"/final_result.md {str(work_dir.path)}",
                cwd=os.getcwd(),
                shell=True,
            )
            final_results_file = glob.glob(os.path.join(str(work_dir.path), "final_result.md"))

            # construct the destination file path
            destination_dir = os.path.dirname(os.path.expanduser(self.args.results_file))
            destination_file = os.path.join(destination_dir, os.path.basename(self.args.results_file))
            # check if the destination directory exists
            if os.path.isdir(destination_dir):
                # copy the results file to the destination path
                shutil.copy(final_results_file[0], destination_file)
                print(f"Final results copied to {destination_dir}")
            else:
                print(f"Error: Destination directory '{destination_dir}' does not exist.")
