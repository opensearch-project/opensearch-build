# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import io
import os
import sys
import unittest
from unittest.mock import patch

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs


class TestBenchmarkArgs(unittest.TestCase):
    ARGS_PY = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "run_benchmark_test.py"
        )
    )

    TEST_CONFIG_PATH = os.path.join(
        os.path.dirname(__file__), "data", "test-config.yml"
    )

    TEST_DIST_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__), "data", "remote", "dist", "opensearch", "manifest.yml"
    )

    @patch("argparse._sys.argv",
           [ARGS_PY, "execute-test", "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test"])
    def test_benchmark_with_default_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.workload, "test")
        self.assertFalse(test_args.insecure)
        self.assertFalse(test_args.single_node)
        self.assertFalse(test_args.min_distribution)
        self.assertFalse(test_args.enable_remote_store)
        self.assertFalse(test_args.enable_instance_storage)

    @patch("argparse._sys.argv",
           [ARGS_PY, "execute-test", "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
            "--manager-node-count", "2", "--data-node-count", "3", "--client-node-count", "1",
            "--ingest-node-count", "1", "--ml-node-count", "1"])
    def test_benchmark_with_optional_node_count_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.manager_node_count, "2")
        self.assertEqual(test_args.data_node_count, "3")
        self.assertEqual(test_args.client_node_count, "1")
        self.assertEqual(test_args.ingest_node_count, "1")
        self.assertEqual(test_args.ml_node_count, "1")

    @patch("argparse._sys.argv",
           [ARGS_PY, "execute-test", "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
            "--data-node-storage", "200", "--ml-node-storage", "100", "--enable-instance-storage"])
    def test_benchmark_with_optional_node_storage_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.data_node_storage, "200")
        self.assertEqual(test_args.ml_node_storage, "100")
        self.assertTrue(test_args.enable_instance_storage)

    @patch("argparse._sys.argv", [ARGS_PY, "execute-test", "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
                                  "--additional-config", 'opensearch.experimental.feature.replication_type.enabled:true','key:value',  # noqa: E231
                                  "--jvm-sys-props", "key1=value1,key2=value2"])
    def test_benchmark_with_optional_config_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.additional_config,
                         '{"opensearch.experimental.feature.replication_type.enabled": "true", "key": "value"}')
        self.assertEqual(test_args.jvm_sys_props, "key1=value1,key2=value2")

    @patch("argparse._sys.argv", [ARGS_PY, "execute-test", "--distribution-url", "https://artifacts.opensearch.org/2.10.0/opensearch-2.10.0-linux-x64.tar.gz",
                                  "--distribution-version", "2.10.0", "--config", TEST_CONFIG_PATH, "--workload", "test"])
    def test_benchmark_with_distribution_url_and_version(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.distribution_url, "https://artifacts.opensearch.org/2.10.0/opensearch-2.10.0-linux-x64.tar.gz")
        self.assertEqual(test_args.distribution_version, "2.10.0")

    @patch("argparse._sys.argv", [ARGS_PY, "execute-test", "--distribution-url", "https://artifacts.opensearch.org/2.10.0/opensearch-2.10.0-linux-x64.tar.gz",
                                  "--distribution-version", None, "--config", TEST_CONFIG_PATH, "--workload", "test"])
    def test_benchmark_with_distribution_url_and_without_version(self) -> None:
        with self.assertRaises(Exception) as context:
            BenchmarkArgs()
        self.assertEqual(str(context.exception), "--distribution-version is required parameter while using --distribution-url param.")

    @patch("argparse._sys.argv", [ARGS_PY, "execute-test", "--config", TEST_CONFIG_PATH, "--workload", "test"])
    def test_benchmark_without_distribution_url_and_without_manifest_and_cluster_endpoint(self) -> None:
        with self.assertRaises(Exception) as context:
            BenchmarkArgs()
        self.assertEqual(str(context.exception), "Please provide either --bundle-manifest or --distribution-url  or --cluster_endpoint to run the performance test.")

    @patch("argparse._sys.argv", [ARGS_PY, "execute-test", "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
                                  "--test-procedure", 'test-procedure,another-test-procedure', "--exclude-tasks", "index,type:search,tag:setup",
                                  "--include-tasks", "index,type:search,tag:setup"])
    def test_benchmark_with_optional_benchmark_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.test_procedure,
                         'test-procedure,another-test-procedure')
        self.assertEqual(test_args.exclude_tasks,
                         'index,type:search,tag:setup')
        self.assertEqual(test_args.include_tasks,
                         'index,type:search,tag:setup')

    @patch("argparse._sys.argv", [ARGS_PY, "compare", "baseline_id", "contender_id"])
    def test_compare_with_required_arguments(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.baseline, "baseline_id")
        self.assertEqual(test_args.contender, "contender_id")

    @patch("argparse._sys.argv", [ARGS_PY, "compare"])
    def test_compare_without_required_arguments(self) -> None:
        with self.assertRaises(ValueError) as context:
            BenchmarkArgs()
        self.assertEqual(str(context.exception), "Both 'baseline' and 'contender' arguments are required for the 'compare' command.")

    @patch("argparse._sys.argv", [ARGS_PY, "compare", "baseline_id", "contender_id", "--results-format", "csv"])
    def test_compare_with_results_format(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.results_format, "csv")

    @patch("argparse._sys.argv", [ARGS_PY, "compare", "baseline_id", "contender_id", "--results-numbers-align", "left"])
    def test_compare_with_results_numbers_align(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.results_numbers_align, "left")

    @patch("argparse._sys.argv", [ARGS_PY, "compare", "baseline_id", "contender_id", "--show-in-results", "true"])
    def test_compare_with_show_in_results(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.show_in_results, "true")

    @patch("argparse._sys.argv", [ARGS_PY, "compare", "baseline_id", "contender_id", "--suffix", "test-suffix"])
    def test_compare_with_suffix(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.stack_suffix, "test-suffix")

    @patch("argparse._sys.argv", [ARGS_PY, "compare", "baseline_id", "contender_id", "--benchmark-config", "benchmark.ini"])
    def test_compare_with_benchmark_config(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.benchmark_config, "benchmark.ini")

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "invalid-command"])
    def test_invalid_command(self) -> None:
        # Capture stderr
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr

        with self.assertRaises(SystemExit):
            BenchmarkArgs()

        # Assert that the expected error message is printed to stderr
        self.assertIn("argument command: invalid choice: 'invalid-command'", captured_stderr.getvalue())

        # Restore stderr
        sys.stderr = sys.__stderr__
