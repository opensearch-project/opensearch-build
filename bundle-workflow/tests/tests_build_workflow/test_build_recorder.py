# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import yaml

from build_workflow.build_recorder import BuildRecorder
from manifests.build_manifest import BuildManifest


class TestBuildRecorder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_recorder = BuildRecorder(
            "1", "output_dir", "OpenSearch", "1.1", "x64", False
        )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_component_and_artifact(self, mock_makedirs, mock_copyfile):
        self.build_recorder.record_component(
            "common-utils",
            MagicMock(
                url="https://github.com/opensearch-project/common-utils",
                ref="main",
                sha="3913d7097934cbfe1fdcf919347f22a597d00b76",
            ),
        )

        self.build_recorder.record_artifact(
            "common-utils", "/files", "../file1.jar", __file__
        )

        self.build_recorder.record_artifact(
            "common-utils", "/files", "../file2.jar", __file__
        )

        self.assertEqual(
            self.build_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "architecture": "x64",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.1",
                },
                "components": [
                    {
                        "artifacts": {"/files": ["../file1.jar", "../file2.jar"]},
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "name": "common-utils",
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/common-utils",
                    }
                ],
                "schema-version": "1.0",
            },
        )

        mock_copyfile.assert_called()
        mock_makedirs.assert_called()

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact(self, mock_makedirs, mock_copyfile):
        self.build_recorder.record_component(
            "common-utils",
            MagicMock(
                url="https://github.com/opensearch-project/common-utils",
                ref="main",
                sha="3913d7097934cbfe1fdcf919347f22a597d00b76",
            ),
        )

        self.build_recorder.record_artifact(
            "common-utils", "/files", "../file1.jar", __file__
        )

        mock_makedirs.assert_called_with("output_dir/..", exist_ok=True)
        mock_copyfile.assert_called_with(__file__, "output_dir/../file1.jar")

    def test_get_manifest(self):
        manifest = self.build_recorder.get_manifest()
        self.assertIs(type(manifest), BuildManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "architecture": "x64",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.1",
                },
                "components": [],
                "schema-version": "1.0",
            },
        )

    def test_write_manifest(self):
        with tempfile.TemporaryDirectory() as dest_dir:
            self.build_recorder.write_manifest(dest_dir)
            manifest_path = os.path.join(dest_dir, "manifest.yml")
            self.assertTrue(os.path.isfile(manifest_path))
            data = self.build_recorder.get_manifest().to_dict()
            with open(manifest_path) as f:
                self.assertEqual(yaml.safe_load(f), data)
