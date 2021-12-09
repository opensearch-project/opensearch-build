# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from manifests.bundle_manifest import BundleManifest


class TestBundleManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-bundle-1.1.0.yml")
        self.manifest = BundleManifest.from_path(self.manifest_filename)

    def test_build(self) -> None:
        self.assertEqual(self.manifest.version, "1.1")
        self.assertEqual(self.manifest.build.name, "OpenSearch")
        self.assertEqual(self.manifest.build.version, "1.1.0")
        self.assertEqual(self.manifest.build.location, "bundle/opensearch-1.1.0-linux-x64.tar.gz")
        self.assertEqual(self.manifest.build.platform, "linux")
        self.assertEqual(self.manifest.build.architecture, "x64")
        self.assertEqual(len(self.manifest.components), 13)

    def test_component(self) -> None:
        opensearch_min_component = self.manifest.components["OpenSearch"]
        self.assertEqual(opensearch_min_component.name, "OpenSearch")
        self.assertEqual(opensearch_min_component.location, "artifacts/dist/opensearch-min-1.1.0-linux-x64.tar.gz")
        self.assertEqual(opensearch_min_component.repository, "https://github.com/opensearch-project/OpenSearch.git")
        self.assertEqual(opensearch_min_component.commit_id, "b7334f49d530ffd1a3f7bd0e5832b9b2a9caa583")
        self.assertEqual(opensearch_min_component.ref, "1.1")

    def test_to_dict(self) -> None:
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_versions(self) -> None:
        self.assertTrue(len(BundleManifest.VERSIONS))
        for version in BundleManifest.VERSIONS:
            manifest = BundleManifest.from_path(os.path.join(self.data_path, "bundle", f"opensearch-bundle-schema-version-{version}.yml"))
            self.assertEqual(version, manifest.version)
