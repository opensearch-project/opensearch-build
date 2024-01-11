# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import List
from unittest.mock import MagicMock, patch

from build_workflow.build_incremental import BuildIncremental
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputManifest


class TestBuildIncremental(unittest.TestCase):
    INPUT_MANIFEST = InputManifest.from_path(
        os.path.join(os.path.dirname(__file__), "data", "opensearch-input-2.12.0.yml"))
    BUILD_MANIFEST = BuildManifest.from_path(
        os.path.join(os.path.dirname(__file__), "data", "opensearch-build-tar-2.12.0.yml"))
    BUILD_MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-tar-2.12.0.yml")
    INPUT_MANIFEST_DASHBOARDS = InputManifest.from_path(
        os.path.join(os.path.dirname(__file__), "data", "opensearch-dashboards-input-2.12.0.yml"))
    BUILD_MANIFEST_DASHBOARDS = BuildManifest.from_path(
        os.path.join(os.path.dirname(__file__), "data", "opensearch-dashboards-build-tar-2.12.0.yml"))
    buildIncremental = BuildIncremental(INPUT_MANIFEST, "tar")

    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("manifests.input_manifest.InputManifest.stable")
    def test_no_commits_diff(self, stable_mock_input_manifest: MagicMock, mock_build_manifest: MagicMock, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = True
        input_manifest_data = {'schema-version': '1.1', 'build': {'name': 'OpenSearch', 'version': '2.12.0'},
                               'components': [{'name': 'OpenSearch',
                                               'repository': 'https://github.com/opensearch-project/OpenSearch.git',
                                               'ref': '05c2befd7d01fab4aef4f0d3d6722d2da240b2c6',
                                               'checks': ['gradle:publish', 'gradle:properties:version']}]}
        build_manifest_data = {'schema-version': '1.2',
                               'build': {'name': 'OpenSearch', 'version': '2.12.0', 'platform': 'linux',
                                         'architecture': 'x64', 'id': 'b2b848e29077488ca7e8c37501b36c87'},
                               'components': [{'name': 'OpenSearch',
                                               'repository': 'https://github.com/opensearch-project/OpenSearch.git',
                                               'ref': '2.x', 'commit_id': '05c2befd7d01fab4aef4f0d3d6722d2da240b2c6',
                                               'version': '2.12.0.0'}]}
        stable_mock_input_manifest.return_value = InputManifest(input_manifest_data)
        mock_build_manifest.return_value = BuildManifest(build_manifest_data)

        diff_list = self.buildIncremental.commits_diff(self.INPUT_MANIFEST)

        self.assertFalse(diff_list)
        self.assertEqual(len(diff_list), 0)

    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("manifests.input_manifest.InputManifest.stable")
    def test_commits_diff(self, stable_mock_input_manifest: MagicMock, mock_build_manifest: MagicMock, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = True
        stable_mock_input_manifest.return_value = self.INPUT_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST

        diff_list = self.buildIncremental.commits_diff(self.INPUT_MANIFEST)

        stable_mock_input_manifest.assert_called_once()
        mock_build_manifest.assert_called_once()
        self.assertIsNotNone(diff_list)
        self.assertEqual(len(diff_list), 8)
        self.assertTrue("k-NN" in diff_list)
        self.assertTrue("geospatial" in diff_list)
        self.assertTrue("security" in diff_list)
        self.assertTrue("cross-cluster-replication" in diff_list)
        self.assertTrue("ml-commons" in diff_list)
        self.assertTrue("neural-search" in diff_list)
        self.assertTrue("opensearch-observability" in diff_list)
        self.assertTrue("security-analytics" in diff_list)

    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("manifests.input_manifest.InputManifest.stable")
    def test_commits_diff_build_manifest_not_exists(self, stable_mock_input_manifest: MagicMock, mock_build_manifest: MagicMock, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = False
        stable_mock_input_manifest.return_value = self.INPUT_MANIFEST_DASHBOARDS
        mock_build_manifest.return_value = self.BUILD_MANIFEST_DASHBOARDS

        diff_list = self.buildIncremental.commits_diff(self.INPUT_MANIFEST_DASHBOARDS)
        stable_mock_input_manifest.assert_not_called()
        mock_build_manifest.assert_not_called()
        self.assertEqual(diff_list, ["OpenSearch-Dashboards"])

    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("manifests.input_manifest.InputManifest.stable")
    def test_commits_diff_for_different_version(self, stable_mock_input_manifest: MagicMock, mock_build_manifest: MagicMock, mock_path_exists: MagicMock) -> None:
        mock_path_exists.return_value = True
        input_manifest_data = {'schema-version': '1.1',
                               'build': {'name': 'OpenSearch', 'version': '2.12.0'},
                               'components': [{'name': 'OpenSearch',
                                               'repository': 'https://github.com/opensearch-project/OpenSearch.git',
                                               'ref': '05c2befd7d01fab4aef4f0d3d6722d2da240b2c6',
                                               'checks': ['gradle:publish', 'gradle:properties:version']}]}
        build_manifest_data = {'schema-version': '1.2',
                               'build': {'name': 'OpenSearch', 'version': '2.11.0', 'platform': 'linux',
                                         'architecture': 'x64', 'id': 'b2b848e29077488ca7e8c37501b36c87'},
                               'components': [{'name': 'OpenSearch',
                                               'repository': 'https://github.com/opensearch-project/OpenSearch.git',
                                               'ref': '2.x', 'commit_id': '05c2befd7d01fab4aef4f0d3d6722d2da240b2c6',
                                               'version': '2.12.0.0'}]}
        stable_mock_input_manifest.return_value = InputManifest(input_manifest_data)
        mock_build_manifest.return_value = BuildManifest(build_manifest_data)
        diff_list = self.buildIncremental.commits_diff(self.INPUT_MANIFEST)

        stable_mock_input_manifest.assert_called_once()
        mock_build_manifest.assert_called_once()
        self.assertEqual(diff_list, ["OpenSearch"])

    def test_rebuild_plugins_with_no_update(self) -> None:
        diff_list: List[str] = []
        rebuild_list = self.buildIncremental.rebuild_plugins(diff_list, self.INPUT_MANIFEST)
        self.assertFalse(rebuild_list)
        self.assertEqual(len(rebuild_list), 0)

    def test_rebuild_plugins_with_core_update(self) -> None:
        diff_list = ["OpenSearch", "alerting"]
        rebuild_list = self.buildIncremental.rebuild_plugins(diff_list, self.INPUT_MANIFEST)

        self.assertTrue(rebuild_list)
        self.assertEqual(len(rebuild_list), 19)
        for component in rebuild_list:
            self.assertTrue(component in self.INPUT_MANIFEST.components)

    def test_rebuild_plugins_without_core(self) -> None:
        diff_list_cu = ["common-utils"]
        rebuild_list_cu = self.buildIncremental.rebuild_plugins(diff_list_cu, self.INPUT_MANIFEST)
        self.assertTrue(rebuild_list_cu)
        self.assertEqual(len(rebuild_list_cu), 13)
        self.assertTrue("common-utils" in rebuild_list_cu)
        self.assertTrue("asynchronous-search" in rebuild_list_cu)
        self.assertTrue("sql" in rebuild_list_cu)

        diff_list_js = ["job-scheduler"]
        rebuild_list_js = self.buildIncremental.rebuild_plugins(diff_list_js, self.INPUT_MANIFEST)
        self.assertTrue(rebuild_list_js)
        self.assertEqual(len(rebuild_list_js), 5)
        self.assertTrue("job-scheduler" in rebuild_list_js)
        self.assertTrue("anomaly-detection" in rebuild_list_js)

        diff_list_geo = ["geospatial"]
        rebuild_list_geo = self.buildIncremental.rebuild_plugins(diff_list_geo, self.INPUT_MANIFEST)
        self.assertTrue(rebuild_list_geo)
        self.assertEqual(len(rebuild_list_geo), 1)
        self.assertTrue("geospatial" in rebuild_list_js)

    def test_rebuild_plugins_with_dashboards(self) -> None:
        buildIncrementDashboards = BuildIncremental(self.INPUT_MANIFEST_DASHBOARDS, "tar")
        diff_list = ["observabilityDashboards"]
        rebuild_list = buildIncrementDashboards.rebuild_plugins(diff_list, self.INPUT_MANIFEST_DASHBOARDS)
        self.assertTrue(rebuild_list)
        self.assertEqual(len(rebuild_list), 2)
        self.assertTrue("OpenSearch-Dashboards" in rebuild_list)
        self.assertTrue("observabilityDashboards" in rebuild_list)
