# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import os
from typing import Union

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs


class BenchmarkTestRunner(abc.ABC):
    args: BenchmarkArgs
    test_manifest: Union[BundleManifest, BuildManifest]
    security: bool
    tests_dir: str

    def __init__(self, args: BenchmarkArgs, test_manifest: Union[BundleManifest, BuildManifest]) -> None:
        self.args = args
        self.test_manifest = test_manifest

        if self.test_manifest:
            self.security = "security" in self.test_manifest.components and not self.args.insecure
        else:
            self.security = False

        self.tests_dir = os.path.join(os.getcwd(), "test-results", "benchmark-test",
                                      f"{'with' if self.security else 'without'}-security")
        os.makedirs(self.tests_dir, exist_ok=True)

    @abc.abstractmethod
    def run_tests(self) -> None:
        pass

    def run(self) -> None:
        self.run_tests()

    def get_git_ref(self) -> str:
        if self.test_manifest:
            os_major_version = self.test_manifest.build.version.split(".")[0]
            if os_major_version in ['2', '3']:
                return 'main'
            else:
                return '1.x'
        else:
            os_major_version = self.args.distribution_version.split(".")[0]
            if os_major_version in ['2', '3']:
                return 'main'
            else:
                return '1.x'
