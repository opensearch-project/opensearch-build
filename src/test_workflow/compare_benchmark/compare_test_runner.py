# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os
import subprocess

from test_workflow.compare_benchmark.compare_args import CompareArgs


class CompareTestRunner:
    def __init__(self) -> None:
        self.container_name = "compare-container"

    def run_comparison(self, compare_args: CompareArgs) -> None:
        """
        Perform the comparison between two test results using the OpenSearch-Benchmark tool.
        """

        # construct the command to compare two test executions
        command = (
            f"docker run --name {self.container_name} "
            "-v ~/.benchmark/benchmark.ini:/opensearch-benchmark/.benchmark/benchmark.ini "
            f"opensearchproject/opensearch-benchmark:1.6.0 "
            f"compare --baseline={compare_args.id1} --contender={compare_args.id2} "
        )

        if compare_args.results_format:
            command += f"--results-format={compare_args.results_format} "

        if compare_args.results_numbers_align:
            command += f"--results-numbers-align={compare_args.results_numbers_align} "

        if compare_args.results_file:
            # create a temporary directory for the compare results file in the container
            container_results_dir = "/tmp/results"
            container_results_file = os.path.join(container_results_dir, os.path.basename(compare_args.results_file))
            command += f"--results-file={container_results_file} "

        if compare_args.show_in_results:
            command += f"--show-in-results={compare_args.show_in_results} "

        try:
            subprocess.run(command, shell=True, check=True)

            # copy the results directory from the container to the local machine
            local_results_dir = os.path.dirname(compare_args.results_file)
            os.makedirs(local_results_dir, exist_ok=True)

            copy_command = f"docker cp {self.container_name}:{container_results_file} {compare_args.results_file}"
            subprocess.run(copy_command, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.output}")

        finally:
            self.cleanup()

    def cleanup(self) -> None:
        subprocess.check_call(f"docker rm {self.container_name}", cwd=os.getcwd(), shell=True)
