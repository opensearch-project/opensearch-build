# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from build_workflow.build_artifact_check import BuildArtifactCheck
from build_workflow.build_target import BuildTarget
from build_workflow.opensearch_dashboards.build_artifact_check_plugin import BuildArtifactOpenSearchDashboardsCheckPlugin


class TestBuildArtifactOpenSearchDashboardsCheckPlugin(unittest.TestCase):
    @contextmanager
    def __mock(self, props={}, snapshot=True):
        with patch("build_workflow.opensearch_dashboards.build_artifact_check_plugin.ZipFile") as mock_zipfile:
            mock_zipfile.return_value.__enter__.return_value.read.return_value.decode.return_value = props
            yield BuildArtifactOpenSearchDashboardsCheckPlugin(
                BuildTarget(
                    build_id="1",
                    output_dir="output_dir",
                    name="OpenSearch",
                    version="1.1.0",
                    patches=["1.0.0"],
                    architecture="x64",
                    snapshot=snapshot,
                )
            )

    def test_check_plugin_invalid_zip_version_snapshot(self):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock() as mock:
                mock.check("invalid.zip")
        self.assertEqual(
            "Artifact invalid.zip is invalid. Expected filename to be in the format of pluginName-1.1.0.zip.",
            str(context.exception),
        )

    def test_check_plugin_invalid_zip_version(self):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock(snapshot=False) as mock:
                mock.check("invalid.zip")
        self.assertEqual(
            "Artifact invalid.zip is invalid. Expected filename to be in the format of pluginName-1.1.0.zip.",
            str(context.exception),
        )

    def test_check_plugin_missing_name(self):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock() as mock:
                mock.check("-1.1.0.zip")
        self.assertEqual(
            "Artifact -1.1.0.zip is invalid. Expected filename to be in the format of pluginName-1.1.0.zip.",
            str(context.exception),
        )

    def test_check_plugin_invalid_version_in_filename(self):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock(snapshot=False) as mock:
                mock.check("pluginName-1.2.3.zip")
        self.assertEqual(
            "Artifact pluginName-1.2.3.zip is invalid. Expected filename to to be one of ['pluginName-1.1.0.zip', 'pluginName-1.0.0.zip'].",
            str(context.exception),
        )

    def test_check_plugin_version_properties_missing(self, *mocks):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock(snapshot=False) as mock:
                mock.check("pluginName-1.1.0.zip")
        self.assertEqual(
            "Artifact pluginName-1.1.0.zip is invalid. Expected to have version=any of ['1.1.0.0', '1.0.0.0'], but none was found.",
            str(context.exception),
        )

    def test_check_plugin_version_properties_mismatch(self, *mocks):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock({"version": "1.2.3.4"}) as mock:
                mock.check("pluginName-1.1.0.zip")
            self.assertEqual(
                "Artifact valid-1.1.0.0.zip is invalid. Expected to have version='1.1.0.0', but was '1.2.3.4'.",
                str(context.exception),
            )

    def test_check_plugin_version_properties(self, *mocks):
        with self.__mock({"opensearchDashboardsVersion": "1.1.0", "version": "1.1.0.0"}, snapshot=False) as mock:
            mock.check("pluginName-1.1.0.zip")

    def test_check_plugin_version_properties_patches(self, *mocks):
        with self.__mock({"opensearchDashboardsVersion": "1.0.0", "version": "1.0.0.0"}, snapshot=False) as mock:
            mock.check("pluginName-1.0.0.zip")
