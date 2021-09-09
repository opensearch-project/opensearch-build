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
from build_workflow.build_target import BuildTarget
from manifests.build_manifest import BuildManifest


class TestBuildRecorder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.build_recorder = BuildRecorder(
            BuildTarget(
                build_id="1",
                output_dir="output_dir",
                name="OpenSearch",
                version="1.1.0",
                arch="x64",
                snapshot=False,
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

        self.build_recorder.record_artifact(
            "common-utils", "files", "../file1.jar", __file__
        )

        self.build_recorder.record_artifact(
            "common-utils", "files", "../file2.jar", __file__
        )

        self.assertEqual(
            self.build_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "architecture": "x64",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.1.0",
                },
                "components": [
                    {
                        "artifacts": {"files": ["../file1.jar", "../file2.jar"]},
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "name": "common-utils",
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/common-utils",
                        "version": "1.1.0.0",
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
            "common-utils", "files", "../file1.jar", __file__
        )

        mock_makedirs.assert_called_with("output_dir/..", exist_ok=True)
        mock_copyfile.assert_called_with(__file__, "output_dir/../file1.jar")

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin_zip_extension(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with self.assertRaises(BuildRecorder.ArtifactInvalidError) as context:
            self.build_recorder.record_artifact(
                "security", "plugins", "../file1.zip", "invalid.file"
            )
        self.assertEqual(
            "Artifact invalid.file is invalid. Not a zip file.",
            context.exception.__str__(),
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
            "Artifact invalid.zip is invalid. Expected filename to include 1.1.0.0.",
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
                    "security", "plugins", "../file1.zip", "valid-1.1.0.0.zip"
                )
            self.assertEqual(
                "Artifact valid-1.1.0.0.zip is invalid. Expected to have version='1.1.0.0', but none was found.",
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
                    "security", "plugins", "../file1.zip", "valid-1.1.0.0.zip"
                )
            self.assertEqual(
                "Artifact valid-1.1.0.0.zip is invalid. Expected to have version='1.1.0.0', but was '1.2.3.4'.",
                context.exception.__str__(),
            )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin_version_properties(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                "opensearch.version=1.1.0\nversion=1.1.0.0"
            )
            self.build_recorder.record_artifact(
                "security", "plugins", "../file1.zip", "valid-1.1.0.0.zip"
            )
            manifest_dict = self.build_recorder.get_manifest().to_dict()
            self.assertEqual(manifest_dict["build"]["version"], "1.1.0")
            self.assertEqual(manifest_dict["components"][0]["version"], "1.1.0.0")

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_maven_version_properties_mismatch(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                "Implementation-Version: 1.2.3.4"
            )
            with self.assertRaises(BuildRecorder.ArtifactInvalidError) as context:
                self.build_recorder.record_artifact(
                    "security", "maven", "../file1.zip", "valid.jar"
                )
            self.assertEqual(
                "Artifact valid.jar is invalid. Expected to have Implementation-Version=any of ['1.1.0.0', '1.1.0', None], but was '1.2.3.4'.",
                context.exception.__str__(),
            )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_maven_version_properties_none(self, *mocks):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                ""
            )
            self.build_recorder.record_artifact(
                "security", "maven", "../file1.jar", "valid.jar"
            )
            manifest_dict = self.build_recorder.get_manifest().to_dict()
            self.assertEqual(manifest_dict["build"]["version"], "1.1.0")
            self.assertEqual(
                manifest_dict["components"][0]["artifacts"]["maven"], ["../file1.jar"]
            )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_maven_artifact_after_checking_maven_version_properties(
        self, *mocks
    ):
        self.build_recorder.record_component("security", MagicMock())
        with patch("build_workflow.build_recorder.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                "Implementation-Version: 1.1.0.0"
            )
            self.build_recorder.record_artifact(
                "security", "maven", "../file1.jar", "valid.jar"
            )
            manifest_dict = self.build_recorder.get_manifest().to_dict()
            self.assertEqual(manifest_dict["build"]["version"], "1.1.0")
            self.assertEqual(
                manifest_dict["components"][0]["artifacts"]["maven"], ["../file1.jar"]
            )

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
                    "version": "1.1.0",
                },
                "components": [],
                "schema-version": "1.0",
            },
        )

    def test_write_manifest(self):
        with tempfile.TemporaryDirectory() as dest_dir:
            self.build_recorder.target.output_dir = dest_dir
            self.build_recorder.write_manifest()
            manifest_path = os.path.join(dest_dir, "manifest.yml")
            self.assertTrue(os.path.isfile(manifest_path))
            data = self.build_recorder.get_manifest().to_dict()
            with open(manifest_path) as f:
                self.assertEqual(yaml.safe_load(f), data)
