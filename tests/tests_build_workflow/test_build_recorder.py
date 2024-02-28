# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import yaml

from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget
from build_workflow.opensearch.build_artifact_check_maven import BuildArtifactOpenSearchCheckMaven
from build_workflow.opensearch.build_artifact_check_plugin import BuildArtifactOpenSearchCheckPlugin
from manifests.build_manifest import BuildManifest
from system.temporary_directory import TemporaryDirectory


class TestBuildRecorder(unittest.TestCase):
    def __mock(self, snapshot: bool = True) -> BuildRecorder:
        return BuildRecorder(
            BuildTarget(
                build_id="1",
                output_dir="output_dir",
                name="OpenSearch",
                version="1.3.0",
                platform="linux",
                architecture="x64",
                snapshot=snapshot,
            )
        )

    def __mock_with_manifest(self, snapshot: bool = True) -> BuildRecorder:
        build_manifest_path = os.path.join("tests", "tests_build_workflow", "data", "opensearch-build-tar-2.12.0.yml")
        build_manifest = BuildManifest.from_path(build_manifest_path)
        return BuildRecorder(
            BuildTarget(
                build_id="1",
                output_dir="output_dir",
                name="OpenSearch",
                version="1.3.0",
                platform="linux",
                architecture="x64",
                snapshot=snapshot,
            ),
            build_manifest
        )

    def __mock_distribution(self, snapshot: bool = True) -> BuildRecorder:
        return BuildRecorder(
            BuildTarget(
                build_id="1",
                output_dir="output_dir",
                name="OpenSearch",
                version="1.3.0",
                platform="linux",
                architecture="x64",
                distribution="rpm",
                snapshot=snapshot,
            )
        )

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_component_and_artifact(self, mock_makedirs: Mock, mock_copyfile: Mock) -> None:
        recorder = self.__mock(snapshot=False)

        recorder.record_component(
            "common-utils",
            MagicMock(
                url="https://github.com/opensearch-project/common-utils",
                ref="main",
                sha="3913d7097934cbfe1fdcf919347f22a597d00b76",
            ),
        )

        recorder.record_artifact("common-utils", "libs", "../file1.jar", __file__)

        recorder.record_artifact("common-utils", "libs", "../file2.jar", __file__)

        self.assertEqual(
            recorder.get_manifest().to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.3.0",
                },
                "components": [
                    {
                        "artifacts": {"libs": ["../file1.jar", "../file2.jar"]},
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "name": "common-utils",
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/common-utils",
                        "version": "1.3.0.0",
                    }
                ],
                "schema-version": "1.2",
            },
        )

        mock_copyfile.assert_called()
        mock_makedirs.assert_called()

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact(self, mock_makedirs: Mock, mock_copyfile: Mock) -> None:
        recorder = self.__mock(snapshot=False)

        recorder.record_component(
            "common-utils",
            MagicMock(
                url="https://github.com/opensearch-project/common-utils",
                ref="main",
                sha="3913d7097934cbfe1fdcf919347f22a597d00b76",
            ),
        )

        recorder.record_artifact("common-utils", "files", os.path.join("..", "file1.jar"), __file__)

        output_dir = os.path.join("output_dir", "..")
        mock_makedirs.assert_called_with(output_dir, exist_ok=True)
        mock_copyfile.assert_called_with(__file__, os.path.join(output_dir, "file1.jar"))

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_plugin(self, mock_makedirs: Mock, mock_copyfile: Mock) -> None:
        recorder = self.__mock(snapshot=False)

        recorder.record_component("security", MagicMock())

        with patch.object(BuildArtifactOpenSearchCheckPlugin, "check") as mock_check:
            recorder.record_artifact("security", "plugins", "../file1.zip", "invalid.file")

        mock_check.assert_called_with("invalid.file")
        mock_copyfile.assert_called()
        mock_makedirs.assert_called()

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    def test_record_artifact_check_maven(self, mock_makedirs: Mock, mock_copyfile: Mock) -> None:
        recorder = self.__mock(snapshot=False)

        recorder.record_component("security", MagicMock())

        with patch.object(BuildArtifactOpenSearchCheckMaven, "check") as mock_check:
            recorder.record_artifact("security", "maven", "../file1.zip", "valid.jar")

        mock_check.assert_called_with("valid.jar")
        mock_copyfile.assert_called()
        mock_makedirs.assert_called()

    def test_get_manifest(self) -> None:
        manifest = self.__mock(snapshot=False).get_manifest()
        self.assertIs(type(manifest), BuildManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.3.0",
                },
                "schema-version": "1.2",
            },
        )

    def test_get_manifest_distribution(self) -> None:
        manifest = self.__mock_distribution(snapshot=False).get_manifest()
        self.assertIs(type(manifest), BuildManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "rpm",
                    "id": "1",
                    "name": "OpenSearch",
                    "version": "1.3.0",
                },
                "schema-version": "1.2",
            },
        )

    def test_write_manifest(self) -> None:
        with TemporaryDirectory() as dest_dir:
            mock = self.__mock(snapshot=False)
            mock.target.output_dir = dest_dir.name
            mock.write_manifest()
            manifest_path = os.path.join(dest_dir.name, "manifest.yml")
            self.assertTrue(os.path.isfile(manifest_path))
            data = mock.get_manifest().to_dict()
            with open(manifest_path) as f:
                self.assertEqual(yaml.safe_load(f), data)

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    @patch.object(BuildArtifactOpenSearchCheckPlugin, "check")
    def test_record_artifact_check_plugin_version_properties(self, mock_plugin_check: Mock, mock_makedirs: Mock,
                                                             mock_copyfile: Mock) -> None:
        mock = self.__mock(snapshot=False)
        mock.record_component(
            "security",
            MagicMock(
                url="https://github.com/opensearch-project/security",
                ref="main",
                sha="3913d7097934cbfe1fdcf919347f22a597d00b76",
            ),
        )
        mock.record_artifact("security", "plugins", "../file1.zip", "valid-1.3.0.0.zip")
        manifest_dict = mock.get_manifest().to_dict()
        self.assertEqual(manifest_dict["build"]["version"], "1.3.0")
        self.assertEqual(manifest_dict["components"][0]["version"], "1.3.0.0")
        mock_plugin_check.assert_called()
        mock_copyfile.assert_called()
        mock_makedirs.assert_called()

    @patch("shutil.copyfile")
    @patch("os.makedirs")
    @patch.object(BuildArtifactOpenSearchCheckPlugin, "check")
    def test_record_artifact_check_plugin_version_properties_snapshot(self, mock_plugin_check: Mock,
                                                                      mock_makedirs: Mock, mock_copyfile: Mock) -> None:
        mock = self.__mock(snapshot=True)
        mock.record_component(
            "security",
            MagicMock(
                url="https://github.com/opensearch-project/security",
                ref="main",
                sha="3913d7097934cbfe1fdcf919347f22a597d00b76",
            ),
        )
        mock.record_artifact("security", "plugins", "../file1.zip", "valid-1.3.0.0-SNAPSHOT.zip")
        manifest_dict = mock.get_manifest().to_dict()
        self.assertEqual(manifest_dict["build"]["version"], "1.3.0-SNAPSHOT")
        self.assertEqual(manifest_dict["components"][0]["version"], "1.3.0.0-SNAPSHOT")
        mock_plugin_check.assert_called()
        mock_copyfile.assert_called()
        mock_makedirs.assert_called()

    def test_append_component_with_existing_manifest(self) -> None:
        mock = self.__mock_with_manifest(snapshot=False)

        self.assertEqual(mock.build_manifest.components_hash.get("job-scheduler").get("commit_id"),
                         "aaf09b0211df15dd74ff2756f2590c360b03486b")
        self.assertEqual(mock.build_manifest.components_hash.get("geospatial").get("commit_id"),
                         "8776900f2f26312b4d3a08e4343f3e3f7bdde536")
        self.assertEqual(mock.build_manifest.components_hash.get("geospatial").get("repository"),
                         "https://github.com/opensearch-project/geospatial.git")
        self.assertEqual(mock.build_manifest.components_hash.get("security").get("commit_id"),
                         "e3c8902dea26fd20f56a6f144042b2623f652e3e")
        self.assertEqual(mock.build_manifest.components_hash.get("security").get("version"), "2.12.0.0")

        self.assertEqual(mock.build_manifest.data.get("build").get("id"), "1")

        mock.record_component(
            "job-scheduler",
            MagicMock(
                url="https://github.com/opensearch-project/job-scheduler.git",
                ref="2.12",
                sha="mockcommitid",
            ),
        )

        self.assertEqual(mock.build_manifest.components_hash.get("job-scheduler").get("commit_id"), "mockcommitid")
        self.assertEqual(mock.build_manifest.components_hash.get("job-scheduler").get("ref"), "2.12")
        self.assertEqual(mock.build_manifest.components_hash.get("job-scheduler").get("repository"),
                         "https://github.com/opensearch-project/job-scheduler.git")
        self.assertEqual(mock.build_manifest.components_hash.get("geospatial").get("commit_id"),
                         "8776900f2f26312b4d3a08e4343f3e3f7bdde536")
        self.assertEqual(mock.build_manifest.components_hash.get("security").get("commit_id"),
                         "e3c8902dea26fd20f56a6f144042b2623f652e3e")
