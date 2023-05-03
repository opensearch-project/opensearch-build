# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_runner import BenchmarkTestRunner
from test_workflow.benchmark_test.benchmark_test_runner_opensearch import BenchmarkTestRunnerOpenSearch
from test_workflow.benchmark_test.benchmark_test_runner_opensearch_plugins import BenchmarkTestRunnerOpenSearchPlugins


class BenchmarkTestRunners:
    RUNNERS = {
        "OpenSearch": BenchmarkTestRunnerOpenSearch,
        "OpenSearch Plugin": BenchmarkTestRunnerOpenSearchPlugins
    }

    @classmethod
    def from_args(cls, args: BenchmarkArgs, test_manifest: BundleManifest) -> BenchmarkTestRunner:
        return cls.RUNNERS.get(args.component, BenchmarkTestRunnerOpenSearchPlugins)(args, test_manifest)
