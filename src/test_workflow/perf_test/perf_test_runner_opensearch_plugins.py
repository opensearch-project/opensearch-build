# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess

from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from system.working_directory import WorkingDirectory
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.perf_test.perf_test_runner import PerfTestRunner


class PerfTestRunnerOpenSearchPlugins(PerfTestRunner):
    test_dir: str
    command: str

    """
      Runner to execute the performance tests for opensearch plugins. The plugins need to define the test suite
    """
    def __init__(self, args: PerfArgs, test_manifest: BundleManifest) -> None:
        super().__init__(args, test_manifest)
        self.tests_dir = os.path.join(os.getcwd(), "test-results", "perf-test", self.args.component)
        os.makedirs(self.tests_dir, exist_ok=True)
        security_flag = "--without-security" if not self.security else ""
        self.command = (
            f"bin/run_perf_test.sh --config {str(os.path.abspath(self.args.config.name))} "
            f"--bundle-manifest {str(os.path.abspath(self.args.bundle_manifest.name))} "
            f"--test-result-dir {str(self.tests_dir)} {security_flag}"
        )

    def get_plugin_repo_url(self) -> str:
        return f"https://github.com/opensearch-project/{self.args.component}.git"

    def run_tests(self) -> None:
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            current_workspace = os.path.join(work_dir.name, self.args.component)
            with GitRepository(self.get_plugin_repo_url(), "main", current_workspace):
                with WorkingDirectory(current_workspace):
                    subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
