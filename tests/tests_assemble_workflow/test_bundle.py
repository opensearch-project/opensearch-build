# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from assemble_workflow.bundle import Bundle
from manifests.build_manifest import BuildManifest


class TestBundle(unittest.TestCase):
    class DummyBundle(Bundle):
        def install_plugin(self, plugin):
            pass

    @patch("assemble_workflow.dist.Dist.extract")
    def test_bundle_rpm(self, *mocks):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = self.DummyBundle(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "rpm")
        self.assertEqual(bundle.min_dist.name, "OpenSearch")
        self.assertEqual(len(bundle.plugins), 12)
        self.assertEqual(bundle.artifacts_dir, artifacts_path)
        self.assertIsNotNone(bundle.bundle_recorder)
        self.assertEqual(bundle.installed_plugins, [])
        self.assertTrue(bundle.min_dist.path.endswith("opensearch-min-1.1.0-linux-x64.tar.gz"))
        self.assertEqual(bundle.distribution, "rpm")

    @patch("assemble_workflow.dist.Dist.extract")
    def test_bundle_tar(self, *mocks):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = self.DummyBundle(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "tar")
        self.assertEqual(bundle.min_dist.name, "OpenSearch")
        self.assertEqual(len(bundle.plugins), 12)
        self.assertEqual(bundle.artifacts_dir, artifacts_path)
        self.assertIsNotNone(bundle.bundle_recorder)
        self.assertEqual(bundle.installed_plugins, [])
        self.assertTrue(bundle.min_dist.path.endswith("opensearch-min-1.1.0-linux-x64.tar.gz"))
        self.assertEqual(bundle.distribution, "tar")

    @patch("assemble_workflow.dist.Dist.extract")
    def test_bundle_zip(self, *mocks):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = self.DummyBundle(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock(), "zip")
        self.assertEqual(bundle.min_dist.name, "OpenSearch")
        self.assertEqual(len(bundle.plugins), 12)
        self.assertEqual(bundle.artifacts_dir, artifacts_path)
        self.assertIsNotNone(bundle.bundle_recorder)
        self.assertEqual(bundle.installed_plugins, [])
        self.assertTrue(bundle.min_dist.path.endswith("opensearch-min-1.1.0-linux-x64.tar.gz"))
        self.assertEqual(bundle.distribution, "zip")

    def test_bundle_does_not_exist_raises_error(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-linux-1.1.0.yml")
        with self.assertRaises(FileNotFoundError) as ctx:
            self.DummyBundle(
                BuildManifest.from_path(manifest_path),
                os.path.join(os.path.dirname(__file__), "data", "does-not-exist"),
                MagicMock(),
                "distribution"
            )
        self.assertTrue("opensearch-min-1.1.0-linux-x64.tar.gz" in str(ctx.exception))
