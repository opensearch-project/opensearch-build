# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import os
import unittest
from typing import Any

from manifests.build_manifest import BuildManifest
from manifests.manifests import Manifests


class TestManifests(unittest.TestCase):
    class WildcardManifests(Manifests):
        def __init__(self, klass: Any, wildcard: str = "*.yml") -> None:
            data_path = os.path.join(os.path.dirname(__file__), "data")
            manifest_filenames = os.path.join(data_path, wildcard)
            super().__init__(klass, glob.glob(manifest_filenames))

    def test_latest(self) -> None:
        manifests = TestManifests.WildcardManifests(BuildManifest, "opensearch-build-*.yml")
        latest_manifest: BuildManifest = manifests.latest
        self.assertEqual(latest_manifest.build.version, max(manifests.keys()))

    def test_latest_no_manifests(self) -> None:
        manifests = TestManifests.WildcardManifests(BuildManifest, "does-not-exist*.yml")
        with self.assertRaises(RuntimeError) as context:
            manifests.latest
        self.assertEqual("No manifests found", str(context.exception))

    def test_build_manifests(self) -> None:
        manifests = TestManifests.WildcardManifests(BuildManifest, "opensearch-build-*.yml")
        self.assertTrue(len(manifests) >= 2)

    def test_invalid_filename(self) -> None:
        with self.assertRaises(ValueError) as context:
            TestManifests.WildcardManifests(BuildManifest, "invalid-schema-version.yml")
        self.assertEqual("Invalid file: invalid-schema-version.yml", str(context.exception))

    def test_versions(self) -> None:
        manifests = TestManifests.WildcardManifests(BuildManifest, "opensearch-build-*.yml")
        versions = manifests.versions
        self.assertTrue("1.1.0" in versions)
        self.assertTrue("1.2.0" in versions)
