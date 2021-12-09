# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import call, patch

from ci_workflow.ci_check_manifest_component import CiCheckManifestComponent
from ci_workflow.ci_target import CiTarget
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputComponentFromDist


class TestCiCheckManifestComponent(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "opensearch-1.1.0-x64-build-manifest.yml")

    @patch("ci_workflow.ci_check_manifest_component.BuildManifest")
    def test_retrieves_manifests(self, mock_manifest):
        check = CiCheckManifestComponent(InputComponentFromDist({
            "name": "common-utils",
            "dist": "url"
        }), CiTarget(version="1.1.0", name="opensearch", snapshot=True))

        mock_manifest.from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)

        check.check()
        mock_manifest.from_url.assert_has_calls([
            call("url/linux/x64/builds/opensearch/manifest.yml"),
            call("url/linux/arm64/builds/opensearch/manifest.yml"),
        ])

    @patch("ci_workflow.ci_check_manifest_component.BuildManifest")
    def test_missing_component(self, mock_manifest):
        check = CiCheckManifestComponent(InputComponentFromDist({
            "name": "does-not-exist",
            "dist": "url"
        }), CiTarget(version="1.1.0", name="opensearch", snapshot=True))

        mock_manifest.from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)

        with self.assertRaises(CiCheckManifestComponent.MissingComponentError) as ctx:
            check.check()

        self.assertEqual(str(ctx.exception), "Missing does-not-exist in url/linux/x64/builds/opensearch/manifest.yml.")
