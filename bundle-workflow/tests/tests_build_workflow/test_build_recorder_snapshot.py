# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget


class TestBuildRecorderSnapshot(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_recorder = BuildRecorder(
            BuildTarget(
                build_id="1",
                output_dir="output_dir",
                name="OpenSearch",
                version="1.1.0",
                arch="x64",
                snapshot=True,
            )
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

        self.assertEqual(
            self.build_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "architecture": "x64",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.1.0-SNAPSHOT",
                },
                "components": [
                    {
                        "artifacts": {},
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "name": "common-utils",
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/common-utils",
                        "version": "1.1.0.0-SNAPSHOT",
                    }
                ],
                "schema-version": "1.0",
            },
        )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin_zip_version(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with self.assertRaises(BuildRecorder.ArtifactInvalidError) as context:
            self.build_recorder.record_artifact(
                "security", "plugins", "../file1.zip", "invalid.zip"
            )
        self.assertEqual(
            "Artifact invalid.zip is invalid. Expected filename to include 1.1.0.0-SNAPSHOT.",
            context.exception.__str__(),
        )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin_version_properties_missing(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                ""
            )
            with self.assertRaises(BuildRecorder.ArtifactInvalidError) as context:
                self.build_recorder.record_artifact(
                    "security", "plugins", "../file1.zip", "valid-1.1.0.0-SNAPSHOT.zip"
                )
            self.assertEqual(
                "Artifact valid-1.1.0.0-SNAPSHOT.zip is invalid. Expected to have version='1.1.0.0-SNAPSHOT', but none was found.",
                context.exception.__str__(),
            )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin_version_properties_mismatch(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                "version=1.2.3.4"
            )
            with self.assertRaises(BuildRecorder.ArtifactInvalidError) as context:
                self.build_recorder.record_artifact(
                    "security", "plugins", "../file1.zip", "valid-1.1.0.0-SNAPSHOT.zip"
                )
            self.assertEqual(
                "Artifact valid-1.1.0.0-SNAPSHOT.zip is invalid. Expected to have version='1.1.0.0-SNAPSHOT', but was '1.2.3.4'.",
                context.exception.__str__(),
            )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin_version_properties(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                "opensearch.version=1.1.0\nversion=1.1.0.0-SNAPSHOT"
            )
            self.build_recorder.record_artifact(
                "security", "plugins", "../file1.zip", "valid-1.1.0.0-SNAPSHOT.zip"
            )
            manifest_dict = self.build_recorder.get_manifest().to_dict()
            self.assertEqual(manifest_dict["build"]["version"], "1.1.0-SNAPSHOT")
            self.assertEqual(
                manifest_dict["components"][0]["version"], "1.1.0.0-SNAPSHOT"
            )
