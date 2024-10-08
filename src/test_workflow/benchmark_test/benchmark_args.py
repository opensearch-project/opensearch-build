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
    cluster_endpoint: str
    distribution_url: str
    distribution_version: str
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
    test_procedure: str
    exclude_tasks: str
    include_tasks: str
    benchmark_config: IO
    user_tag: str
    target_hosts: str
    telemetry: list
    telemetry_params: str
    logging_level: int
    baseline: str
    contender: str
    results_format: str
    results_numbers_align: str
    results_file: str
    show_in_results: str
    command: str
    enable_instance_storage: bool

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle or compare two tests")
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument("--suffix", dest="suffix",
                                   help="Suffix to be added to stack name for performance test")

        parent_parser.add_argument("--benchmark-config", dest="benchmark_config",
                                   help="absolute filepath to custom benchmark.ini config")

        subparsers = parser.add_subparsers(dest="command", required=True,
                                           help="Please provide either 'execute-test' to run benchmark or 'compare' command to compare benchmark runs.")
        # command to run a benchmark test
        execute_test_parser = subparsers.add_parser("execute-test",
                                                    help="Execute benchmark test", parents=[parent_parser])
        execute_test_parser.add_argument("--bundle-manifest", type=argparse.FileType("r"),
                                         help="Bundle Manifest file.")
        execute_test_parser.add_argument("--distribution-url", dest="distribution_url",
                                         help="Link to a downloadable OpenSearch tarball.")
        execute_test_parser.add_argument("--cluster-endpoint", dest="cluster_endpoint",
                                         help="Load balancer url for benchmark testing")
        execute_test_parser.add_argument("--distribution-version", dest="distribution_version",
                                         help="provide OpenSearch version if using distribution-url param.")
        execute_test_parser.add_argument("--username", dest="username",
                                         help="Username for the cluster")
        execute_test_parser.add_argument("--password", dest="password",
                                         help="Password for the cluster")
        execute_test_parser.add_argument("--component", dest="component", default="OpenSearch",
                                         help="Component name that needs to be performance tested")
        execute_test_parser.add_argument("--config", type=argparse.FileType("r"),
                                         help="Config file.")
        execute_test_parser.add_argument("--without-security", dest="insecure", action="store_true",
                                         help="Force the security of the cluster to be disabled.", default=False)
        execute_test_parser.add_argument("--keep", dest="keep", action="store_true",
                                         help="Do not delete the working temporary directory.")
        execute_test_parser.add_argument("--single-node", dest="single_node", action="store_true",
                                         help="Is this a single node cluster")
        execute_test_parser.add_argument("--min-distribution", dest="min_distribution", action="store_true",
                                         help="Is it the minimal OpenSearch distribution with no security and plugins")
        execute_test_parser.add_argument("--manager-node-count", dest="manager_node_count",
                                         help="Number of cluster manager nodes, default is 3")
        execute_test_parser.add_argument("--data-node-count", dest="data_node_count",
                                         help="Number of data nodes, default is 2")
        execute_test_parser.add_argument("--client-node-count", dest="client_node_count",
                                         help="Number of dedicated client nodes, default is 0")
        execute_test_parser.add_argument("--ingest-node-count", dest="ingest_node_count",
                                         help="Number of dedicated ingest nodes, default is 0")
        execute_test_parser.add_argument("--ml-node-count", dest="ml_node_count",
                                         help="Number of dedicated machine learning nodes, default is 0")
        execute_test_parser.add_argument("--jvm-sys-props", dest="jvm_sys_props",
                                         help="A comma-separated list of key=value pairs that will be added to jvm.options as JVM system properties.")
        execute_test_parser.add_argument("--additional-config", nargs="*", action=JsonArgs, dest="additional_config",
                                         help="Additional opensearch.yml config parameters passed as JSON")
        execute_test_parser.add_argument("--use-50-percent-heap", dest="use_50_percent_heap", action="store_true",
                                         help="Use 50 percent of physical memory as heap.")
        execute_test_parser.add_argument("--data-node-storage", dest="data_node_storage",
                                         help="User provided data-node ebs block storage size, defaults to 100Gb")
        execute_test_parser.add_argument("--enable-remote-store", dest="enable_remote_store", action="store_true",
                                         help="Enable Remote Store feature in OpenSearch")
        execute_test_parser.add_argument("--data-instance-type", dest="data_instance_type",
                                         help="EC2 instance type for data node, defaults to r5.xlarge.")
        execute_test_parser.add_argument("--workload", dest="workload", required=True,
                                         help="Name of the workload that OpenSearch Benchmark should run")
        execute_test_parser.add_argument("--user-tag", dest="user_tag",
                                         help="Attach arbitrary text to the meta-data of each metric record")
        execute_test_parser.add_argument("--workload-params", dest="workload_params",
                                         help="With this parameter you can inject variables into workloads. Parameters differs "
                                              'for each workload type. e.g., --workload-params "number_of_replicas:1,number_of_shards:5"')
        execute_test_parser.add_argument("--test-procedure", dest="test_procedure",
                                         help="Defines a test procedure to use. You can find a list of test procedures by using "
                                              'opensearch-benchmark list test-procedures. E.g. --test-procedure="ingest-only"')
        execute_test_parser.add_argument("--exclude-tasks", dest="exclude_tasks",
                                         help='Defines a comma-separated list of test procedure tasks not to run. E.g. --exclude-tasks="index-append"')
        execute_test_parser.add_argument("--include-tasks", dest="include_tasks",
                                         help="Defines a comma-separated list of test procedure tasks to run. By default, all tasks listed in a test procedure array are run."
                                              ' E.g. --include-tasks="scroll"',)
        execute_test_parser.add_argument("--capture-node-stat", dest="telemetry", action="append_const", const="node-stats",
                                         help="Enable opensearch-benchmark to capture node stat metrics such as cpu, mem, jvm etc as well.")
        execute_test_parser.add_argument("--capture-segment-replication-stat", dest="telemetry", action="append_const", const="segment-replication-stats",
                                         help="Enable opensearch-benchmark to segment_replication stat metrics such as replication lag.")
        execute_test_parser.add_argument("--telemetry-params", dest="telemetry_params",
                                         help="Allows to set parameters for telemetry devices. Accepts json input.")
        execute_test_parser.add_argument("-v", "--verbose", action="store_const", default=logging.INFO, const=logging.DEBUG, dest="logging_level",
                                         help="Show more verbose output.")
        execute_test_parser.add_argument("--ml-node-storage", dest="ml_node_storage",
                                         help="User provided ml-node ebs block storage size defaults to 100Gb")
        execute_test_parser.add_argument("--enable-instance-storage", dest="enable_instance_storage", action="store_true",
                                         help="Use instance based SSD storage instead of EBS for data nodes", default=False)

        # command to run comparison
        compare_parser = subparsers.add_parser("compare", parents=[parent_parser],
                                               help="Compare two tests using their test execution IDs")
        compare_parser.add_argument("baseline", type=str, help="The baseline ID to compare", nargs='?')
        compare_parser.add_argument("contender", type=str, help="The contender ID to compare", nargs='?')
        compare_parser.add_argument("--results-format", default="markdown", type=str,
                                    help="Defines the output format for the results, markdown or csv (default: markdown)")
        compare_parser.add_argument("--results-numbers-align", default="right", type=str,
                                    help="Defines the format for the command line results. (Default: right)")
        compare_parser.add_argument("--show-in-results", type=str,
                                    help="Determines whether to include the comparison in the results file")
        compare_parser.add_argument("-v", "--verbose", action="store_const", default=logging.INFO, const=logging.DEBUG, dest="logging_level",
                                    help="Show more verbose output.")

        args = parser.parse_args()
        self.command = args.command
        self.stack_suffix = args.suffix if args.suffix else None
        self.benchmark_config = args.benchmark_config if args.benchmark_config else None

        if args.command == "execute-test":
            self.bundle_manifest = args.bundle_manifest if args.bundle_manifest else None
            self.distribution_url = args.distribution_url if args.distribution_url else None
            self.cluster_endpoint = args.cluster_endpoint if args.cluster_endpoint else None
            self.distribution_version = args.distribution_version if args.distribution_version else None
            self.config = args.config
            self.keep = args.keep
            self.single_node = args.single_node
            self.min_distribution = args.min_distribution
            self.component = args.component
            self.insecure = args.insecure
            self.username = args.username if args.username else "admin"
            self.password = args.password if args.password else None
            self.manager_node_count = args.manager_node_count if args.manager_node_count else None
            self.data_node_count = args.data_node_count if args.data_node_count else None
            self.client_node_count = args.client_node_count if args.client_node_count else None
            self.ingest_node_count = args.ingest_node_count if args.ingest_node_count else None
            self.ml_node_count = args.ml_node_count if args.ml_node_count else None
            self.jvm_sys_props = args.jvm_sys_props if args.jvm_sys_props else None
            self.data_node_storage = args.data_node_storage if args.data_node_storage else None
            self.ml_node_storage = args.ml_node_storage if args.ml_node_storage else None
            self.enable_instance_storage = args.enable_instance_storage
            self.enable_remote_store = args.enable_remote_store
            self.data_instance_type = args.data_instance_type if args.data_instance_type else None
            self.workload = args.workload
            self.workload_params = args.workload_params if args.workload_params else None
            self.test_procedure = args.test_procedure if args.test_procedure else None
            self.exclude_tasks = args.exclude_tasks if args.exclude_tasks else None
            self.include_tasks = args.include_tasks if args.include_tasks else None
            self.user_tag = args.user_tag if args.user_tag else None
            self.additional_config = json.dumps(args.additional_config) if args.additional_config is not None else None
            self.use_50_percent_heap = args.use_50_percent_heap
            self.telemetry = args.telemetry
            self.telemetry_params = args.telemetry_params if args.telemetry_params else None
            self.logging_level = args.logging_level

            if self.bundle_manifest is None and self.distribution_url is None and self.cluster_endpoint is None:
                raise Exception("Please provide either --bundle-manifest or --distribution-url  or --cluster_endpoint to run the performance test.")
            elif self.distribution_url and self.distribution_version is None:
                raise Exception("--distribution-version is required parameter while using --distribution-url param.")

        elif args.command == "compare":
            if not args.baseline or not args.contender:
                raise ValueError("Both 'baseline' and 'contender' arguments are required for the 'compare' command.")
            self.baseline = args.baseline
            self.contender = args.contender
            self.results_format = args.results_format if hasattr(args, "results_format") else None
            self.results_numbers_align = args.results_numbers_align if hasattr(args, "results_numbers_align") else None
            self.show_in_results = args.show_in_results if hasattr(args, "show_in_results") else None
            self.logging_level = args.logging_level

        else:
            logging.error("Invalid command: %s" % args.command)
