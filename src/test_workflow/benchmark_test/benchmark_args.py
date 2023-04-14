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
    dataNodeStorage: int
    mlNodeStorage: int
    jvmSysProps: str
    additionalConfig: json
    workload: str
    benchmarkConfig: IO
    userTag: str
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
        parser.add_argument("--mlNodeStorage", dest="mlNodeStorage", help="User provided ml-node ebs block storage size"
                                                                          " defaults to 100Gb")
        parser.add_argument("--dataNodeStorage", dest="dataNodeStorage", help="User provided data-node ebs block "
                                                                              "storage size, defaults to 100Gb")

        parser.add_argument("--workload", dest="workload", help="workload type for the OpenSearch benchmarking", required=True)
        parser.add_argument("--benchmark-config", dest="benchmarkConfig", help="absolute filepath to custom "
                                                                               "opensearch-benchmark.ini config")
        parser.add_argument("--user-tag", dest="userTag", help="Attach arbitrary text to the meta-data of each metric record")

        args = parser.parse_args()
        self.bundle_manifest = args.bundle_manifest
        self.stack_suffix = args.suffix if args.suffix else None
        self.config = args.config
        self.keep = args.keep
        self.singleNode = args.singleNode
        self.minDistribution = args.minDistribution
        self.component = args.component
        self.insecure = args.insecure
        self.managerNodeCount = args.managerNodeCount if args.managerNodeCount else None
        self.dataNodeCount = args.dataNodeCount if args.dataNodeCount else None
        self.clientNodeCount = args.clientNodeCount if args.clientNodeCount else None
        self.ingestNodeCount = args.ingestNodeCount if args.ingestNodeCount else None
        self.mlNodeCount = args.mlNodeCount if args.mlNodeCount else None
        self.jvmSysProps = args.jvmSysProps if args.jvmSysProps else None
        self.dataNodeStorage = args.dataNodeStorage if args.dataNodeStorage else None
        self.mlNodeStorage = args.mlNodeStorage if args.mlNodeStorage else None
        self.workload = args.workload
        self.benchmarkConfig = args.benchmarkConfig if args.benchmarkConfig else None
        self.userTag = args.userTag if args.userTag else None
        self.additionalConfig = json.dumps(args.additionalConfig) if args.additionalConfig is not None else None
        #sys.exit(0)


