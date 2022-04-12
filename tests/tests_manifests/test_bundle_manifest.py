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
        self.manifest_filename = os.path.join(self.data_path, "opensearch-bundle-2.0.0.yml")
        self.manifest = BundleManifest.from_path(self.manifest_filename)

        self.manifest_distribution_filename = os.path.join(self.data_path, "opensearch-bundle-2.0.0.yml")
        self.manifest_distribution = BundleManifest.from_path(self.manifest_distribution_filename)

    def test_build(self) -> None:
        self.assertEqual(self.manifest.version, "2.0")
        self.assertEqual(self.manifest.build.name, "OpenSearch")
        self.assertEqual(self.manifest.build.version, "2.0.0-alpha1-SNAPSHOT")
        self.assertEqual(self.manifest.build.location, "tar/dist/opensearch/opensearch-2.0.0-alpha1-SNAPSHOT-linux-x64.tar.gz")
        self.assertEqual(self.manifest.build.platform, "linux")
        self.assertEqual(self.manifest.build.architecture, "x64")
        self.assertEqual(len(self.manifest.components), 16)

        self.assertEqual(self.manifest_distribution.build.version, "2.0.0-alpha1-SNAPSHOT")
        self.assertEqual(self.manifest_distribution.build.distribution, "tar")

    def test_component(self) -> None:
        opensearch_min_component = self.manifest.components["OpenSearch"]
        self.assertEqual(opensearch_min_component.name, "OpenSearch")
        self.assertEqual(opensearch_min_component.locations, ["tar/builds/opensearch/dist/opensearch-min-2.0.0-alpha1-SNAPSHOT-linux-x64.tar.gz"])
        self.assertEqual(opensearch_min_component.repository, "https://github.com/opensearch-project/OpenSearch.git")
        self.assertEqual(opensearch_min_component.commit_id, "a9a1c0dd01aff08e48e7a65c9dfe2a2de6683061")
        self.assertEqual(opensearch_min_component.ref, "2.0")

    def test_to_dict(self) -> None:
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_versions(self) -> None:
        self.assertTrue(len(BundleManifest.VERSIONS))
        for version in BundleManifest.VERSIONS:
            manifest = BundleManifest.from_path(os.path.join(self.data_path, "bundle", f"opensearch-bundle-schema-version-{version}.yml"))
            self.assertEqual(version, manifest.version)
