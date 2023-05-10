# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from manifests.bundle_manifest import BundleManifest
from system import console
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_runners import BenchmarkTestRunners


def main() -> int:
    """
        Entry point for Benchmark Test with bundle manifest, config file containing the required arguments for running
        benchmarking test. Will call out in test.sh with benchmark as argument
    """
    benchmark_args = BenchmarkArgs()
    console.configure(level=benchmark_args.logging_level)
    manifest = BundleManifest.from_file(benchmark_args.bundle_manifest)
    BenchmarkTestRunners.from_args(benchmark_args, manifest).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
