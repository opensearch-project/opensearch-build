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
    @patch("manifests_workflow.input_manifests.InputComponents")
    @patch("manifests_workflow.input_manifests.InputManifest.from_file")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_cron")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    @patch("manifests_workflow.input_manifests.InputManifest.from_path")
    @patch("manifests_workflow.input_manifests_opensearch_dashboards.ComponentOpenSearchDashboardsMin")
    @patch("manifests_workflow.input_manifests.InputManifest")
    def test_update(self, mock_input_manifest: MagicMock, mock_component_opensearch_min: MagicMock,
                    mock_input_manifest_from_path: MagicMock, mock_add_to_cron: MagicMock, mock_add_to_versionincrement_workflow: MagicMock,
                    mock_input_manifest_from_file: MagicMock, mock_input_manifest_component: MagicMock,
                    *mocks: MagicMock) -> None:
        mock_component_opensearch_min.return_value = MagicMock(name="OpenSearch-Dashboards")
        mock_component_opensearch_min.branches.return_value = ["main", "0.9.0"]
        mock_component_opensearch_min.checkout.return_value = MagicMock(version="0.9.0")
        mock_input_manifest_from_path.return_value = MagicMock(components=[])

        manifests = InputManifestsOpenSearchDashboards()
        manifests.update()
        self.assertEqual(mock_input_manifest_from_file().to_file.call_count, 1)
        calls = [
            call(
                os.path.join(
                    InputManifestsOpenSearchDashboards.manifests_path(),
                    "0.9.0",
                    "opensearch-dashboards-0.9.0.yml",
                )
            )
        ]
        mock_input_manifest_from_file().to_file.assert_has_calls(calls)
        mock_add_to_cron.assert_has_calls([
            call('0.9.0')
        ])
        mock_add_to_versionincrement_workflow.assert_has_calls([
            call('0.9.0')
        ])
