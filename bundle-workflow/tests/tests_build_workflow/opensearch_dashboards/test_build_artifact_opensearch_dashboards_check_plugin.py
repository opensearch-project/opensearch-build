# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from contextlib import contextmanager

from build_workflow.build_artifact_check import BuildArtifactCheck
from build_workflow.build_target import BuildTarget
from build_workflow.opensearch_dashboards.build_artifact_check_plugin import \
    BuildArtifactOpenSearchDashboardsCheckPlugin


class TestBuildArtifactOpenSearchDashboardsCheckPlugin(unittest.TestCase):
    @contextmanager
    def __mock(self, snapshot=True):
        yield BuildArtifactOpenSearchDashboardsCheckPlugin(
            BuildTarget(
                build_id="1",
                output_dir="output_dir",
                name="OpenSearch",
                version="1.1.0",
                arch="x64",
                snapshot=snapshot,
            )
        )

    def test_check_plugin_invalid_zip_version(self):
        with self.assertRaises(BuildArtifactCheck.BuildArtifactInvalidError) as context:
            with self.__mock() as mock:
                mock.check("invalid.zip")
        self.assertEqual(
            "Artifact invalid.zip is invalid. Expected filename to include 1.1.0.",
            str(context.exception),
        )

    def test_check_plugin_zip(self, *mocks):
        with self.__mock(snapshot=False) as mock:
            mock.check("valid-1.1.0.zip")

    def test_check_plugin_snapshot_zip(self, *mocks):
        with self.__mock(snapshot=True) as mock:
            mock.check("valid-1.1.0.zip")
