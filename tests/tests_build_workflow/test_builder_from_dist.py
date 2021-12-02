# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from build_workflow.build_target import BuildTarget
from build_workflow.builder_from_dist import BuilderFromDist
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputComponentFromDist


class TestBuilderFromDist(unittest.TestCase):
    def setUp(self):
        self.builder = BuilderFromDist(
            InputComponentFromDist({"name": "common-utils", "dist": "url"}),
            BuildTarget(
                name="OpenSearch",
                version="1.1.0",
                platform="windows",
                architecture="x64",
                snapshot=False,
            ),
        )

    def test_builder(self):
        self.assertEqual(self.builder.component.name, "common-utils")

    @patch("build_workflow.builder_from_dist.BuildManifest")
    def test_checkout(self, mock_manifest):
        self.builder.checkout("dir")
        mock_manifest.from_url.assert_called_with("url/windows/x64/builds/opensearch/manifest.yml")

    def test_build(self):
        build_recorder = MagicMock()
        self.builder.build(build_recorder)

    @patch("os.makedirs")
    @patch("urllib.request.urlretrieve")
    @patch("build_workflow.builder_from_dist.BuilderFromDist.ManifestGitRepository")
    def test_export_artifacts(self, mock_manifest_git_repository, mock_urllib, mock_makedirs, *mocks):
        build_recorder = MagicMock()
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-windows-1.1.0.yml")
        self.builder.build_manifest = BuildManifest.from_path(manifest_path)
        self.builder.export_artifacts(build_recorder)
        build_recorder.record_component.assert_called_with("common-utils", mock_manifest_git_repository.return_value)
        mock_makedirs.assert_called_with(
            os.path.realpath(os.path.join("builds", "maven", "org", "opensearch", "common-utils", "1.1.0.0")),
            exist_ok=True
        )
        mock_urllib.assert_called_with(
            "url/windows/x64/builds/opensearch/maven/org/opensearch/common-utils/1.1.0.0/common-utils-1.1.0.0.jar",
            os.path.realpath(os.path.join("builds", "maven", "org", "opensearch", "common-utils", "1.1.0.0", "common-utils-1.1.0.0.jar")),
        )
