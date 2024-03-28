# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os
import tempfile
import unittest
from typing import Any, Optional
from unittest.mock import MagicMock, Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs
from test_workflow.benchmark_test.benchmark_test_runner_opensearch import BenchmarkTestRunnerOpenSearch
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
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkCreateCluster.create")
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
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkCreateCluster.create")
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

    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestCluster.start")
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestSuite")
    @patch('test_workflow.benchmark_test.benchmark_test_runner_opensearch.retry_call')
    def test_run_with_cluster_endpoint(self, mock_retry_call: Mock, mock_suite: Mock, mock_benchmark_test_cluster: Mock) -> None:
        args = MagicMock(cluster_endpoint=True)
        mock_cluster = MagicMock()

        mock_benchmark_test_cluster.return_value = mock_cluster
        instance = BenchmarkTestRunnerOpenSearch(args, None)
        instance.run_tests()
        self.assertEqual(mock_suite.call_count, 1)
        self.assertEqual(mock_benchmark_test_cluster.call_count, 1)
        mock_retry_call.assert_called_once_with(mock_suite.return_value.execute, tries=3, delay=60, backoff=2)

    @patch('test_workflow.benchmark_test.benchmark_test_cluster.BenchmarkTestCluster.wait_for_processing')
    @patch("test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestSuite")
    @patch('test_workflow.benchmark_test.benchmark_test_runner_opensearch.retry_call')
    @patch("subprocess.run")
    @patch("requests.get")
    def test_run_with_cluster_endpoint_with_arguments(self, mock_requests_get: Mock, mock_subprocess_run: Mock,
                                                      mock_retry_call: Mock, mock_suite: Mock, mock_wait_for_processing: Optional[Mock]) -> None:
        args = MagicMock(cluster_endpoint=True)
        mock_wait_for_processing.return_value = None
        mock_result = MagicMock()
        mock_result.stdout = '''
                        {
                            "cluster_name" : "opensearch-cluster.amazon.com",
                            "version": {
                            "distribution": "opensearch",
                            "number": "2.9.0",
                            "build_type": "tar",
                            "minimum_index_compatibility_version": "2.0.0"
                            }
                        }
                        '''
        mock_subprocess_run.return_value = mock_result

        instance = BenchmarkTestRunnerOpenSearch(args, None)
        with patch('test_workflow.benchmark_test.benchmark_test_runner_opensearch.BenchmarkTestCluster') as MockBenchmarkTestCluster:
            mock_cluster_instance = MockBenchmarkTestCluster.return_value
            mock_cluster_instance.endpoint_with_port = "opensearch-cluster.amazon.com"
            mock_cluster_instance.fetch_password.return_value = "admin"

            with patch("json.loads"):
                instance.run_tests()
        self.assertEqual(mock_suite.call_count, 1)
        self.assertEqual(MockBenchmarkTestCluster.call_count, 1)
        mock_retry_call.assert_called_once_with(mock_suite.return_value.execute, tries=3, delay=60, backoff=2)
