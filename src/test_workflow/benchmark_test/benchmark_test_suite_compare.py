# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_suite import BenchmarkTestSuite


class BenchmarkTestSuiteCompare(BenchmarkTestSuite):
    def __init__(self, args: BenchmarkArgs):
        super().__init__(args)
        self.command = ""

    def execute(self) -> None:
        self.form_command()
        try:
            subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
            self.copy_comparison_results_to_local()
        finally:
            self.cleanup()

    def form_command(self) -> str:
        command = f'docker run --name docker-container-{self.args.stack_suffix} ' \
                  "-v ~/.benchmark/benchmark.ini:/opensearch-benchmark/.benchmark/benchmark.ini " \
                  f"opensearchproject/opensearch-benchmark:1.6.0 " \
                  f"compare --baseline={self.args.baseline} --contender={self.args.contender} "

        if self.args.results_format:
            command += f"--results-format={self.args.results_format} "

        if self.args.results_numbers_align:
            command += f"--results-numbers-align={self.args.results_numbers_align} "

        command += "--results-file=final_result.md "

        if self.args.show_in_results:
            command += f"--show-in-results={self.args.show_in_results} "

        self.command = command
        return self.command

    def copy_comparison_results_to_local(self) -> None:
        try:
            subprocess.check_call(
                f"docker cp docker-container-{self.args.stack_suffix}:opensearch-benchmark" f"/final_result.md {str(os.getcwd())}/final_result_{self.args.stack_suffix}.md",
                cwd=os.getcwd(),
                shell=True,
            )
            logging.info(f"Final results copied to {str(os.getcwd())}/final_result_{self.args.stack_suffix}.md")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to copy results: {e}")
            raise
