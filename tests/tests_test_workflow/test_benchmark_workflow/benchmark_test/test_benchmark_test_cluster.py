# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest
from unittest.mock import MagicMock, Mock, patch

from test_workflow.benchmark_test.benchmark_test_cluster import BenchmarkTestCluster


class TestBenchmarkTestCluster(unittest.TestCase):
    def setUp(self) -> None:
        self.args = Mock()
        self.args.insecure = False
        self.args.cluster_endpoint = "opensearch-cluster.amazon.com"
        self.password = None
        self.cluster_endpoint = self.args.cluster_endpoint
        self.cluster_endpoint_with_port = None

        self.benchmark_test_cluster = BenchmarkTestCluster(self.args)

    @patch("subprocess.run")
    @patch("requests.get")
    def test_endpoint_without_security(self, mock_requests_get: Mock, mock_subprocess_run: Mock) -> None:
        self.args.insecure = True
        self.cluster_endpoint_with_port = None
        mock_result = MagicMock()
        mock_result.stdout = '''
        {
            "cluster_name" : "opensearch-cluster.amazon.com”,
            "version": {
            "distribution": "opensearch",
            "number": “2.9.0”,
            "build_type": "tar",
            "minimum_index_compatibility_version": "2.0.0"
            }
        }
        '''
        mock_subprocess_run.return_value = mock_result
        with patch("json.loads", ):
            self.benchmark_test_cluster.start()
            mock_requests_get.assert_called_with(url=f"http://{self.benchmark_test_cluster.endpoint}/_cluster/health")
        self.assertEqual(self.benchmark_test_cluster.endpoint, 'opensearch-cluster.amazon.com')
        self.assertEqual(self.benchmark_test_cluster.endpoint_with_port, 'opensearch-cluster.amazon.com:80')
        self.assertEqual(self.benchmark_test_cluster.port, 80)

    @patch('test_workflow.benchmark_test.benchmark_test_cluster.get_password')
    @patch("subprocess.run")
    @patch("requests.get")
    @patch('test_workflow.benchmark_test.benchmark_test_cluster.HTTPBasicAuth')
    def test_endpoint_with_security(self, mock_http_auth: Mock, mock_requests_get: Mock, mock_subprocess_run: Mock,
                                    mock_password: Mock) -> None:
        mock_password.return_value = "admin"
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
        with patch("json.loads"):
            self.benchmark_test_cluster.start()
            mock_requests_get.assert_called_with(url=f"https://{self.benchmark_test_cluster.endpoint}/_cluster/health", auth=mock_http_auth.return_value, verify=False)
        self.assertEqual(self.benchmark_test_cluster.endpoint, 'opensearch-cluster.amazon.com')
        self.assertEqual(self.benchmark_test_cluster.endpoint_with_port, 'opensearch-cluster.amazon.com:443')
        self.assertEqual(self.benchmark_test_cluster.port, 443)

    def test_endpoint_with_timeout_error(self) -> None:

        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("Command", 5)

            with self.assertRaises(TimeoutError) as context:
                self.benchmark_test_cluster.start()

            self.assertIn("Time out! Couldn't connect to the cluster", str(context.exception))
