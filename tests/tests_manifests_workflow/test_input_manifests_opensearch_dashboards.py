# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from manifests_workflow.input_manifests_opensearch_dashboards import InputManifestsOpenSearchDashboards


class TestInputManifestsOpenSearchDashboards(unittest.TestCase):
    def test_files(self) -> None:
        files = InputManifestsOpenSearchDashboards.files()
        self.assertTrue(len(files) >= 1)
        manifest = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "manifests",
                "3.0.0",
                "opensearch-dashboards-3.0.0.yml",
            )
        )
        self.assertTrue(manifest in files)

    @patch("os.makedirs")
    @patch("os.chdir")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_cron")
    @patch("manifests.manifest.Manifest.to_file")
    @patch("manifests_workflow.input_manifests_opensearch_dashboards.ComponentOpenSearchDashboardsMin")
    def test_update(self, mock_component_opensearch_dashboards_min: MagicMock, mock_manifest_to_file: MagicMock,
                    mock_add_to_cron: MagicMock, mock_add_to_versionincrement_workflow: MagicMock,
                    mock_os_chdir: MagicMock, mock_os_makedirs: MagicMock) -> None:
        mock_component_opensearch_dashboards_min.return_value = MagicMock(name="OpenSearch-Dashboards")
        mock_component_opensearch_dashboards_min.branches.return_value = ["2.12"]
        mock_component_opensearch_dashboards_min.checkout.return_value = MagicMock(version="2.12.1000")

        manifests = InputManifestsOpenSearchDashboards()
        manifests.update()
        self.assertEqual(mock_manifest_to_file.call_count, 1)
        calls = [
            call(
                os.path.join(
                    InputManifestsOpenSearchDashboards.manifests_path(),
                    "2.12.1000",
                    "opensearch-dashboards-2.12.1000.yml",
                )
            )
        ]
        mock_manifest_to_file.assert_has_calls(calls)
        mock_add_to_cron.assert_has_calls([
            call('2.12.1000')
        ])
        mock_add_to_versionincrement_workflow.assert_has_calls([
            call('2.12.1000')
        ])

    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_cron")
    @patch("manifests.manifest.Manifest.to_file")
    @patch("manifests_workflow.input_manifests_opensearch_dashboards.ComponentOpenSearchDashboardsMin")
    def test_update_outdated_branch(self, mock_component_opensearch_dashboards_min: MagicMock, mock_manifest_to_file: MagicMock,
                                    mock_add_to_cron: MagicMock, mock_add_to_versionincrement_workflow: MagicMock) -> None:
        mock_component_opensearch_dashboards_min.return_value = MagicMock(name="OpenSearch-Dashboards")
        mock_component_opensearch_dashboards_min.branches.return_value = ["1.2"]
        mock_component_opensearch_dashboards_min.checkout.return_value = MagicMock(version="1.2.1000")

        manifests = InputManifestsOpenSearchDashboards()
        manifests.update()
        self.assertEqual(mock_manifest_to_file.call_count, 0)
        self.assertEqual(mock_add_to_cron.call_count, 0)
        self.assertEqual(mock_add_to_versionincrement_workflow.call_count, 0)
