# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import yaml

from manifests.manifest import Manifest
from system.temporary_directory import TemporaryDirectory


class TestManifest(unittest.TestCase):
    class SampleManifest(Manifest['TestManifest.SampleManifest']):
        def __init__(self, data: Dict[Any, Any]) -> None:
            super().__init__(data)
            self.data = data

        def __to_dict__(self) -> dict:
            return self.data

    class SampleManifestWithVersions(Manifest['TestManifest.SampleManifest']):
        def __init__(self, data: Dict[Any, Any]) -> None:
            super().__init__(data)
            self.data = data

        def __to_dict__(self) -> dict:
            return self.data

    SampleManifestWithVersions.VERSIONS = {
        "3.14": SampleManifestWithVersions,
        "6.42": SampleManifestWithVersions
    }

    def setUp(self) -> None:
        self.data_path = os.path.join(os.path.dirname(__file__), "data")

    def test_manifest_is_abstract(self) -> None:
        with self.assertRaises(TypeError) as context:
            Manifest(None)  # type: ignore[abstract]
        self.assertEqual(
            "Can't instantiate abstract class Manifest with abstract methods __init__",
            context.exception.__str__(),
        )

    def test_invalid_version_empty(self) -> None:
        manifest_path = os.path.join(self.data_path, "invalid-schema-version-empty.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifest.from_path(manifest_path)
        self.assertEqual(
            "Invalid manifest schema: {'schema-version': ['empty values not allowed']}",
            context.exception.__str__(),
        )

    def test_invalid_version_no_value(self) -> None:
        manifest_path = os.path.join(self.data_path, "invalid-schema-version-no-value.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifest.from_path(manifest_path)
        self.assertEqual(
            "Invalid manifest schema: {'schema-version': ['null value not allowed']}",
            context.exception.__str__(),
        )

    def test_compact(self) -> None:
        self.assertEqual(Manifest.compact({}), {})
        self.assertEqual(Manifest.compact({"x": "y"}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": []}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": None}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": "y", "z": {"t": None}}), {"x": "y"})
        self.assertEqual(Manifest.compact({"x": True}), {"x": True})
        self.assertEqual(Manifest.compact({"x": False}), {"x": False})

    def test_to_file(self) -> None:
        manifest_path = os.path.join(self.data_path, "min.yml")
        manifest = TestManifest.SampleManifest.from_path(manifest_path)

        with TemporaryDirectory() as path:
            output_path = os.path.join(path.name, "manifest.yml")
            manifest.to_file(output_path)
            self.assertTrue(os.path.isfile(manifest_path))
            with open(output_path) as f:
                self.assertEqual(yaml.safe_load(f), manifest.to_dict())

    def test_invalid_version_no_value_3_14(self) -> None:
        manifest_path = os.path.join(self.data_path, "invalid-schema-version-no-value.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifestWithVersions.from_path(manifest_path)
        self.assertEqual(
            "Missing manifest version, must be one of 3.14, 6.42",
            context.exception.__str__(),
        )

    def test_invalid_version_empty_3_14(self) -> None:
        manifest_path = os.path.join(self.data_path, "invalid-schema-version-empty.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifestWithVersions.from_path(manifest_path)
        self.assertEqual(
            "Missing manifest version, must be one of 3.14, 6.42",
            context.exception.__str__(),
        )

    def test_invalid_version_3_14(self) -> None:
        manifest_path = os.path.join(self.data_path, "opensearch-build-1.1.0.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.SampleManifestWithVersions.from_path(manifest_path)
        self.assertEqual(
            "Invalid manifest version: 1.2, must be one of 3.14, 6.42",
            context.exception.__str__(),
        )

    @patch("manifests.manifest.urllib.request.urlopen")
    def test_from_url(self, mock_urlopen: Mock) -> None:
        cm = MagicMock()
        cm.read.return_value.decode.return_value = '{"schema-version":"3.14"}'
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
        manifest = TestManifest.SampleManifest.from_url("url")
        self.assertEqual(manifest.version, "3.14")
        mock_urlopen.assert_called_with("url")

    def test_eq(self) -> None:
        manifest_path = os.path.join(self.data_path, "min.yml")
        manifest1 = TestManifest.SampleManifest.from_path(manifest_path)
        manifest2 = TestManifest.SampleManifest.from_path(manifest_path)
        self.assertEqual(manifest1, manifest1)
        self.assertEqual(manifest1, manifest2)
