# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import os
import subprocess
import sys

import yaml

from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from system.working_directory import WorkingDirectory
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.perf_test.perf_test_cluster import PerfTestCluster
from test_workflow.perf_test.perf_test_runner import PerfTestRunner
from test_workflow.perf_test.perf_test_suite import PerfTestSuite

"""
  Runner to execute the performance tests for opensearch plugins. The plugins need to define the test suite
"""
class PerfTestRunnerOpenSearchPlugins(PerfTestRunner):
    def __init__(self, args: PerfArgs, test_manifest: BundleManifest):
        super().__init__(args, test_manifest)
        self.command = (
            f"python3 run_perf_test.py --config {yaml.safe_load(self.args.config)} "
            f"--bundle-manifest {str(self.args.bundle_manifest.name)}"
        )

    def get_plugin_repo_url(self):
        if "GITHUB_TOKEN" in os.environ:
            return f"https://${GITHUB_TOKEN}@github.com/opensearch-project/{self.args.component}.git"
        return f"https://github.com/opensearch-project/{self.args.component}.git"

    def run_tests(self):
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            current_workspace = os.path.join(work_dir.name, "plugin")
            with GitRepository(self.get_plugin_repo_url(), "main", current_workspace):
                with WorkingDirectory(current_workspace):
                    if self.security:
                        subprocess.check_call(f"{self.command} -s", cwd=os.getcwd(), shell=True)
                    else:
                        subprocess.check_call(f"{self.command}", cwd=os.getcwd(), shell=True)
