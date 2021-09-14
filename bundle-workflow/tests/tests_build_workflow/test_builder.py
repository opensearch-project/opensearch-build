# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from build_workflow.build_target import BuildTarget
from build_workflow.builder import Builder
from paths.script_finder import ScriptFinder


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = Builder(
            "component",
            MagicMock(working_directory="/tmp/checked-out-component"),
            MagicMock(),
        )

    def test_builder(self):
        self.assertEqual(self.builder.component_name, "component")

    def test_build(self):
        self.builder.build(BuildTarget(version="1.0.0", arch="x64", snapshot=False))
        self.builder.git_repo.execute.assert_called_with(
            " ".join(
                [
                    os.path.realpath(
                        os.path.join(ScriptFinder.default_scripts_path, "build.sh")
                    ),
                    "-v 1.0.0",
                    "-a x64",
                    "-s false",
                    "-o artifacts",
                ]
            )
        )
        self.builder.build_recorder.record_component.assert_called_with(
            "component", self.builder.git_repo
        )

    def test_build_snapshot(self):
        self.builder.build(BuildTarget(version="1.0.0", arch="x64", snapshot=True))
        self.builder.git_repo.execute.assert_called_with(
            " ".join(
                [
                    os.path.realpath(
                        os.path.join(ScriptFinder.default_scripts_path, "build.sh")
                    ),
                    "-v 1.0.0",
                    "-a x64",
                    "-s true",
                    "-o artifacts",
                ]
            )
        )
        self.builder.build_recorder.record_component.assert_called_with(
            "component", self.builder.git_repo
        )

    def mock_os_walk(self, artifact_path):
        if artifact_path.endswith("/checked-out-component/artifacts/core-plugins"):
            return [["/core-plugins", [], ["plugin1.zip"]]]
        if artifact_path.endswith("/checked-out-component/artifacts/maven"):
            return [("/maven", [], ["artifact1.jar"])]
        else:
            return []

    @patch("os.walk")
    def test_export_artifacts(self, mock_walk):
        mock_walk.side_effect = self.mock_os_walk
        self.builder.export_artifacts()
        self.assertEqual(self.builder.build_recorder.record_artifact.call_count, 2)
        self.builder.build_recorder.record_artifact.assert_has_calls([
            call(
                "component",
                "maven",
                os.path.relpath("/maven/artifact1.jar", self.builder.artifacts_path),
                "/maven/artifact1.jar",
            ),
            call(
                "component",
                "core-plugins",
                os.path.relpath("/core-plugins/plugin1.zip", self.builder.artifacts_path),
                "/core-plugins/plugin1.zip",
            ),
        ])
