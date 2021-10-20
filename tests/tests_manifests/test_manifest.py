# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from manifests.manifest import Manifest
from system.temporary_directory import TemporaryDirectory


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

    def test_invalid_version_empty(self):
        manifest_path = os.path.join(self.data_path, "invalid-schema-version-empty.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifest.from_path(manifest_path)
        self.assertEqual(
            "Invalid manifest schema: {'schema-version': ['empty values not allowed']}",
            context.exception.__str__(),
        )

    def test_invalid_version_no_value(self):
        manifest_path = os.path.join(self.data_path, "invalid-schema-version-no-value.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifest.from_path(manifest_path)
        self.assertEqual(
            "Invalid manifest schema: {'schema-version': ['null value not allowed']}",
            context.exception.__str__(),
        )

    def test_compact(self):
        self.assertEqual(Manifest.compact({}), {})
        self.assertEqual(Manifest.compact({"x": "y"}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": []}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": None}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": {"t": None}}), {"x": "y"})

    def test_to_file(self):
        manifest_path = os.path.join(self.data_path, "min.yml")
        manifest = TestManifest.SampleManifest.from_path(manifest_path)

        with TemporaryDirectory() as path:
            output_path = os.path.join(path.name, "manifest.yml")
            manifest.to_file(output_path)
            self.assertTrue(os.path.isfile(manifest_path))
            with open(output_path) as f:
                self.assertEqual(yaml.safe_load(f), manifest.to_dict())
