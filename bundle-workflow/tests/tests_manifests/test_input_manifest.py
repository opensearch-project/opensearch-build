# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from manifests.input_manifest import InputManifest


class TestInputManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.manifests_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../../../manifests")
        )

    def test_1_0(self):
        path = os.path.join(self.manifests_path, "opensearch-1.0.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.version, "1.0.0")
        self.assertEqual(len(manifest.components), 12)
        opensearch_component = manifest.components[0]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "1.0")
        for component in manifest.components:
            self.assertIsInstance(component.ref, str)

    def test_1_1(self):
        path = os.path.join(self.manifests_path, "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.version, "1.1.0")
        self.assertEqual(len(manifest.components), 14)
        opensearch_component = manifest.components[0]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "1.1")
        for component in manifest.components:
            self.assertIsInstance(component.ref, str)

    def test_to_dict(self):
        path = os.path.join(self.manifests_path, "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        data = manifest.to_dict()
        with open(path) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_invalid_ref(self):
        data_path = os.path.join(os.path.dirname(__file__), "data")
        manifest_path = os.path.join(data_path, "invalid-ref.yml")

        with self.assertRaises(TypeError) as context:
            InputManifest.from_path(manifest_path)
        self.assertEqual(
            "type of ref must be str; got float instead", str(context.exception)
        )
