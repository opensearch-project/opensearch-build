# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
import zipfile
from unittest.mock import MagicMock

from assemble_workflow.bundle_opensearch import BundleOpenSearch
from assemble_workflow.bundle_opensearch_dashboards import BundleOpenSearchDashboards
from assemble_workflow.bundles import Bundles
from manifests.build_manifest import BuildManifest


class TestBundles(unittest.TestCase):
    def test_bundle_opensearch(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = Bundles.create(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "tar", False)
        self.assertIs(type(bundle), BundleOpenSearch)

    def test_bundle_opensearch_dashboards(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-dashboards-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = Bundles.create(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "tar", False)
        self.assertIs(type(bundle), BundleOpenSearchDashboards)
        self.assertFalse(bundle.tmp_dir.keep)

    def test_bundle_keep(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = Bundles.create(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "tar", True)
        self.assertTrue(bundle.tmp_dir.keep)

    def test_bundle_distribution_tar(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = Bundles.create(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "tar", False)
        self.assertEqual(bundle.distribution, "tar")

    def test_bundle_distribution_zip(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        with self.assertRaises(zipfile.BadZipFile) as bad_zip_file_error:
            Bundles.create(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "zip", False)
        self.assertEqual(str(bad_zip_file_error.exception), "File is not a zip file")

    def test_bundle_distribution_rpm(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = Bundles.create(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "rpm", False)
        self.assertEqual(bundle.distribution, "rpm")

    def test_bundle_opensearch_invalid(self) -> None:
        manifest = BuildManifest(
            {
                "schema-version": "1.2",
                "build": {
                    "name": "invalid",
                    "platform": "linux",
                    "architecture": "x86",
                    "id": "id",
                    "version": "1.0.0",
                },
            }
        )
        with self.assertRaises(ValueError) as ctx:
            Bundles.create(manifest, "path", MagicMock(), "distribution", False)
        self.assertEqual(str(ctx.exception), "Unsupported bundle: invalid")
