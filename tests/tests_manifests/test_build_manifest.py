# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from manifests.build_manifest import BuildComponent, BuildManifest


class TestBuildManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-build-1.1.0.yml")
        self.manifest = BuildManifest.from_path(self.manifest_filename)

    def test_build(self) -> None:
        self.assertEqual(self.manifest.version, "1.2")
        self.assertEqual(self.manifest.build.name, "OpenSearch")
        self.assertEqual(self.manifest.build.version, "1.1.0")
        self.assertEqual(len(self.manifest.components), 15)

    def test_component(self) -> None:
        opensearch_component = self.manifest.components["OpenSearch"]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.commit_id, "b7334f49d530ffd1a3f7bd0e5832b9b2a9caa583")
        self.assertEqual(opensearch_component.ref, "1.x")
        self.assertEqual(
            sorted(opensearch_component.artifacts.keys()),
            ["core-plugins", "dist", "maven"],
        )

    def test_to_dict(self) -> None:
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_components_index(self) -> None:
        component = self.manifest.components["index-management"]
        self.assertEqual(component.name, "index-management")

    def test_components_index_error(self) -> None:
        with self.assertRaises(KeyError) as ctx:
            self.manifest.components["invalid-component"]
        self.assertEqual(str(ctx.exception), "'invalid-component'")

    def test_versions(self) -> None:
        self.assertTrue(len(BuildManifest.VERSIONS))
        for version in BuildManifest.VERSIONS:
            manifest = BuildManifest.from_path(os.path.join(self.data_path, "build", f"opensearch-build-schema-version-{version}.yml"))
            self.assertEqual(version, manifest.version)
            self.assertIsNotNone(any(manifest.components))

    def test_select(self) -> None:
        path = os.path.join(self.data_path, "build", "opensearch-build-schema-version-1.2.yml")
        manifest = BuildManifest.from_path(path)
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)

    def test_select_none(self) -> None:
        path = os.path.join(self.data_path, "build", "opensearch-build-schema-version-1.2.yml")
        manifest = BuildManifest.from_path(path)
        with self.assertRaises(ValueError) as ctx:
            self.assertEqual(len(list(manifest.components.select(focus="x"))), 0)
        self.assertEqual(str(ctx.exception), "No components matched focus=x.")

    def test_component_matches(self) -> None:
        self.assertTrue(BuildComponent({"name": "x", "repository": "", "ref": "", "commit_id": "", "version": ""}).__matches__())

    def test_component_matches_focus(self) -> None:
        component = BuildComponent({"name": "x", "repository": "", "ref": "", "commit_id": "", "version": ""})
        self.assertTrue(component.__matches__(focus=None))
        self.assertTrue(component.__matches__(focus="x"))
        self.assertFalse(component.__matches__(focus="y"))
