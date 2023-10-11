# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Optional
from unittest.mock import MagicMock, Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.benchmark_test.benchmark_test_cluster import BenchmarkTestCluster


class TestBenchmarkTestCluster(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    def setUp(self, args: Optional[Mock] = None, use_manifest: bool = True) -> None:
        self.args = Mock()
        if args:
            self.args = args
        else:
            self.args.workload = "nyc_taxis"
            self.args.stack_suffix = "test-suffix"
            self.args.insecure = False
            self.args.single_node = True
            self.args.min_distribution = False
        self.manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST) if use_manifest else None
        self.stack_name = "stack"
        self.security = True
        self.config = {"Constants": {"SecurityGroupId": "sg-00000000", "VpcId": "vpc-12345", "AccountId": "12345678",
                                     "Region": "us-west-2", "Role": "role-arn", "serverAccessType": "prefixList", "restrictServerAccessTo": "pl-1234",
                                     "isInternal": "true"}}
        self.benchmark_test_cluster = BenchmarkTestCluster(bundle_manifest=self.manifest, config=self.config, args=self.args, current_workspace="current_workspace")

    @patch("test_workflow.benchmark_test.benchmark_test_cluster.BenchmarkTestCluster.wait_for_processing")
    def test_create_single_node_secure(self, mock_wait_for_processing: Optional[Mock]) -> None:
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-007-x64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_test_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)
        self.assertEqual(self.benchmark_test_cluster.endpoint_with_port, 'www.example.com:443')
        self.assertEqual(self.benchmark_test_cluster.port, 443)
        self.assertTrue("opensearch-infra-stack-test-suffix-007-x64" in self.benchmark_test_cluster.stack_name)
        self.assertTrue("securityDisabled=false" in self.benchmark_test_cluster.params)
        self.assertTrue("singleNodeCluster=true" in self.benchmark_test_cluster.params)
        self.assertTrue("isInternal=true" in self.benchmark_test_cluster.params)
        self.assertTrue("distributionUrl=https://artifacts.opensearch.org/bundles/1.0.0/41d5ae25183d4e699e92debfbe3f83bd/opensearch-1.0.0-linux-x64.tar.gz" in self.benchmark_test_cluster.params)
        self.assertTrue(isinstance(self.manifest, BundleManifest))
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_cluster.terminate()
            self.assertEqual(mock_check_call.call_count, 1)

    def test_endpoint(self) -> None:
        self.assertEqual(self.benchmark_test_cluster.endpoint_with_port, None)

    def test_port(self) -> None:
        self.assertEqual(self.benchmark_test_cluster.port, 443)

    @patch("test_workflow.benchmark_test.benchmark_test_cluster.BenchmarkTestCluster.wait_for_processing")
    def test_create_single_node_insecure(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.insecure = True
        self.args.data_instance_type = 'r5.4xlarge'
        TestBenchmarkTestCluster.setUp(self, self.args)
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-007-x64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_test_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)

        self.assertEqual(self.benchmark_test_cluster.endpoint_with_port, 'www.example.com:80')
        self.assertEqual(self.benchmark_test_cluster.port, 80)
        self.assertTrue("securityDisabled=true" in self.benchmark_test_cluster.params)
        self.assertTrue("dataInstanceType=r5.4xlarge" in self.benchmark_test_cluster.params)

    @patch("test_workflow.benchmark_test.benchmark_test_cluster.BenchmarkTestCluster.wait_for_processing")
    def test_create_multi_node(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.single_node = False
        self.args.use_50_percent_heap = True
        self.args.enable_remote_store = True
        TestBenchmarkTestCluster.setUp(self, self.args)
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-007-x64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_test_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)

        self.assertTrue("singleNodeCluster=false" in self.benchmark_test_cluster.params)
        self.assertTrue("use50PercentHeap=true" in self.benchmark_test_cluster.params)
        self.assertTrue("enableRemoteStore=true" in self.benchmark_test_cluster.params)

    @patch("test_workflow.benchmark_test.benchmark_test_cluster.BenchmarkTestCluster.wait_for_processing")
    def test_create_multi_node_without_manifest(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.distribution_url = "https://artifacts.opensearch.org/2.10.0/opensearch.tar.gz"
        self.args.distribution_version = '2.10.0'
        TestBenchmarkTestCluster.setUp(self, self.args, False)
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_test_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)
        self.assertTrue("opensearch-infra-stack-test-suffix" in self.benchmark_test_cluster.stack_name)
        self.assertTrue("cpuArch=x64" in self.benchmark_test_cluster.params)
        self.assertTrue("distVersion=2.10.0" in self.benchmark_test_cluster.params)
        self.assertTrue("distributionUrl=https://artifacts.opensearch.org/2.10.0/opensearch.tar.gz" in self.benchmark_test_cluster.params)
