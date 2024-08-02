# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import os
import shutil
import subprocess

from system.temporary_directory import TemporaryDirectory
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

        if self.args.results_file:
            command += "--results-file=final_result.md "

        if self.args.show_in_results:
            command += f"--show-in-results={self.args.show_in_results} "

        self.command = command
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
            # convert destination_file to Unix-style path
            unix_style_destination_file = destination_file.replace('\\', '/')
            # check if the destination directory exists
            if os.path.isdir(destination_dir):
                # copy the results file to the destination path
                shutil.copy(final_results_file[0], unix_style_destination_file)
                print(f"Final results copied to {destination_dir}")
            else:
                print(f"Error: Destination directory '{destination_dir}' does not exist.")
