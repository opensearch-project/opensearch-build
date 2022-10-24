# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_multi_node_cluster import PerfMultiNodeCluster
from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig


class TestPerfMultiNodeCluster(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    def setUp(self) -> None:
        self.manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.stack_name = "stack"
        self.config = {"Constants": {"SecurityGroupId": "sg-00000000", "VpcId": "vpc-12345",
                       "AccountId": "12345678", "Region": "us-west-2", "Role": "role-arn"}}

    def test_multi_node_cluster(self) -> None:
        test_cluster = PerfMultiNodeCluster(
            bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
            cluster_config=PerfTestClusterConfig(True, 2, 3, 0, 0), current_workspace="current_workspace")

        self.assertEqual(test_cluster.work_dir, os.path.join("current_workspace", "opensearch-cluster", "cdk", "multi-node"))
        self.assertTrue("cluster_stack_name" in test_cluster.params)
        self.assertTrue("data_node_count=2" in test_cluster.params)
        self.assertTrue("master_node_count=3" in test_cluster.params)
        self.assertTrue("client_node_count=0" in test_cluster.params)
        self.assertTrue("ingest_node_count=0" in test_cluster.params)
        self.assertTrue("use_50_percent_heap=disable" in test_cluster.params)

    def test_multi_node_cluster_invalid_configuration(self) -> None:
        self.assertRaises(
            AssertionError, PerfMultiNodeCluster,
            bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
            cluster_config=PerfTestClusterConfig(False, 1, 0, 0, 0), current_workspace="current_workspace")

    def test_multi_node_cluster_without_security(self) -> None:
        test_cluster = PerfMultiNodeCluster(
            bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
            cluster_config=PerfTestClusterConfig(False, 1, 1, 0, 0), current_workspace="current_workspace")

        cdk_output = {
            self.stack_name: {
                "LoadBalancerEndpoint": "abc"
            }
        }
        test_cluster.create_endpoint(cdk_output)
        self.assertEqual(test_cluster.cluster_endpoint_with_port, "http://abc:80")
        self.assertTrue(test_cluster.is_endpoint_public)
        self.assertEqual(test_cluster.endpoint, "abc")

    def test_multi_node_cluster_with_security(self) -> None:
        test_cluster = PerfMultiNodeCluster(
            bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
            cluster_config=PerfTestClusterConfig(True, 1, 1, 0, 0), current_workspace="current_workspace")

        cdk_output = {
            self.stack_name: {
                "LoadBalancerEndpoint": "abc"
            }
        }
        test_cluster.create_endpoint(cdk_output)
        self.assertEqual(test_cluster.cluster_endpoint_with_port, "https://abc:443")
        self.assertTrue(test_cluster.is_endpoint_public)
        self.assertEqual(test_cluster.endpoint, "abc")

    def test_cdk_failure_scenarios(self) -> None:
        test_cluster = PerfMultiNodeCluster(
            bundle_manifest=self.manifest, config=self.config, stack_name=self.stack_name,
            cluster_config=PerfTestClusterConfig(True, 1, 1, 0, 0), current_workspace="current_workspace")

        self.assertRaises(RuntimeError, test_cluster.create_endpoint, {self.stack_name: {}})
