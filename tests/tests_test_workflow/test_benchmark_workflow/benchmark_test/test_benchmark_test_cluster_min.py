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

from manifests.build_manifest import BuildManifest
from test_workflow.benchmark_test.benchmark_create_cluster import BenchmarkCreateCluster


class TestBenchmarkCreateClusterMin(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    MIN_MANIFEST = os.path.join(DATA, "min_distribution_manifest.yml")

    def setUp(self, args: Optional[Mock] = None) -> None:
        self.args = Mock()

        self.args.workload = "nyc_taxis"
        self.args.stack_suffix = "test-suffix"
        self.args.insecure = True
        self.args.single_node = False
        self.args.min_distribution = True
        self.manifest = BuildManifest.from_path(self.MIN_MANIFEST)
        self.stack_name = "stack"
        self.security = True
        self.config = {"Constants": {"SecurityGroupId": "sg-00000000", "VpcId": "vpc-12345", "AccountId": "12345678",
                                     "Region": "us-west-2", "Role": "role-arn", "serverAccessType": "prefixList", "restrictServerAccessTo": "pl-1234",
                                     "isInternal": "true", "IamRoleArn": ""}}
        self.benchmark_create_cluster = BenchmarkCreateCluster(bundle_manifest=self.manifest, config=self.config, args=self.args, current_workspace="current_workspace")

    @patch("test_workflow.benchmark_test.benchmark_create_cluster.BenchmarkCreateCluster.wait_for_processing")
    def test_create_min_cluster(self, mock_wait_for_processing: Optional[Mock]) -> None:
        mock_file = MagicMock(side_effect=[{"opensearch-infra-stack-test-suffix-8042-arm64": {"loadbalancerurl": "www.example.com"}}])
        with patch("subprocess.check_call") as mock_check_call:
            with patch("builtins.open", MagicMock()):
                with patch("json.load", mock_file):
                    self.benchmark_create_cluster.start()
                    self.assertEqual(mock_check_call.call_count, 1)
        self.assertTrue(isinstance(self.manifest, BuildManifest))
        self.assertTrue("securityDisabled=true" in self.benchmark_create_cluster.params)
        self.assertTrue("minDistribution=true" in self.benchmark_create_cluster.params)
        self.assertTrue("distributionUrl=https://artifacts.opensearch.org/snapshots/core/opensearch/2.9.0-SNAPSHOT/"
                        "opensearch-min-2.9.0-SNAPSHOT-linux-arm64-latest.tar.gz" in self.benchmark_create_cluster.params)
        self.assertTrue("customRoleArn" not in self.benchmark_create_cluster.params)
