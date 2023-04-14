import logging
import os
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

    @patch("argparse._sys.argv", [ARGS_PY, "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test"])
    def test_benchmark_with_default_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.workload, "test")
        self.assertFalse(test_args.insecure)
        self.assertFalse(test_args.singleNode)
        self.assertFalse(test_args.minDistribution)

    @patch("argparse._sys.argv", [ARGS_PY, "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
                                  "--managerNodeCount", "2", "--dataNodeCount", "3", "--clientNodeCount", "1",
                                  "--ingestNodeCount", "1", "--mlNodeCount", "1"])
    def test_benchmark_with_optional_node_count_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.managerNodeCount, "2")
        self.assertEqual(test_args.dataNodeCount, "3")
        self.assertEqual(test_args.clientNodeCount, "1")
        self.assertEqual(test_args.ingestNodeCount, "1")
        self.assertEqual(test_args.mlNodeCount, "1")

    @patch("argparse._sys.argv", [ARGS_PY, "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
                                  "--dataNodeStorage", "200", "--mlNodeStorage", "100"])
    def test_benchmark_with_optional_node_storage_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.dataNodeStorage, "200")
        self.assertEqual(test_args.mlNodeStorage, "100")

    @patch("argparse._sys.argv", [ARGS_PY, "--bundle-manifest", TEST_DIST_MANIFEST_PATH, "--config", TEST_CONFIG_PATH, "--workload", "test",
                                  "--additionalConfig", 'opensearch.experimental.feature.replication_type.enabled:true','key:value',
                                  "--jvmSysProps", "key1=value1,key2=value2"])
    def test_benchmark_with_optional_config_parameters(self) -> None:
        test_args = BenchmarkArgs()
        self.assertEqual(test_args.additionalConfig, '{"opensearch.experimental.feature.replication_type.enabled": "true", "key": "value"}')
        self.assertEqual(test_args.jvmSysProps, "key1=value1,key2=value2")








