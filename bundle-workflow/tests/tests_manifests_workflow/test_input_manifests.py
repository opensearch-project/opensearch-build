# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from manifests.input_manifest import InputManifest
from manifests_workflow.input_manifests import InputManifests


class TestInputManifests(unittest.TestCase):
    def test_files(self):
        files = InputManifests.files()
        self.assertTrue(len(files) >= 2)
        manifest = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "../../../manifests/1.1.0/opensearch-1.1.0.yml",
            )
        )
        self.assertTrue(manifest in files)

    def test_manifests_path(self):
        path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../../../manifests/")
        )
        self.assertEqual(path, InputManifests.manifests_path())

    @patch("os.makedirs")
    @patch("os.chdir")
    @patch("manifests_workflow.input_manifests.InputManifest.from_path")
    @patch("manifests_workflow.input_manifests.ComponentOpenSearchMin")
    @patch("manifests_workflow.input_manifests.ComponentOpenSearch")
    @patch("system.temporary_directory.TemporaryDirectory")
    @patch("manifests_workflow.input_manifests.InputManifest")
    def test_update(
        self,
        mock_input_manifest,
        mock_tmpdir,
        mock_component_opensearch,
        mock_component_opensearch_min,
        mock_input_manifest_from_path,
        *mocks
    ):
        mock_tmpdir.__enter__.return_value = "dir"
        mock_component_opensearch_min.return_value = MagicMock(name="OpenSearch")
        mock_component_opensearch_min.get_branches.return_value = ["main", "0.9.0"]
        mock_component_opensearch_min.checkout.return_value = MagicMock(version="0.9.0")
        mock_component_opensearch.return_value = MagicMock(name="common-utils")
        mock_component_opensearch.checkout.return_value = MagicMock(version="0.10.0")
        mock_input_manifest_from_path.return_value = MagicMock(
            components=[
                InputManifest.Component(
                    {"name": "common-utils", "repository": "git", "ref": "ref"}
                )
            ]
        )
        manifests = InputManifests()
        manifests.update()
        self.assertEqual(mock_input_manifest().to_file.call_count, 2)
        calls = [
            call(
                os.path.join(
                    InputManifests.manifests_path(), "0.10.0/opensearch-0.10.0.yml"
                )
            ),
            call(
                os.path.join(
                    InputManifests.manifests_path(), "0.9.0/opensearch-0.9.0.yml"
                )
            ),
        ]
        mock_input_manifest().to_file.assert_has_calls(calls)
