# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import ClusterConfig
from test_workflow.integ_test.topology import Topology


class TopologyTests(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    def setUp(self) -> None:
        self.topology = 1
        mock_manifest = MagicMock()
        mock_manifest.build.version = "1.1.0"
        mock_manifest.build.distribution = "tar"
        self.manifest = mock_manifest

        self.bundle_manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.work_dir = "test_work_dir"

        self.component_name = "sql"
        self.security_enabled = True
        self.component_test_config = "test_config"
        self.additional_cluster_config = {"script.context.field.max_compilations_rate": "1000/1m"}
        self.save_logs = ""
        self.dependency_installer = None

    @patch("test_workflow.integ_test.topology.LocalTestCluster")
    def test_create_topology(self, mock_local_test_cluster: Mock) -> None:
        mock_test_recorder = MagicMock()
        dependency_installer = MagicMock()
        topology = Topology(
            [ClusterConfig({'cluster_name': 'cluster1', 'data_nodes': 1, 'cluster_manager_nodes': 0})],
            dependency_installer,
            self.work_dir,  # type: ignore
            self.component_name,
            self.additional_cluster_config,
            self.bundle_manifest,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        mock_local_test_cluster.create().__enter__.return_value = [{"endpoint": "localhost", "port": 9200, "transport": 9300}]
        mock_local_test_cluster.create_cluster = MagicMock()
        topology.create_clusters()  # type: ignore

        mock_local_test_cluster.create_cluster.assert_called_once_with(
            dependency_installer,
            os.path.join(self.work_dir, "1"),
            "sql",
            self.additional_cluster_config,
            self.bundle_manifest,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder,
            9200
        )
