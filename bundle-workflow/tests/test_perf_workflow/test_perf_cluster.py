# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_cluster import PerfTestCluster


class TestPerfCluster(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "data")
        )
        self.manifest_filename = os.path.join(
            self.data_path, "test_manifest.yaml"
        )
        self.manifest = BundleManifest.from_path(self.manifest_filename)
        self.stack_name = 'stack'
        self.security = 'disable'
        config = {
            'Constants': {
                'SecurityGroupId': 'sg-00000000',
                'VpcId': 'vpc-12345',
                'AccountId': '12345678',
                'Region': 'us-west-2',
                'Role': 'role-arn'
            }
        }
        self.perf_test_cluster = PerfTestCluster(
            bundle_manifest=self.manifest, config=config, stack_name=self.stack_name, security=self.security
        )

    def test_create(self):
        mock_file = MagicMock(side_effect=[{"stack": {"PrivateIp": "10.10.10.10"}}])
        with patch('test_workflow.perf_test_cluster.os.chdir') as mock_chdir:
            with patch("subprocess.check_call") as mock_check_call:
                with patch("builtins.open", MagicMock()):
                    with patch("json.load", mock_file):
                        self.perf_test_cluster.create()
                        mock_chdir.assert_called_once_with('tools/cdk/mensor/single-node/')
                        self.assertEqual(mock_check_call.call_count, 1)

    def test_endpoint(self):
        self.assertEqual(self.perf_test_cluster.endpoint(), None)

    def test_port(self):
        self.assertEqual(self.perf_test_cluster.port(), 443)

    def test_destroy(self):
        with patch('test_workflow.perf_test_cluster.os.chdir') as mock_chdir:
            with patch("subprocess.check_call") as mock_check_call:
                self.perf_test_cluster.destroy()
                mock_chdir.assert_called_once_with('tools/cdk/mensor/single-node/')
                self.assertEqual(mock_check_call.call_count, 1)
