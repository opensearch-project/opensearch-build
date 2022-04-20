# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_test_cluster import PerfTestCluster
from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig


class TestPerfTestCluster(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    def setUp(self):
        self.manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.stack_name = "stack"
        self.security = "disable"
        self.config = {"Constants": {"SecurityGroupId": "sg-00000000", "VpcId": "vpc-12345", "AccountId": "12345678", "Region": "us-west-2", "Role": "role-arn"}}
        self.perf_test_cluster = PerfTestCluster(bundle_manifest=self.manifest, config=self.config,
                                                 stack_name=self.stack_name, cluster_config=PerfTestClusterConfig(self.security),
                                                 current_workspace="current_workspace")

    def test_create(self):
        mock_file = MagicMock(side_effect=[{"stack": {"PrivateIp": "10.10.10.10"}}])
        with patch("test_workflow.perf_test.perf_test_cluster.os.chdir") as mock_chdir:
            with patch("subprocess.check_call") as mock_check_call:
                with patch("builtins.open", MagicMock()):
                    with patch("json.load", mock_file):
                        self.perf_test_cluster.start()
                        mock_chdir.assert_called_once_with(os.path.join(self.perf_test_cluster.current_workspace, "opensearch-cluster", "cdk", "single-node"))
                        self.assertEqual(mock_check_call.call_count, 1)

    def test_endpoint(self):
        self.assertEqual(self.perf_test_cluster.endpoint_with_port(), None)

    def test_port(self):
        self.assertEqual(self.perf_test_cluster.port(), 443)

    def test_terminate(self):
        with patch("test_workflow.perf_test.perf_test_cluster.os.chdir") as mock_chdir:
            with patch("subprocess.check_call") as mock_check_call:
                self.perf_test_cluster.terminate()
                mock_chdir.assert_called_once_with(os.path.join(self.perf_test_cluster.current_workspace, "current_workspace", "opensearch-cluster", "cdk", "single-node"))
                self.assertEqual(mock_check_call.call_count, 1)

    def test_single_node_cluster(self):
        test_cluster = PerfTestCluster(bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
                                       cluster_config=PerfTestClusterConfig(self.security, 1, 0, 0, 0),
                                       current_workspace="current_workspace")
        self.assertEqual(test_cluster.work_dir, "current_workspace/opensearch-cluster/cdk/single-node")
        self.assertTrue("stack_name" in test_cluster.params)
        self.assertTrue("data_node_count" not in test_cluster.params)

    def test_multi_node_cluster(self):
        test_cluster = PerfTestCluster(bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
                                       cluster_config=PerfTestClusterConfig(self.security, 2, 3, 0, 0),
                                       current_workspace="current_workspace")
        self.assertEqual(test_cluster.work_dir, "current_workspace/opensearch-cluster/cdk/multi-node")
        print(test_cluster.params)
        self.assertTrue("cluster_stack_name" in test_cluster.params)
        self.assertTrue("data_node_count=2" in test_cluster.params)
        self.assertTrue("master_node_count=3" in test_cluster.params)
        self.assertTrue("client_node_count=0" in test_cluster.params)
        self.assertTrue("ingest_node_count=0" in test_cluster.params)
