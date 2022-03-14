# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any, List
from unittest.mock import MagicMock, Mock, call, patch

from build_workflow.build_target import BuildTarget
from build_workflow.builder_from_source import BuilderFromSource
from manifests.input_manifest import InputComponentFromSource
from paths.script_finder import ScriptFinder


class TestBuilderFromSource(unittest.TestCase):
    def setUp(self) -> None:
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

        self.builder_distribution = BuilderFromSource(
            InputComponentFromSource({"name": "OpenSearch", "repository": "url", "ref": "ref"}),
            BuildTarget(
                name="OpenSearch",
                version="1.3.0",
                platform="linux",
                architecture="x64",
                distribution="tar",
                snapshot=False,
            ),
        )

        self.builder_distribution_support = BuilderFromSource(
            InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref"}),
            BuildTarget(
                name="OpenSearch",
                version="1.3.0",
                platform="linux",
                architecture="x64",
                distribution="rpm",
                snapshot=False,
            ),
        )

    def test_builder(self) -> None:
        self.assertEqual(self.builder.component.name, "common-utils")

    @patch("build_workflow.builder_from_source.GitRepository")
    def test_build(self, mock_git_repo: Mock) -> None:
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
    def test_build_distribution(self, mock_git_repo: Mock) -> None:
        mock_git_repo.return_value = MagicMock(working_directory="dir")
        build_recorder = MagicMock()
        self.builder_distribution.checkout("dir")
        self.builder_distribution.build(build_recorder)
        mock_git_repo.return_value.execute.assert_called_with(
            " ".join(
                [
                    "bash",
                    os.path.realpath(os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "build.sh")),
                    "-v 1.3.0",
                    "-p linux",
                    "-a x64",
                    "-d tar",
                    "-s false",
                    "-o builds",
                ]
            )
        )
        build_recorder.record_component.assert_called_with("OpenSearch", mock_git_repo.return_value)

    @patch("build_workflow.builder_from_source.GitRepository")
    def test_build_distribution_support(self, mock_git_repo: Mock) -> None:
        mock_git_repo.return_value = MagicMock(working_directory="dir")
        build_recorder = MagicMock()
        self.builder_distribution_support.checkout("dir")
        self.builder_distribution_support.build(build_recorder)
        mock_git_repo.return_value.execute.assert_called_with(
            " ".join(
                [
                    "bash",
                    os.path.realpath(os.path.join(ScriptFinder.component_scripts_path, "common-utils", "build.sh")),
                    "-v 1.3.0",
                    "-p linux",
                    "-a x64",
                    "-s false",
                    "-o builds",
                ]
            )
        )
        build_recorder.record_component.assert_called_with("common-utils", mock_git_repo.return_value)

    @patch("build_workflow.builder_from_source.GitRepository")
    def test_build_snapshot(self, mock_git_repo: Mock) -> None:
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

    @patch("build_workflow.builder_from_source.GitRepository")
    def test_build_snapshot_qualiier(self, mock_git_repo: Mock) -> None:
        self.builder.target.snapshot = True
        self.builder.target.qualifier = "alpha1"
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
                    "-q alpha1",
                    "-p linux",
                    "-a x64",
                    "-s true",
                    "-o builds",
                ]
            )
        )
        build_recorder.record_component.assert_called_with("common-utils", self.builder.git_repo)

    def mock_os_walk(self, artifact_path: str) -> List[Any]:
        if artifact_path.endswith(os.path.join("dir", "builds", "core-plugins")):
            return [["core-plugins", [], ["plugin1.zip"]]]
        if artifact_path.endswith(os.path.join("dir", "builds", "maven")):
            return [("maven", [], ["artifact1.jar"])]
        else:
            return []

    @patch("os.walk")
    @patch("build_workflow.builder_from_source.GitRepository")
    def test_export_artifacts(self, mock_git_repo: Mock, mock_walk: Mock) -> None:
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
