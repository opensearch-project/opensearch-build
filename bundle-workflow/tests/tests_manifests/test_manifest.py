# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest

import yaml

from manifests.manifest import Manifest


class TestManifest(unittest.TestCase):
    class SampleManifest(Manifest):
        def __init__(self, data):
            super().__init__(data)
            self.data = data

        def __to_dict__(self):
            return self.data

    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "data")

    def test_manifest_is_abstract(self):
        with self.assertRaises(TypeError) as context:
            Manifest(None)
        self.assertEqual(
            "Can't instantiate abstract class Manifest with abstract methods __init__",
            context.exception.__str__(),
        )

    def test_invalid_version(self):
        manifest_path = os.path.join(self.data_path, "invalid-schema-version.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifest.from_path(manifest_path)
        self.assertEqual(
            "Unsupported schema version: invalid", context.exception.__str__()
        )

    def test_compact(self):
        self.assertEqual(Manifest.compact({}), {})
        self.assertEqual(Manifest.compact({"x": "y"}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": []}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": None}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": {"t": None}}), {"x": "y"})

    def test_to_file(self):
        manifest_path = os.path.join(self.data_path, "opensearch-build-1.1.0.yml")
        manifest = TestManifest.SampleManifest.from_path(manifest_path)

        with tempfile.TemporaryDirectory() as path:
            output_path = os.path.join(path, "manifest.yml")
            manifest.to_file(output_path)
            self.assertTrue(os.path.isfile(manifest_path))
            with open(output_path) as f:
                self.assertEqual(yaml.safe_load(f), manifest.to_dict())
