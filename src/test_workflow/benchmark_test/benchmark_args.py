# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import argparse
import json
import sys
from typing import IO
from test_workflow.test_jsonargs import JsonArgs


# Contains the arguments required to run a perf test.
class BenchmarkArgs:
    bundle_manifest: IO
    stack_suffix: str
    config: IO
    keep: bool
    insecure: bool
    singleNode: bool
    minDistribution: bool
    managerNodeCount: int
    dataNodeCount: int
    clientNodeCount: int
    ingestNodeCount: int
    mlNodeCount: int
    jvmSysProps: str
    additionalConfig: json
    workload: str
    targetHosts: str

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
        parser.add_argument("--bundle-manifest", type=argparse.FileType("r"), help="Bundle Manifest file.",
                            required=True)
        parser.add_argument("--suffix", dest="suffix", help="Suffix to be added to stack name for performance test")
        parser.add_argument("--component", dest="component", default="OpenSearch",
                            help="Component name that needs to be performance tested")
        parser.add_argument("--config", type=argparse.FileType("r"), help="Config file.", required=True)
        parser.add_argument(
            "--without-security", dest="insecure", action="store_true",
            help="Force the security of the cluster to be disabled.", default=False)
        parser.add_argument("--keep", dest="keep", action="store_true",
                            help="Do not delete the working temporary directory.")
        parser.add_argument("--singleNode", dest="singleNode", action="store_true",
                            help="Is this a single node cluster")
        parser.add_argument("--minDistribution", dest="minDistribution", action="store_true", help="Is it the minimal "
                                                                                                   "OpenSearch "
                                                                                                   "distribution with "
                                                                                                   "no security and "
                                                                                                   "plugins")
        parser.add_argument("--managerNodeCount", dest="managerNodeCount", help="Number of cluster manager nodes, "
                                                                                "default is 3")
        parser.add_argument("--dataNodeCount", dest="dataNodeCount", help="Number of data nodes, default is 2")
        parser.add_argument("--clientNodeCount", dest="clientNodeCount", help="Number of dedicated client nodes, "
                                                                              "default is 0")
        parser.add_argument("--ingestNodeCount", dest="ingestNodeCount", help="Number of dedicated ingest nodes, "
                                                                              "default is 0")
        parser.add_argument("--mlNodeCount", dest="mlNodeCount", help="Number of dedicated machine learning nodes, "
                                                                      "default is 0")
        parser.add_argument("--jvmSysProps", dest="jvmSysProps", help="A comma-separated list of key=value pairs that "
                                                                      "will be added to jvm.options as JVM system "
                                                                      "properties.")
        parser.add_argument("--additionalConfig", nargs='*', action=JsonArgs, dest="additionalConfig",
                            help="Additional opensearch.yml config "
                                 "parameters passed as JSON")

        parser.add_argument("--workload", dest="workload", help="workload type for the OpenSearch benchmarking", required=True)

        args = parser.parse_args()
        self.bundle_manifest = args.bundle_manifest
        self.stack_suffix = args.suffix
        self.config = args.config
        self.keep = args.keep
        self.singleNode = args.singleNode
        self.minDistribution = args.minDistribution
        self.component = args.component
        self.insecure = args.insecure
        self.managerNodeCount = args.managerNodeCount
        self.dataNodeCount = args.dataNodeCount
        self.clientNodeCount = args.clientNodeCount
        self.ingestNodeCount = args.ingestNodeCount
        self.mlNodeCount = args.mlNodeCount
        self.jvmSysProps = args.jvmSysProps
        self.workload = args.workload

        self.additionalConfig = args.additionalConfig if args.additionalConfig is not None else None
