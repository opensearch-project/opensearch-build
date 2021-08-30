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
    def setUp(self):
        self.data_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "data")
        )
        self.manifest_filename = os.path.join(
            self.data_path, "opensearch-bundle-1.1.0.yml"
        )
        self.manifest = BundleManifest.from_path(self.manifest_filename)

    def test_build(self):
        self.assertEqual(self.manifest.version, "1.0")
        self.assertEqual(self.manifest.build.name, "OpenSearch")
        self.assertEqual(self.manifest.build.version, "1.1.0")
        self.assertEqual(
            self.manifest.build.location, "bundle/opensearch-1.1.0-linux-x64.tar.gz"
        )
        self.assertEqual(self.manifest.build.architecture, "x64")
        self.assertEqual(len(self.manifest.components), 13)

    def test_component(self):
        opensearch_min_component = self.manifest.components[0]
        self.assertEqual(opensearch_min_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_min_component.location,
            "artifacts/bundle/opensearch-min-1.1.0-linux-x64.tar.gz",
        )
        self.assertEqual(
            opensearch_min_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(
            opensearch_min_component.commit_id,
            "07a57d9bbb3922079b7bb1be83a01252f57f81ec",
        )
        self.assertEqual(opensearch_min_component.ref, "1.x")

    def test_to_dict(self):
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)
