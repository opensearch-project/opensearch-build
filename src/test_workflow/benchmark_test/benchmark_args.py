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
import logging
from typing import IO

from test_workflow.json_args import JsonArgs


# Contains the arguments required to run a perf test.
class BenchmarkArgs:
    bundle_manifest: IO
    stack_suffix: str
    config: IO
    keep: bool
    insecure: bool
    single_node: bool
    min_distribution: bool
    manager_node_count: int
    data_node_count: int
    client_node_count: int
    ingest_node_count: int
    ml_node_count: int
    data_node_storage: int
    ml_node_storage: int
    jvm_sys_props: str
    additional_config: str
    data_instance_type: str
    use_50_percent_heap: bool
    enable_remote_store: bool
    workload: str
    workload_params: str
    benchmark_config: IO
    user_tag: str
    target_hosts: str
    telemetry: list
    logging_level: int

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
        parser.add_argument("--bundle-manifest", type=argparse.FileType("r"), help="Bundle Manifest file.",
                            required=True)
        parser.add_argument("--suffix", dest="suffix", help="Suffix to be added to stack name for performance test")
        parser.add_argument("--component", dest="component", default="OpenSearch",
                            help="Component name that needs to be performance tested")
        parser.add_argument("--config", type=argparse.FileType("r"), help="Config file.", required=True)
        parser.add_argument("--without-security", dest="insecure", action="store_true",
                            help="Force the security of the cluster to be disabled.", default=False)
        parser.add_argument("--keep", dest="keep", action="store_true",
                            help="Do not delete the working temporary directory.")
        parser.add_argument("--single-node", dest="single_node", action="store_true",
                            help="Is this a single node cluster")
        parser.add_argument("--min-distribution", dest="min_distribution", action="store_true",
                            help="Is it the minimal OpenSearch distribution with no security and plugins")
        parser.add_argument("--manager-node-count", dest="manager_node_count",
                            help="Number of cluster manager nodes, default is 3")
        parser.add_argument("--data-node-count", dest="data_node_count", help="Number of data nodes, default is 2")
        parser.add_argument("--client-node-count", dest="client_node_count",
                            help="Number of dedicated client nodes, default is 0")
        parser.add_argument("--ingest-node-count", dest="ingest_node_count",
                            help="Number of dedicated ingest nodes, default is 0")
        parser.add_argument("--ml-node-count", dest="ml_node_count",
                            help="Number of dedicated machine learning nodes, default is 0")
        parser.add_argument("--jvm-sys-props", dest="jvm_sys_props",
                            help="A comma-separated list of key=value pairs that will be added to jvm.options as JVM system properties.")
        parser.add_argument("--additional-config", nargs='*', action=JsonArgs, dest="additional_config",
                            help="Additional opensearch.yml config parameters passed as JSON")
        parser.add_argument("--use-50-percent-heap", dest="use_50_percent_heap", action="store_true",
                            help="Use 50 percent of physical memory as heap.")
        parser.add_argument("--ml-node-storage", dest="ml_node_storage",
                            help="User provided ml-node ebs block storage size defaults to 100Gb")
        parser.add_argument("--data-node-storage", dest="data_node_storage",
                            help="User provided data-node ebs block storage size, defaults to 100Gb")
        parser.add_argument("--enable-remote-store", dest="enable_remote_store", action="store_true",
                            help="Enable Remote Store feature in OpenSearch")
        parser.add_argument("--data-instance-type", dest="data_instance_type",
                            help="EC2 instance type for data node, defaults to r5.xlarge.")
        parser.add_argument("--workload", dest="workload", required=True,
                            help="Name of the workload that OpenSearch Benchmark should run")
        parser.add_argument("--benchmark-config", dest="benchmark_config",
                            help="absolute filepath to custom benchmark.ini config")
        parser.add_argument("--user-tag", dest="user_tag",
                            help="Attach arbitrary text to the meta-data of each metric record")
        parser.add_argument("--workload-params", dest="workload_params",
                            help="With this parameter you can inject variables into workloads. Parameters differs "
                                 "for each workload type. e.g., --workload-params \"number_of_replicas:1,number_of_shards:5\"")
        parser.add_argument("--capture-node-stat", dest="telemetry", action="append_const", const="node-stats",
                            help="Enable opensearch-benchmark to capture node stat metrics such as cpu, mem, jvm etc as well.")
        parser.add_argument("--capture-segment-replication-stat", dest="telemetry", action="append_const",
                            const="segment-replication-stats",
                            help="Enable opensearch-benchmark to segment_replication stat metrics such as replication lag.")
        parser.add_argument("-v", "--verbose", help="Show more verbose output.", action="store_const", default=logging.INFO,
                            const=logging.DEBUG, dest="logging_level")

        args = parser.parse_args()
        self.bundle_manifest = args.bundle_manifest
        self.stack_suffix = args.suffix if args.suffix else None
        self.config = args.config
        self.keep = args.keep
        self.single_node = args.single_node
        self.min_distribution = args.min_distribution
        self.component = args.component
        self.insecure = args.insecure
        self.manager_node_count = args.manager_node_count if args.manager_node_count else None
        self.data_node_count = args.data_node_count if args.data_node_count else None
        self.client_node_count = args.client_node_count if args.client_node_count else None
        self.ingest_node_count = args.ingest_node_count if args.ingest_node_count else None
        self.ml_node_count = args.ml_node_count if args.ml_node_count else None
        self.jvm_sys_props = args.jvm_sys_props if args.jvm_sys_props else None
        self.data_node_storage = args.data_node_storage if args.data_node_storage else None
        self.ml_node_storage = args.ml_node_storage if args.ml_node_storage else None
        self.enable_remote_store = args.enable_remote_store
        self.data_instance_type = args.data_instance_type if args.data_instance_type else None
        self.workload = args.workload
        self.workload_params = args.workload_params if args.workload_params else None
        self.benchmark_config = args.benchmark_config if args.benchmark_config else None
        self.user_tag = args.user_tag if args.user_tag else None
        self.additional_config = json.dumps(args.additional_config) if args.additional_config is not None else None
        self.use_50_percent_heap = args.use_50_percent_heap
        self.telemetry = args.telemetry
        self.logging_level = args.logging_level
