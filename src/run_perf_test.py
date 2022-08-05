# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.perf_test.perf_test_runners import PerfTestRunners


def main() -> int:
    """
        Entry point for Performance Test with bundle manifest, config file containing the required arguments for running
        rally test and the stack name for the cluster. Will call out in test.sh with perf as argument
    """
    perf_args = PerfArgs()
    manifest = BundleManifest.from_file(perf_args.bundle_manifest)
    PerfTestRunners.from_args(perf_args, manifest).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
