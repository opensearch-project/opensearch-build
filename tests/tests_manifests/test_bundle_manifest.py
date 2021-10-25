# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import patch

import yaml

from manifests.bundle_manifest import BundleManifest


class TestBundleManifest(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-bundle-1.1.0.yml")
        self.manifest = BundleManifest.from_path(self.manifest_filename)

    def test_build(self):
        self.assertEqual(self.manifest.version, "1.1")
        self.assertEqual(self.manifest.build.name, "OpenSearch")
        self.assertEqual(self.manifest.build.version, "1.1.0")
        self.assertEqual(self.manifest.build.location, "bundle/opensearch-1.1.0-linux-x64.tar.gz")
        self.assertEqual(self.manifest.build.platform, "linux")
        self.assertEqual(self.manifest.build.architecture, "x64")
        self.assertEqual(len(self.manifest.components), 13)

    def test_component(self):
        opensearch_min_component = self.manifest.components[0]
        self.assertEqual(opensearch_min_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_min_component.location,
            "artifacts/dist/opensearch-min-1.1.0-linux-x64.tar.gz",
        )
        self.assertEqual(
            opensearch_min_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(
            opensearch_min_component.commit_id,
            "b7334f49d530ffd1a3f7bd0e5832b9b2a9caa583",
        )
        self.assertEqual(opensearch_min_component.ref, "1.1")

    def test_to_dict(self):
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_get_manifest_relative_location(self):
        actual = BundleManifest.get_bundle_manifest_relative_location("25", "1.1.0", "linux", "x64")
        # TODO: use platform, https://github.com/opensearch-project/opensearch-build/issues/669
        expected = "bundles/1.1.0/25/x64/manifest.yml"
        self.assertEqual(actual, expected, "the manifest relative location is not as expected")

    def test_get_tarball_relative_location(self):
        actual = BundleManifest.get_tarball_relative_location("25", "1.1.0", "darwin", "x64")
        # TODO: use platform, https://github.com/opensearch-project/opensearch-build/issues/669
        expected = "bundles/1.1.0/25/x64/opensearch-1.1.0-darwin-x64.tar.gz"
        self.assertEqual(actual, expected, "the tarball relative location is not as expected")

    def test_get_tarball_name(self):
        actual = BundleManifest.get_tarball_name("1.1.0", "darwin", "x64")
        expected = "opensearch-1.1.0-darwin-x64.tar.gz"
        self.assertEqual(actual, expected, "the tarball name is not as expected")

    @patch("os.remove")
    @patch("builtins.open")
    @patch("manifests.bundle_manifest.BundleManifest.from_path")
    @patch("manifests.bundle_manifest.S3Bucket")
    def test_from_s3(self, mock_s3_bucket, *mocks):
        s3_bucket = mock_s3_bucket.return_value
        s3_download_path = BundleManifest.get_bundle_manifest_relative_location(
            self.manifest.build.id,
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture,
        )
        dest = os.path.realpath(os.path.join(tempfile.gettempdir(), "xyz"))
        BundleManifest.from_s3(
            "bucket_name",
            self.manifest.build.id,
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture,
            dest,
        )
        self.assertEqual(s3_bucket.download_file.call_count, 1)
        s3_bucket.download_file.assert_called_with(s3_download_path, dest)
        os.remove.assert_called_with(os.path.join(dest, "manifest.yml"))

    def test_versions(self):
        self.assertTrue(len(BundleManifest.VERSIONS))
        for version in BundleManifest.VERSIONS:
            manifest = BundleManifest.from_path(
                os.path.join(
                    self.data_path, "bundle", f"opensearch-bundle-schema-version-{version}.yml"
                )
            )
            self.assertEqual(version, manifest.version)
