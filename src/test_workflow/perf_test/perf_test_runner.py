# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


class PerfTestRunner(abc.ABC):
    def __init__(self, args: PerfArgs, test_manifest: BundleManifest):
        self.args = args
        self.test_manifest = test_manifest

        self.security = "security" in self.test_manifest.components and not self.args.insecure
        tests_dir = os.path.join(os.getcwd(), "test-results", "perf-test", f"{'with' if security else 'without'}-security")
        os.makedirs(tests_dir, exist_ok=True)

    def run(self):
        self.run_tests()
