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
        with patch('test_workflow.integ_test.utils.get_password') as mock_get_password:
            mock_get_password.return_value = "myStrongPassword123!"

            self.args = Mock()
            self.args.insecure = False
            self.args.sigv4 = False
            self.args.cluster_endpoint = "opensearch-cluster.amazon.com"
            self.args.secondary_endpoint = None
            self.args.password = None
            self.benchmark_test_cluster = BenchmarkTestCluster(self.args)

    CLUSTER_INFO = '''
            {
                "cluster_name" : "opensearch-cluster.amazon.com",
                "version": {
                "distribution": "opensearch",
                "number": "2.12.0",
                "build_type": "tar",
                "minimum_index_compatibility_version": "2.0.0"
                }
            }
            '''

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

    @patch("subprocess.run")
    @patch("requests.get")
    @patch('test_workflow.benchmark_test.benchmark_test_cluster.HTTPBasicAuth')
    def test_endpoint_with_security(self, mock_http_auth: Mock, mock_requests_get: Mock, mock_subprocess_run: Mock) -> None:
        mock_result = MagicMock()
        mock_result.stdout = '''
                {
                    "cluster_name" : "opensearch-cluster.amazon.com",
                    "version": {
                    "distribution": "opensearch",
                    "number": "2.12.0",
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
        self.assertEqual(self.benchmark_test_cluster.password, 'myStrongPassword123!')
        self.assertEqual(self.benchmark_test_cluster.endpoint_with_port, 'opensearch-cluster.amazon.com:443')
        self.assertEqual(self.benchmark_test_cluster.port, 443)

    def test_endpoint_with_timeout_error(self) -> None:

        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("Command", 30)

            with self.assertRaises(TimeoutError) as context:
                self.benchmark_test_cluster.start()

            self.assertIn("Time out! Couldn't connect to the cluster", str(context.exception))

    @patch("subprocess.run")
    @patch("requests.get")
    def test_target_hosts_without_secondary_endpoint(self, mock_requests_get: Mock, mock_subprocess_run: Mock) -> None:
        mock_result = MagicMock()
        mock_result.stdout = self.CLUSTER_INFO
        mock_subprocess_run.return_value = mock_result

        self.benchmark_test_cluster.start()

        # A single cluster is passed to opensearch-benchmark as a plain host:port string.
        self.assertEqual(self.benchmark_test_cluster.target_hosts, 'opensearch-cluster.amazon.com:443')
        self.assertIsNone(self.benchmark_test_cluster.secondary_endpoint)
        self.assertIsNone(self.benchmark_test_cluster.secondary_endpoint_with_port)

    @patch("subprocess.run")
    @patch("requests.get")
    @patch('test_workflow.benchmark_test.benchmark_test_cluster.HTTPBasicAuth')
    def test_secondary_endpoint(self, mock_http_auth: Mock, mock_requests_get: Mock, mock_subprocess_run: Mock) -> None:
        self.args.secondary_endpoint = "opensearch-follower-cluster.amazon.com"
        cluster = BenchmarkTestCluster(self.args)
        mock_result = MagicMock()
        mock_result.stdout = self.CLUSTER_INFO
        mock_subprocess_run.return_value = mock_result

        cluster.start()

        # Both clusters are probed and waited on, the version comes off the primary cluster.
        self.assertEqual(mock_subprocess_run.call_count, 2)
        self.assertEqual(self.args.distribution_version, '2.12.0')
        mock_requests_get.assert_any_call(url="https://opensearch-cluster.amazon.com/_cluster/health", auth=mock_http_auth.return_value, verify=False)
        mock_requests_get.assert_any_call(url="https://opensearch-follower-cluster.amazon.com/_cluster/health", auth=mock_http_auth.return_value, verify=False)

        self.assertEqual(cluster.endpoint_with_port, 'opensearch-cluster.amazon.com:443')
        self.assertEqual(cluster.secondary_endpoint, 'opensearch-follower-cluster.amazon.com')
        self.assertEqual(cluster.secondary_endpoint_with_port, 'opensearch-follower-cluster.amazon.com:443')
        self.assertEqual(cluster.target_hosts, {
            "default": [{"host": "opensearch-cluster.amazon.com", "port": 443}],
            "follower": [{"host": "opensearch-follower-cluster.amazon.com", "port": 443}],
        })

    @patch("subprocess.run")
    def test_secondary_endpoint_with_sigv4(self, mock_subprocess_run: Mock) -> None:
        self.args.sigv4 = True
        self.args.secondary_endpoint = "opensearch-follower-cluster.amazon.com"
        cluster = BenchmarkTestCluster(self.args)

        cluster.start()

        # sigv4 runs skip the cluster probe altogether.
        mock_subprocess_run.assert_not_called()
        self.assertEqual(cluster.target_hosts, {
            "default": [{"host": "opensearch-cluster.amazon.com", "port": 443}],
            "follower": [{"host": "opensearch-follower-cluster.amazon.com", "port": 443}],
        })

    @patch("subprocess.run")
    @patch("requests.get")
    def test_secondary_endpoint_exception(self, mock_requests_get: Mock, mock_subprocess_run: Mock) -> None:
        self.args.secondary_endpoint = "opensearch-follower-cluster.amazon.com"
        cluster = BenchmarkTestCluster(self.args)
        primary_result = MagicMock()
        primary_result.stdout = self.CLUSTER_INFO
        secondary_result = MagicMock()
        secondary_result.stdout = ""
        mock_subprocess_run.side_effect = [primary_result, secondary_result]

        with self.assertRaises(Exception) as context:
            cluster.start()

        self.assertIn("Empty response retrieved from the curl command", str(context.exception))

    @patch("subprocess.run")
    def test_endpoint_exception(self, mock_subprocess_run: Mock) -> None:
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_subprocess_run.return_value = mock_result
        with self.assertRaises(Exception) as context:
            self.benchmark_test_cluster.start()

        self.assertIn("Empty response retrieved from the curl command", str(context.exception))
