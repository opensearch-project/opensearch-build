# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os
import tempfile
import unittest
from typing import Any
from unittest.mock import Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_runners import BenchmarkTestRunners


class TestBenchmarkTestRunnerOpenSearch(unittest.TestCase):

    @patch("argparse._sys.argv", ["run_benchmark_test.py",
                                  "--bundle-manifest",
                                  os.path.join(os.path.dirname(__file__), "data", "bundle_manifest.yml"),
                                  "--config", os.path.join(os.path.dirname(__file__), "data", "test-config.yml"),
                                  "--workload", "test",
                                  "--suffix", "test"])
    @patch("os.chdir")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.TemporaryDirectory")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.GitRepository")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestCluster.create")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestSuite")
    def test_run(self, mock_suite: Mock, mock_cluster: Mock, mock_git: Mock, mock_temp_directory: Mock,
                 *mocks: Any) -> None:
        mock_temp_directory.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_cluster.return_value.__enter__.return_value = mock_cluster

        benchmark_args = BenchmarkArgs()
        test_manifest = BundleManifest.from_file(benchmark_args.bundle_manifest)
        runner = BenchmarkTestRunners.from_args(benchmark_args, test_manifest)
        runner.run()

        mock_git.assert_called_with("https://github.com/opensearch-project/opensearch-cluster-cdk.git", "1.x",
                                    os.path.join(tempfile.gettempdir(), "opensearch-cluster-cdk"))
        self.assertEqual(mock_suite.call_count, 1)
        self.assertEqual(mock_cluster.call_count, 1)
        self.assertEqual(mock_git.call_count, 1)
        self.assertEqual(mock_temp_directory.call_count, 1)

    @patch("argparse._sys.argv", ["run_benchmark_test.py",
                                  "--distribution-url",
                                  "https://artifacts.opensearch.org/2.10.0/opensearch.tar.gz",
                                  "--distribution-version",
                                  "2.3.0",
                                  "--config", os.path.join(os.path.dirname(__file__), "data", "test-config.yml"),
                                  "--workload", "test",
                                  "--suffix", "test"])
    @patch("os.chdir")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.TemporaryDirectory")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.GitRepository")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestCluster.create")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestSuite")
    def test_run_with_dist_url_and_version(self, mock_suite: Mock, mock_cluster: Mock, mock_git: Mock,
                                           mock_temp_directory: Mock,
                                           *mocks: Any) -> None:
        mock_temp_directory.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_cluster.return_value.__enter__.return_value = mock_cluster

        benchmark_args = BenchmarkArgs()
        runner = BenchmarkTestRunners.from_args(benchmark_args)
        runner.run()
        mock_git.assert_called_with("https://github.com/opensearch-project/opensearch-cluster-cdk.git", "main",
                                    os.path.join(tempfile.gettempdir(), "opensearch-cluster-cdk"))
        self.assertEqual(mock_suite.call_count, 1)
        self.assertEqual(mock_cluster.call_count, 1)
        self.assertEqual(mock_git.call_count, 1)
        self.assertEqual(mock_temp_directory.call_count, 1)
