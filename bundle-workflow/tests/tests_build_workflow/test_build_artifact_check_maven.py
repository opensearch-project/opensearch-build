# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from build_workflow.build_artifact_check import BuildArtifactCheck
from build_workflow.build_artifact_check_maven import BuildArtifactCheckMaven
from build_workflow.build_target import BuildTarget


class TestBuildArtifactCheckMaven(unittest.TestCase):
    @contextmanager
    def __mock(self, props="", snapshot=True):
        with patch("build_workflow.build_artifact_check_maven.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = (
                props
            )
            yield BuildArtifactCheckMaven(
                BuildTarget(
                    build_id="1",
                    output_dir="output_dir",
                    name="OpenSearch",
                    version="1.1.0",
                    arch="x64",
                    snapshot=snapshot,
                )
            )

    def test_build_artifact_check_maven_version_properties_none(self):
        with self.__mock("") as mock:
            mock.check("valid.jar")

    def test_record_maven_artifact_after_checking_maven_version_properties(self):
        with self.__mock("Implementation-Version: 1.1.0.0", snapshot=False) as mock:
            mock.check("valid.jar")

    def test_record_maven_artifact_after_checking_maven_version_properties_snapshot(
        self
    ):
        with self.__mock("Implementation-Version: 1.1.0.0-SNAPSHOT") as mock:
            mock.check("valid.jar")

    def test_build_artifact_check_maven_version_properties_mismatch(self):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock("Implementation-Version: 1.2.3.4", snapshot=False) as mock:
                mock.check("valid.jar")

        self.assertEqual(
            "Artifact valid.jar is invalid. Expected to have Implementation-Version=any of ['1.1.0.0', '1.1.0', None], but was '1.2.3.4'.",
            str(context.exception),
        )
