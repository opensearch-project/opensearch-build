# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

import yaml
from retry.api import retry_call  # type: ignore

from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from system.working_directory import WorkingDirectory
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.perf_test.perf_single_node_cluster import PerfSingleNodeCluster
from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig
from test_workflow.perf_test.perf_test_runner import PerfTestRunner
from test_workflow.perf_test.perf_test_suite import PerfTestSuite


class PerfTestRunnerOpenSearch(PerfTestRunner):
    """
      Runner to execute the performance tests for opensearch.
    """
    def __init__(self, args: PerfArgs, test_manifest: BundleManifest) -> None:
        super().__init__(args, test_manifest)
        logging.info("Running opensearch tests")

    def get_infra_repo_url(self) -> str:
        if "GITHUB_TOKEN" in os.environ:
            return "https://${GITHUB_TOKEN}@github.com/opensearch-project/opensearch-infra.git"
        return "https://github.com/opensearch-project/opensearch-infra.git"

    def run_tests(self) -> None:
        config = yaml.safe_load(self.args.config)
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            current_workspace = os.path.join(work_dir.name, "infra")
            logging.info("current_workspace is " + str(current_workspace))
            with GitRepository(self.get_infra_repo_url(), "main", current_workspace):
                with WorkingDirectory(current_workspace):
                    with PerfSingleNodeCluster.create(self.test_manifest, config, self.args.stack, PerfTestClusterConfig(self.security), current_workspace) as test_cluster:
                        perf_test_suite = PerfTestSuite(self.test_manifest, test_cluster.endpoint_with_port, self.security, current_workspace, self.tests_dir, self.args)
                        retry_call(perf_test_suite.execute, tries=3, delay=60, backoff=2)
