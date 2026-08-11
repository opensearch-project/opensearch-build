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
from test_workflow.benchmark_test.benchmark_create_cluster import BenchmarkCreateCluster


class TestBenchmarkCreateCluster(unittest.TestCase):
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
            self.args.enable_instance_storage = False
            self.args.ccr_enabled = False
        self.manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST) if use_manifest else None
        self.stack_name = "stack"
        self.security = True
        self.config = {"Constants": {"SecurityGroupId": "sg-00000000", "VpcId": "vpc-12345", "AccountId": "12345678",
                                     "Region": "us-west-2", "Role": "role-arn", "serverAccessType": "prefixList", "restrictServerAccessTo": "pl-1234",
                                     "isInternal": "true", "IamRoleArn": "arn:aws:iam::12344567890:role/customRole"}}
        self.benchmark_create_cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args, current_workspace="current_workspace")

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_single_node_secure(self, mock_wait_for_processing: Optional[Mock]) -> None:
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-007-x64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_create_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)
        self.assertEqual(self.benchmark_create_cluster.endpoint_with_port, 'www.example.com:443')
        self.assertEqual(self.benchmark_create_cluster.port, 443)
        self.assertTrue("opensearch-infra-stack-test-suffix-007-x64" in self.benchmark_create_cluster.stack_name)
        self.assertTrue("securityDisabled=false" in self.benchmark_create_cluster.params)
        self.assertTrue("adminPassword=admin" in self.benchmark_create_cluster.params)
        self.assertTrue("singleNodeCluster=true" in self.benchmark_create_cluster.params)
        self.assertTrue("isInternal=true" in self.benchmark_create_cluster.params)
        self.assertTrue("useInstanceBasedStorage=false" in self.benchmark_create_cluster.params)
        self.assertTrue("distributionUrl=https://artifacts.opensearch.org/bundles/1.0.0/41d5ae25183d4e699e92debfbe3f83bd/opensearch-1.0.0-linux-x64.tar.gz" in self.benchmark_create_cluster.params)
        self.assertTrue(isinstance(self.manifest, BundleManifest))
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_create_cluster.terminate()
            self.assertEqual(mock_check_call.call_count, 1)

    def test_endpoint(self) -> None:
        self.assertEqual(self.benchmark_create_cluster.endpoint_with_port, None)

    def test_port(self) -> None:
        self.assertEqual(self.benchmark_create_cluster.port, 443)

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_single_node_insecure(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.insecure = True
        self.args.data_instance_type = 'r5.4xlarge'
        self.args.enable_instance_storage = True
        self.args.heap_size_in_gb = '4'

        TestBenchmarkCreateCluster.setUp(self, self.args)
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-007-x64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_create_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)

        self.assertEqual(self.benchmark_create_cluster.endpoint_with_port, 'www.example.com:80')
        self.assertEqual(self.benchmark_create_cluster.port, 80)
        self.assertTrue("securityDisabled=true" in self.benchmark_create_cluster.params)
        self.assertTrue("dataInstanceType=r5.4xlarge" in self.benchmark_create_cluster.params)
        self.assertTrue("customRoleArn=arn:aws:iam::12344567890:role/customRole" in self.benchmark_create_cluster.params)
        self.assertTrue("useInstanceBasedStorage=true" in self.benchmark_create_cluster.params)
        self.assertTrue("heapSizeInGb=4" in self.benchmark_create_cluster.params)

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_multi_node(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.single_node = False
        self.args.enable_remote_store = True
        self.args.plugin_url = "https://example.com/plugin.zip"
        TestBenchmarkCreateCluster.setUp(self, self.args)
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-007-x64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_create_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)

        self.assertTrue("singleNodeCluster=false" in self.benchmark_create_cluster.params)
        self.assertTrue("enableRemoteStore=true" in self.benchmark_create_cluster.params)
        self.assertTrue("pluginUrl=https://example.com/plugin.zip" in self.benchmark_create_cluster.params)

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_ccr_leader_stack_suffix_and_seed_ip_single_node(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.ccr_enabled = True
        self.args.single_node = True
        TestBenchmarkCreateCluster.setUp(self, self.args)
        cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args,
                                         current_workspace="current_workspace", cluster_role="leader")
        self.assertEqual(cluster.cluster_role, "leader")
        self.assertEqual(cluster.output_file, "output-leader.json")
        self.assertTrue("test-suffix-leader" in cluster.stack_name)
        self.assertTrue("suffix=test-suffix-leader" in cluster.params)
        mock_file = MagicMock(side_effect=[{cluster.stack_name: {"loadbalancerurl": "www.example.com", "privateip": "10.0.0.5"}}])
        with patch("subprocess.check_call"):
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    cluster.start()
        self.assertEqual(cluster.seed_node_ip, "10.0.0.5")

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.requests.get")
    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_ccr_follower_seed_ip_multi_node(self, mock_wait_for_processing: Optional[Mock], mock_get: Mock) -> None:
        self.args.ccr_enabled = True
        self.args.single_node = False
        self.args.insecure = True
        TestBenchmarkCreateCluster.setUp(self, self.args)
        # Other cluster_manager nodes are listed first, so matching on role alone would pick the
        # wrong one. Only the node named 'seed' is the seed node.
        mock_get.return_value.json.return_value = [
            {"ip": "10.0.2.4", "name": "ip-10-0-2-4.us-east-1.compute.internal"},
            {"ip": "10.0.3.7", "name": "ip-10-0-3-7.us-east-1.compute.internal"},
            {"ip": "10.0.1.9", "name": "seed"},
        ]
        cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args,
                                         current_workspace="current_workspace", cluster_role="follower")
        self.assertTrue("test-suffix-follower" in cluster.stack_name)
        get_calls_when_waiting = []
        mock_wait_for_processing.side_effect = lambda: get_calls_when_waiting.append(mock_get.call_count)
        mock_file = MagicMock(side_effect=[{cluster.stack_name: {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call"):
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    cluster.start()
        self.assertEqual(cluster.seed_node_ip, "10.0.1.9")
        self.assertEqual(mock_get.call_args.kwargs["url"], "http://www.example.com/_cat/nodes?format=json&h=ip,name")
        # The cluster has to be up before it can be asked for its seed node, so no _cat/nodes call
        # may have happened by the time wait_for_processing runs.
        mock_wait_for_processing.assert_called_once()
        self.assertEqual(get_calls_when_waiting, [0])

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.requests.get")
    def test_fetch_seed_node_ip_from_cluster_no_seed_node(self, mock_get: Mock) -> None:
        self.args.ccr_enabled = True
        self.args.single_node = False
        TestBenchmarkCreateCluster.setUp(self, self.args)
        mock_get.return_value.json.return_value = [{"ip": "10.0.2.4", "name": "ip-10-0-2-4.us-east-1.compute.internal"}]
        cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args,
                                         current_workspace="current_workspace", cluster_role="leader")
        cluster.cluster_endpoint = "leader.example.com"
        with self.assertRaises(RuntimeError):
            cluster.fetch_seed_node_ip_from_cluster()

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.requests.put")
    def test_apply_follower_settings(self, mock_put: Mock) -> None:
        self.args.ccr_enabled = True
        self.args.insecure = False
        self.args.username = "admin"
        TestBenchmarkCreateCluster.setUp(self, self.args)
        cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args,
                                         current_workspace="current_workspace", cluster_role="follower")
        cluster.cluster_endpoint = "follower.example.com"
        cluster.apply_follower_settings("10.0.0.5")

        # The remote connection settings are applied first, then the replication relationship.
        self.assertEqual(mock_put.call_count, 2)
        settings_kwargs = mock_put.call_args_list[0].kwargs
        self.assertEqual(settings_kwargs["url"], "https://follower.example.com/_cluster/settings")
        self.assertEqual(settings_kwargs["json"]["persistent"]["cluster.remote.leader.seeds"], ["10.0.0.5:9300"])
        self.assertEqual(settings_kwargs["verify"], False)

        relationship_kwargs = mock_put.call_args_list[1].kwargs
        self.assertEqual(relationship_kwargs["url"], "https://follower.example.com/_remote_replication/cluster/my-relationship")
        self.assertEqual(relationship_kwargs["json"], {"role": "SECONDARY", "local_alias": "local-cluster", "remote_alias": "leader"})
        self.assertEqual(relationship_kwargs["verify"], False)
        self.assertEqual(mock_put.return_value.raise_for_status.call_count, 2)

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.requests.put")
    def test_apply_follower_settings_insecure(self, mock_put: Mock) -> None:
        self.args.ccr_enabled = True
        self.args.insecure = True
        TestBenchmarkCreateCluster.setUp(self, self.args)
        cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args,
                                         current_workspace="current_workspace", cluster_role="follower")
        cluster.cluster_endpoint = "follower.example.com"
        cluster.apply_follower_settings("10.0.0.5")

        self.assertEqual(mock_put.call_count, 2)
        for kwargs in [call.kwargs for call in mock_put.call_args_list]:
            self.assertTrue(kwargs["url"].startswith("http://"))
            self.assertNotIn("auth", kwargs)
            self.assertNotIn("verify", kwargs)

    def test_apply_follower_settings_missing_seed_ip(self) -> None:
        self.args.ccr_enabled = True
        TestBenchmarkCreateCluster.setUp(self, self.args)
        cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args,
                                         current_workspace="current_workspace", cluster_role="follower")
        with self.assertRaises(RuntimeError):
            cluster.apply_follower_settings("")

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_multi_node_without_manifest(self, mock_wait_for_processing: Optional[Mock]) -> None:
        self.args.distribution_url = "https://artifacts.opensearch.org/2.10.0/opensearch.tar.gz"
        self.args.distribution_version = '2.12.0'
        self.args.insecure = False
        TestBenchmarkCreateCluster.setUp(self, self.args, False)
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_create_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)
        self.assertTrue("opensearch-infra-stack-test-suffix" in self.benchmark_create_cluster.stack_name)
        self.assertTrue("cpuArch=x64" in self.benchmark_create_cluster.params)
        self.assertTrue("distVersion=2.12.0" in self.benchmark_create_cluster.params)
        self.assertTrue("securityDisabled=false" in self.benchmark_create_cluster.params)
        self.assertTrue("adminPassword=myStrongPassword123!" in self.benchmark_create_cluster.params)
        self.assertTrue("distributionUrl=https://artifacts.opensearch.org/2.10.0/opensearch.tar.gz" in self.benchmark_create_cluster.params)
