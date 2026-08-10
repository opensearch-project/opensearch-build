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
import shlex
import shutil
import subprocess
from typing import Any, Dict, List

import pandas as pd

from system.temporary_directory import TemporaryDirectory
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_suite import BenchmarkTestSuite


class BenchmarkTestSuiteExecute(BenchmarkTestSuite):

    DATA_WORKLOADS: List[str] = []

    def __init__(self, endpoint: Any, security: bool, args: BenchmarkArgs, password: str):
        super().__init__(args, endpoint, security, password)

    def execute(self) -> None:
        self.form_command()
        log_info = f"Executing {self.command}"
        for host in self.hosts_to_mask():
            log_info = log_info.replace(host, len(host) * "*")
        log_info = log_info.replace(self.args.username, len(self.args.username) * "*")
        logging.info(log_info.replace(self.password, len(self.password) * "*") if self.password else log_info)
        try:
            subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
            if self.args.cluster_endpoint or self.args.distribution_url:
                self.convert()
        finally:
            self.cleanup()

    def hosts_to_mask(self) -> List[str]:
        # For a multi-cluster run the endpoint is a role -> host/port mapping, mask every host in it.
        if isinstance(self.endpoint, dict):
            return [str(host["host"]) for hosts in self.endpoint.values() for host in hosts]
        return [str(self.endpoint)]

    def form_command(self) -> str:
        self.command = f'docker run --user root --name docker-container-{self.args.stack_suffix}'

        if self.security and self.args.sigv4:
            self.command += ' -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN'

        if self.args.benchmark_config:
            self.command += f" -v {self.args.benchmark_config}:/root/.benchmark/benchmark.ini"

        if self.args.workload in self.DATA_WORKLOADS:
            self.command += (
                f" -v /home/ec2-user/.benchmark/benchmarks/data/{self.args.workload}"
                f":/opensearch-benchmark/{self.args.workload}"
            )

        self.command += f" mayhem6788/opensearch-benchmark:1.21.0 execute-test --workload={self.args.workload} " \
                        f"--pipeline=benchmark-only --target-hosts={self.target_hosts()}"

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
            self.command += f" --telemetry {','.join(self.args.telemetry)}"
            if self.args.telemetry_params:
                self.command += f" --telemetry-params '{self.args.telemetry_params}'"

        self.command += f' --client-options={self.client_options()} --results-file=final_result.md'
        return self.command

    def target_hosts(self) -> str:
        # Pass the cluster endpoints as a role -> hosts mapping for multi-cluster use cases
        # (e.g. cross-cluster-replication, where 'default' is the leader), otherwise a single host:port.
        if isinstance(self.endpoint, dict):
            return shlex.quote(json.dumps(self.endpoint))
        return str(self.endpoint)

    def client_options(self) -> str:
        # Both clusters of a multi-cluster run share the same credentials, so the same options
        # are applied to every role.
        if isinstance(self.endpoint, dict):
            options = {role: self.client_options_dict() for role in self.endpoint}
            return shlex.quote(json.dumps(options))

        if self.security and self.args.sigv4:
            return f'"retry_on_timeout:False,timeout:120,amazon_aws_log_in:session,region:{self.args.region},service:{self.args.service}"'
        elif self.security:
            return (f'"retry_on_timeout:False,timeout:120,use_ssl:true,verify_certs:false,basic_auth_user:\'{self.args.username}\','
                    f'basic_auth_password:\'{self.password}\'"')
        return '"timeout:120"'

    def client_options_dict(self) -> Dict[str, Any]:
        if self.security and self.args.sigv4:
            return {
                "retry_on_timeout": False,
                "timeout": 120,
                "amazon_aws_log_in": "session",
                "region": self.args.region,
                "service": self.args.service,
            }
        elif self.security:
            return {
                "retry_on_timeout": False,
                "timeout": 120,
                "use_ssl": True,
                "verify_certs": False,
                "basic_auth_user": self.args.username,
                "basic_auth_password": self.password,
            }
        return {"timeout": 120}

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
