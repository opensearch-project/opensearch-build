# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import Mock, patch

import pytest

from run_benchmark_test import main


class TestRunBenchmarkTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "--help"])
    @patch("run_benchmark_test.check_docker")
    def test_usage(self, mock_docker: Mock) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    BUNDLE_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__),
        "jenkins",
        "data",
    )

    CONFIG_ROOT_PATH = os.path.join(
        os.path.dirname(__file__),
        "data",
    )

    OPENSEARCH_BUNDLE_MANIFEST = os.path.realpath(os.path.join(BUNDLE_MANIFEST_PATH, "opensearch-1.3.0-bundle.yml"))
    BENCHMARK_TEST_CONFIG = os.path.realpath(os.path.join(CONFIG_ROOT_PATH, "test-config.yml"))

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "execute-test", "--bundle-manifest", OPENSEARCH_BUNDLE_MANIFEST, "--config",
                                  BENCHMARK_TEST_CONFIG, "--workload", "test", "--suffix", "test"])
    @patch("run_benchmark_test.BenchmarkTestRunners.from_args")
    @patch("run_benchmark_test.check_docker")
    def test_default_execute_benchmark_test(self, mock_docker: Mock, mock_runner: Mock, *mocks: Any) -> None:
        main()
        self.assertEqual(1, mock_runner.call_count)

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "execute-test", "--bundle-manifest", OPENSEARCH_BUNDLE_MANIFEST, "--config",
                                  BENCHMARK_TEST_CONFIG, "--workload", "test", "--suffix", "test"])
    @patch("test_workflow.benchmark_test.benchmark_test_runners.BenchmarkTestRunnerOpenSearchPlugins.run_tests")
    @patch("test_workflow.benchmark_test.benchmark_test_runners.BenchmarkTestRunnerOpenSearch.run_tests")
    @patch("run_benchmark_test.check_docker")
    def test_run_benchmark_test(self, mock_docker: Mock, os_mock_runner: Mock, plugin_mock_runner: Mock, *mock: Any) -> None:
        main()
        self.assertEqual(1, os_mock_runner.call_count)
        self.assertEqual(0, plugin_mock_runner.call_count)

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "execute-test", "--bundle-manifest", OPENSEARCH_BUNDLE_MANIFEST, "--config",
                                  BENCHMARK_TEST_CONFIG, "--workload", "test", "--suffix", "test", "--component", "abc"])
    @patch("test_workflow.benchmark_test.benchmark_test_runners.BenchmarkTestRunnerOpenSearchPlugins.run_tests")
    @patch("test_workflow.benchmark_test.benchmark_test_runners.BenchmarkTestRunnerOpenSearch.run_tests")
    @patch("run_benchmark_test.check_docker")
    def test_run_benchmark_test_plugins(self, mock_docker: Mock, os_mock_runner: Mock, plugin_mock_runner: Mock, *mock: Any) -> None:
        main()
        self.assertEqual(0, os_mock_runner.call_count)
        self.assertEqual(1, plugin_mock_runner.call_count)

    @patch("argparse._sys.argv", ["run_benchmark_test.py", "execute-test", "--distribution-url", "test.url", "--distribution-version", "2.10.0",
                                  "--config", BENCHMARK_TEST_CONFIG, "--workload", "test", "--suffix", "test"])
    @patch("run_benchmark_test.BenchmarkTestRunners.from_args")
    @patch("run_benchmark_test.check_docker")
    def test_default_execute_benchmark_test_without_manifest(self, mock_docker: Mock, mock_runner: Mock) -> None:
        main()
        self.assertEqual(1, mock_runner.call_count)
