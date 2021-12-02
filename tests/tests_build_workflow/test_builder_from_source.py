# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from build_workflow.build_target import BuildTarget
from build_workflow.builder_from_source import BuilderFromSource
from manifests.input_manifest import InputComponentFromSource
from paths.script_finder import ScriptFinder


class TestBuilderFromSource(unittest.TestCase):
    def setUp(self):
        self.builder = BuilderFromSource(
            InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref"}),
            BuildTarget(
                name="OpenSearch",
                version="1.1.0",
                platform="linux",
                architecture="x64",
                snapshot=False,
            ),
        )

    def test_builder(self):
        self.assertEqual(self.builder.component.name, "common-utils")

    @patch("build_workflow.builder_from_source.GitRepository")
    def test_build(self, mock_git_repo):
        mock_git_repo.return_value = MagicMock(working_directory="dir")
        build_recorder = MagicMock()
        self.builder.checkout("dir")
        self.builder.build(build_recorder)
        mock_git_repo.return_value.execute.assert_called_with(
            " ".join(
                [
                    "bash",
                    os.path.realpath(os.path.join(ScriptFinder.component_scripts_path, "common-utils", "build.sh")),
                    "-v 1.1.0",
                    "-p linux",
                    "-a x64",
                    "-s false",
                    "-o builds",
                ]
            )
        )
        build_recorder.record_component.assert_called_with("common-utils", mock_git_repo.return_value)

    @patch("build_workflow.builder_from_source.GitRepository")
    def test_build_snapshot(self, mock_git_repo):
        self.builder.target.snapshot = True
        mock_git_repo.return_value = MagicMock(working_directory="dir")
        build_recorder = MagicMock()
        self.builder.checkout("dir")
        self.builder.build(build_recorder)
        mock_git_repo.return_value.execute.assert_called_with(
            " ".join(
                [
                    "bash",
                    os.path.realpath(os.path.join(ScriptFinder.component_scripts_path, "common-utils", "build.sh")),
                    "-v 1.1.0",
                    "-p linux",
                    "-a x64",
                    "-s true",
                    "-o builds",
                ]
            )
        )
        build_recorder.record_component.assert_called_with("common-utils", self.builder.git_repo)

    def mock_os_walk(self, artifact_path):
        if artifact_path.endswith(os.path.join("dir", "builds", "core-plugins")):
            return [["core-plugins", [], ["plugin1.zip"]]]
        if artifact_path.endswith(os.path.join("dir", "builds", "maven")):
            return [("maven", [], ["artifact1.jar"])]
        else:
            return []

    @patch("os.walk")
    @patch("build_workflow.builder_from_source.GitRepository")
    def test_export_artifacts(self, mock_git_repo, mock_walk):
        build_recorder = MagicMock()
        mock_git_repo.return_value = MagicMock(working_directory="dir")
        mock_walk.side_effect = self.mock_os_walk
        self.builder.checkout("dir")
        self.builder.export_artifacts(build_recorder)
        self.assertEqual(build_recorder.record_artifact.call_count, 2)
        build_recorder.record_artifact.assert_has_calls(
            [
                call(
                    "common-utils",
                    "maven",
                    os.path.relpath(
                        os.path.join("maven", "artifact1.jar"),
                        os.path.join("dir", "artifacts"),
                    ),
                    os.path.join("maven", "artifact1.jar"),
                ),
                call(
                    "common-utils",
                    "core-plugins",
                    os.path.relpath(
                        os.path.join("core-plugins", "plugin1.zip"),
                        os.path.join("dir", "artifacts"),
                    ),
                    os.path.join("core-plugins", "plugin1.zip"),
                ),
            ]
        )
