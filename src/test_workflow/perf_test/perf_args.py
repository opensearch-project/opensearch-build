# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import argparse
from typing import IO


# Contains the arguments required to run a perf test.
class PerfArgs:
    bundle_manifest: IO
    stack: str
    config: IO
    keep: bool
    workload: str
    workload_options: dict
    warmup_iters: int
    test_iters: int
    insecure: bool

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
        parser.add_argument("--bundle-manifest", type=argparse.FileType("r"), help="Bundle Manifest file.", required=True)
        parser.add_argument("--stack", dest="stack", help="Stack name for performance test")
        parser.add_argument("--component", dest="component", default="OpenSearch", help="Component name that needs to be performance tested")
        parser.add_argument("--config", type=argparse.FileType("r"), help="Config file.", required=True)
        parser.add_argument(
            "--without-security", dest="insecure", action="store_true",
            help="Force the security of the cluster to be disabled.", default=False)
        parser.add_argument("--keep", dest="keep", action="store_true", help="Do not delete the working temporary directory.")
        parser.add_argument("--workload", default="nyc_taxis", help="Mensor (internal client) param - Workload name from OpenSeach Benchmark Workloads")
        parser.add_argument("--workload-options", default="{}", help="Mensor (internal client) param - Json object with OpenSearch Benchmark arguments")
        parser.add_argument("--warmup-iters", default=0, help="Mensor (internal client) param - Number of times to run a workload before collecting data")
        parser.add_argument("--test-iters", default=1, help="Mensor (internal client) param - Number of times to run a workload")
        args = parser.parse_args()
        self.bundle_manifest = args.bundle_manifest
        self.stack = args.stack
        self.config = args.config
        self.keep = args.keep
        self.workload = args.workload
        self.workload_options = args.workload_options
        self.warmup_iters = args.warmup_iters
        self.test_iters = args.test_iters
        self.component = args.component
        self.insecure = args.insecure
