# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import os

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_args import PerfArgs


class PerfTestRunner(abc.ABC):
    args: PerfArgs
    test_manifest: BundleManifest
    security: bool
    tests_dir: str

    def __init__(self, args: PerfArgs, test_manifest: BundleManifest) -> None:
        self.args = args
        self.test_manifest = test_manifest

        self.security = "security" in self.test_manifest.components and not self.args.insecure
        self.tests_dir = os.path.join(os.getcwd(), "test-results", "perf-test", f"{'with' if self.security else 'without'}-security")
        os.makedirs(self.tests_dir, exist_ok=True)

    @abc.abstractmethod
    def run_tests(self) -> None:
        pass

    def run(self) -> None:
        self.run_tests()
