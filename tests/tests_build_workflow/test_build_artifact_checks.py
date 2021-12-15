# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from build_workflow.build_artifact_checks import BuildArtifactChecks
from build_workflow.build_target import BuildTarget
from build_workflow.opensearch.build_artifact_check_maven import BuildArtifactOpenSearchCheckMaven
from build_workflow.opensearch.build_artifact_check_plugin import BuildArtifactOpenSearchCheckPlugin
from build_workflow.opensearch_dashboards.build_artifact_check_plugin import BuildArtifactOpenSearchDashboardsCheckPlugin


class TestBuildArtifactChecks(unittest.TestCase):
    def __mock_target(self, name: str = "OpenSearch") -> BuildTarget:
        return BuildTarget(
            build_id="1",
            output_dir="output_dir",
            name=name,
            version="1.1.0",
            architecture="x64",
            snapshot=True,
        )

    def test_opensearch_build_artifact_check_plugin(self) -> None:
        target = self.__mock_target(name="OpenSearch")
        check = BuildArtifactChecks.create(target, "plugins")
        self.assertIs(type(check), BuildArtifactOpenSearchCheckPlugin)

    def test_opensearch_build_artifact_check_maven(self) -> None:
        target = self.__mock_target(name="OpenSearch")
        check = BuildArtifactChecks.create(target, "maven")
        self.assertIs(type(check), BuildArtifactOpenSearchCheckMaven)

    def test_opensearch_build_artifact_check_other(self) -> None:
        target = self.__mock_target(name="OpenSearch")
        self.assertIsNone(BuildArtifactChecks.create(target, "other"))

    def test_opensearch_dashboards_build_artifact_check_plugin(self) -> None:
        target = self.__mock_target(name="OpenSearch Dashboards")
        check = BuildArtifactChecks.create(target, "plugins")
        self.assertIs(type(check), BuildArtifactOpenSearchDashboardsCheckPlugin)

    def test_build_artifact_check_invalid(self) -> None:
        target = self.__mock_target(name="invalid")
        with self.assertRaises(ValueError) as ctx:
            BuildArtifactChecks.create(target, "plugins")
        self.assertEqual(str(ctx.exception), "Unsupported bundle: invalid")

    @patch.object(BuildArtifactOpenSearchCheckPlugin, "check")
    def test_check(self, mock_check: Mock) -> None:
        target = self.__mock_target(name="OpenSearch")
        BuildArtifactChecks.check(target, "plugins", "artifact.zip")
        mock_check.assert_called_with("artifact.zip")
