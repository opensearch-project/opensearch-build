# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import json
import os
import subprocess
from typing import Any

from manifests.bundle_manifest import BundleManifest
from system.working_directory import WorkingDirectory
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
        self.command = (
            f"docker run opensearch-benchmark:latest execute_test "
            f"--workload={self.args.workload} --test-mode --pipeline=benchmark-only --target-hosts={endpoint}"
        )
        print(self.command)

    def execute(self) -> None:
        if self.security:
            self.command += ' --client-options="use_ssl:true,verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'admin\'"'

        print(self.command)
        subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)

