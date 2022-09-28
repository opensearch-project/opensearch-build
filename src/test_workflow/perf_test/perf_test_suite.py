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
from test_workflow.perf_test.perf_args import PerfArgs


class PerfTestSuite:
    manifest: BundleManifest
    work_dir: str
    endpoint: dict
    security: bool
    current_workspace: str
    args: PerfArgs
    command: str

    """
    Represents a performance test suite. This class runs rally test on the deployed cluster with the provided IP.
    """
    def __init__(
        self,
        bundle_manifest: BundleManifest,
        endpoint: Any,
        security: bool,
        current_workspace: str,
        test_results_path: str,
        args: PerfArgs,
        owner: str = "opensearch-devops",
        scenario: str = "DEFAULT"
    ) -> None:
        self.manifest = bundle_manifest
        self.work_dir = current_workspace + "/mensor/"
        self.endpoint = endpoint
        self.security = security
        self.current_workspace = current_workspace
        self.args = args
        endpoint_arg = ""
        # Pass the cluster endpoints with -t for multi-cluster use cases(e.g. cross-cluster-replication)
        if type(self.endpoint) is dict:
            endpoint_arg = "-t '{}'".format(json.dumps(self.endpoint))
        else:
            endpoint_arg = "-e {}".format(self.endpoint)
        self.command = (
            f"pipenv run python test_config.py {endpoint_arg} -b {self.manifest.build.id}"
            f" -a {self.manifest.build.architecture} -p {os.getcwd() if test_results_path is None else test_results_path}"
            f" --workload {self.args.workload} --workload-options '{self.args.workload_options}'"
            f" --warmup-iters {self.args.warmup_iters} --test-iters {self.args.test_iters}"
            f" --scenario-type {scenario} --owner {owner}"
        )

    def execute(self) -> None:
        try:
            current_workspace = os.path.join(self.current_workspace, self.work_dir)
            with WorkingDirectory(current_workspace):
                subprocess.check_call("pipenv install", cwd=current_workspace, shell=True)
                if self.security:
                    subprocess.check_call(f"{self.command} -s", cwd=current_workspace, shell=True)
                else:
                    subprocess.check_call(f"{self.command}", cwd=current_workspace, shell=True)
        finally:
            os.chdir(self.current_workspace)
