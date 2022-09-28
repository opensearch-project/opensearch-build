# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.perf_test.perf_test_runner import PerfTestRunner
from test_workflow.perf_test.perf_test_runner_opensearch import PerfTestRunnerOpenSearch
from test_workflow.perf_test.perf_test_runner_opensearch_plugins import PerfTestRunnerOpenSearchPlugins


class PerfTestRunners:
    RUNNERS = {
        "OpenSearch": PerfTestRunnerOpenSearch,
        "OpenSearch Plugin": PerfTestRunnerOpenSearchPlugins
    }

    @classmethod
    def from_args(cls, args: PerfArgs, test_manifest: BundleManifest) -> PerfTestRunner:
        return cls.RUNNERS.get(args.component, PerfTestRunnerOpenSearchPlugins)(args, test_manifest)
