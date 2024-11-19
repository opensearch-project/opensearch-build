# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from manifests_workflow.input_manifests_opensearch import InputManifestsOpenSearch


class TestInputManifestsOpenSearch(unittest.TestCase):
    def test_files(self) -> None:
        files = InputManifestsOpenSearch.files()
        self.assertTrue(len(files) >= 2)
        manifest = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "manifests",
                "3.0.0",
                "opensearch-3.0.0.yml",
            )
        )
        self.assertTrue(manifest in files)

    @patch("os.makedirs")
    @patch("os.chdir")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_cron")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_integTest_notification_cron")
    @patch("manifests.manifest.Manifest.to_file")
    @patch("manifests_workflow.input_manifests_opensearch.ComponentOpenSearchMin")
    def test_update(self, mock_component_opensearch_min: MagicMock, mock_manifest_to_file: MagicMock, mock_add_to_integTest_notification_cron: MagicMock,
                    mock_add_to_cron: MagicMock, mock_add_to_versionincrement_workflow: MagicMock,
                    *mocks: MagicMock) -> None:
        mock_component_opensearch_min.return_value = MagicMock(name="OpenSearch")
        mock_component_opensearch_min.branches.return_value = ["2.1000"]
        mock_component_opensearch_min.checkout.return_value = MagicMock(version="2.1000.1000")
        manifests = InputManifestsOpenSearch()
        manifests.update()
        self.assertEqual(mock_manifest_to_file.call_count, 2)
        calls = [
            call(
                os.path.join(
                    InputManifestsOpenSearch.manifests_path(),
                    "2.1000.1000",
                    "opensearch-2.1000.1000.yml",
                )
            )
        ]
        mock_manifest_to_file.assert_has_calls(calls)
        mock_add_to_integTest_notification_cron.assert_has_calls([
            call('2.1000.1000'),
        ])
        mock_add_to_cron.assert_has_calls([
            call('2.1000.1000'),
        ])
        mock_add_to_versionincrement_workflow.assert_has_calls([
            call('2.1000.1000'),
        ])

    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_cron")
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_integTest_notification_cron")
    @patch("manifests.manifest.Manifest.to_file")
    @patch("manifests_workflow.input_manifests_opensearch.ComponentOpenSearchMin")
    def test_update_outdated_branch(self, mock_component_opensearch_min: MagicMock, mock_manifest_to_file: MagicMock, mock_add_to_integTest_notification_cron: MagicMock,
                                    mock_add_to_cron: MagicMock, mock_add_to_versionincrement_workflow: MagicMock) -> None:
        mock_component_opensearch_min.return_value = MagicMock(name="OpenSearch")
        mock_component_opensearch_min.branches.return_value = ["1.2"]
        mock_component_opensearch_min.checkout.return_value = MagicMock(version="1.2.1000")
        manifests = InputManifestsOpenSearch()
        manifests.update()
        self.assertEqual(mock_manifest_to_file.call_count, 0)
        self.assertEqual(mock_add_to_cron.call_count, 0)
        self.assertEqual(mock_add_to_integTest_notification_cron.call_count, 0)
        self.assertEqual(mock_add_to_versionincrement_workflow.call_count, 0)
