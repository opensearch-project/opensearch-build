# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from ci_workflow.ci_check_manifest_component import CiCheckManifestComponent
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputManifest


class TestCiCheckManifestComponent(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "opensearch-1.1.0-x64-build-manifest.yml")

    @patch("ci_workflow.ci_check_manifest_component.BuildManifest")
    def test_retrieves_manifests(self, mock_manifest):
        check = CiCheckManifestComponent(InputManifest.ComponentFromDist({
            "name": "common-utils",
            "dist": "url"
        }), MagicMock())

        mock_manifest.from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)

        check.check()
        mock_manifest.from_url.assert_has_calls([
            call("url/x64/manifest.yml"),
            call("url/arm64/manifest.yml")
        ])

    @patch("ci_workflow.ci_check_manifest_component.BuildManifest")
    def test_missing_component(self, mock_manifest):
        check = CiCheckManifestComponent(InputManifest.ComponentFromDist({
            "name": "does-not-exist",
            "dist": "url"
        }), MagicMock())

        mock_manifest.from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)

        with self.assertRaises(CiCheckManifestComponent.MissingComponentError) as ctx:
            check.check()

        self.assertEqual(str(ctx.exception), "Missing does-not-exist in url/x64/manifest.yml.")
