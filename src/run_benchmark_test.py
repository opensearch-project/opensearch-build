# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_runners import BenchmarkTestRunners


def main() -> int:
    """
        Entry point for Performance Test with bundle manifest, config file containing the required arguments for running
        rally test and the stack name for the cluster. Will call out in test.sh with perf as argument
    """
    benchmark_args = BenchmarkArgs()
    print(benchmark_args.bundle_manifest, benchmark_args.singleNode, benchmark_args.insecure, benchmark_args.managerNodeCount)
    manifest = BundleManifest.from_file(benchmark_args.bundle_manifest)
    BenchmarkTestRunners.from_args(benchmark_args, manifest).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
