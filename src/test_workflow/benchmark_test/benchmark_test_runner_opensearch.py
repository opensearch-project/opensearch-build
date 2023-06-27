# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import Union

import yaml
from retry.api import retry_call  # type: ignore

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from system.working_directory import WorkingDirectory
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_cluster import BenchmarkTestCluster
from test_workflow.benchmark_test.benchmark_test_runner import BenchmarkTestRunner
from test_workflow.benchmark_test.benchmark_test_suite import BenchmarkTestSuite


class BenchmarkTestRunnerOpenSearch(BenchmarkTestRunner):
    """
      Runner to execute the performance tests for opensearch.
    """
    def __init__(self, args: BenchmarkArgs, test_manifest: Union[BundleManifest, BuildManifest]) -> None:
        super().__init__(args, test_manifest)
        logging.info("Running opensearch tests")

    def get_cluster_repo_url(self) -> str:
        if "GITHUB_TOKEN" in os.environ:
            return "https://${GITHUB_TOKEN}@github.com/opensearch-project/opensearch-cluster-cdk.git"
        return "https://github.com/opensearch-project/opensearch-cluster-cdk.git"

    def run_tests(self) -> None:
        config = yaml.safe_load(self.args.config)

        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            current_workspace = os.path.join(work_dir.name, "opensearch-cluster-cdk")
            with GitRepository(self.get_cluster_repo_url(), "main", current_workspace):
                with WorkingDirectory(current_workspace):
                    with BenchmarkTestCluster.create(self.test_manifest, config, self.args, current_workspace) as test_cluster:
                        benchmark_test_suite = BenchmarkTestSuite(test_cluster.endpoint_with_port, self.security, self.args)
                        retry_call(benchmark_test_suite.execute, tries=3, delay=60, backoff=2)
