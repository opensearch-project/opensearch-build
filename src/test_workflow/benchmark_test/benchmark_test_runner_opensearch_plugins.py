# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
from typing import Union

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_runner import BenchmarkTestRunner


class BenchmarkTestRunnerOpenSearchPlugins(BenchmarkTestRunner):
    test_dir: str
    command: str

    """
      Runner to execute the performance tests for opensearch plugins. The plugins need to define the test suite
    """
    def __init__(self, args: BenchmarkArgs, test_manifest: Union[BundleManifest, BuildManifest]) -> None:
        super().__init__(args, test_manifest)

    def get_plugin_repo_url(self) -> str:
        return f"https://github.com/opensearch-project/{self.args.component}.git"

    def run_tests(self) -> None:
        pass
