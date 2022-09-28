# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, call, patch

from ci_workflow.ci_check_manifest_component import CiCheckManifestComponent
from ci_workflow.ci_target import CiTarget
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputComponentFromDist


class TestCiCheckManifestComponent(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "opensearch-1.1.0-x64-build-manifest.yml")

    @patch("manifests.distribution.find_build_root")
    @patch("ci_workflow.ci_check_manifest_component.BuildManifest")
    def test_retrieves_manifests(self, mock_manifest: Mock, find_build_root: Mock) -> None:
        find_build_root.return_value = "url/linux/ARCH/builds/opensearch"
        check = CiCheckManifestComponent(
            InputComponentFromDist({"name": "common-utils", "dist": "url"}), CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=True)
        )

        mock_manifest.from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)

        check.check()
        mock_manifest.from_url.assert_has_calls(
            [
                call("url/linux/ARCH/builds/opensearch/manifest.yml"),
                call("url/linux/ARCH/builds/opensearch/manifest.yml"),
            ]
        )
        find_build_root.assert_has_calls(
            [
                call("url", "linux", "x64", "opensearch"),
                call("url", "linux", "arm64", "opensearch"),
            ]
        )

    @patch("manifests.distribution.find_build_root")
    @patch("ci_workflow.ci_check_manifest_component.BuildManifest")
    def test_missing_component(self, mock_manifest: Mock, find_build_root: Mock) -> None:
        find_build_root.return_value = "url/linux/x64/builds/opensearch"
        check = CiCheckManifestComponent(
            InputComponentFromDist({"name": "does-not-exist", "dist": "url"}), CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=True)
        )

        mock_manifest.from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)

        with self.assertRaises(CiCheckManifestComponent.MissingComponentError) as ctx:
            check.check()

        self.assertEqual(str(ctx.exception), "Missing does-not-exist in url/linux/x64/builds/opensearch/manifest.yml.")
        find_build_root.assert_called()
