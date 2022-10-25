# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import yaml

from manifests.build_manifest import BuildComponent, BuildManifest


class TestBuildManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-build-1.1.0.yml")
        self.manifest = BuildManifest.from_path(self.manifest_filename)

        self.manifest_filename_distribution = os.path.join(self.data_path, "opensearch-build-1.3.0.yml")
        self.manifest_distribution = BuildManifest.from_path(self.manifest_filename_distribution)

    def test_build(self) -> None:
        self.assertEqual(self.manifest.version, "1.2")
        self.assertEqual(self.manifest.build.name, "OpenSearch")
        self.assertEqual(self.manifest.build.filename, "opensearch")
        self.assertEqual(self.manifest.build.version, "1.1.0")
        self.assertEqual(len(self.manifest.components), 15)

        self.assertEqual(self.manifest_distribution.build.version, "1.3.0")
        self.assertEqual(self.manifest_distribution.build.distribution, "tar")

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

    @patch("manifests.manifest.urllib.request.urlopen")
    def test_legacy_from_url(self, urlopen: Mock) -> None:
        # Fake the dashboard file to look like its coming from the url, but its really in the data directory
        cm = MagicMock()
        self.manifest_filename = os.path.join(self.data_path, "opensearch-dashboards-build-1.1.0.yml")
        cm.read.return_value.decode.return_value = open(self.manifest_filename, 'r').read()
        cm.__enter__.return_value = cm
        urlopen.return_value = cm

        self.manifest = BuildManifest.from_url('http://fakeurl')
        self.assertEqual(self.manifest.version, "1.1")
        self.assertEqual(self.manifest.build.name, "OpenSearch Dashboards")
        self.assertEqual(self.manifest.build.filename, "opensearch-dashboards")
        self.assertEqual(self.manifest.build.version, "1.1.0")
        self.assertEqual(len(self.manifest.components), 10)

        component = self.manifest.components['OpenSearch-Dashboards']
        self.assertEqual(component.commit_id, "44d2cb5b4f9a7c641c1fef32ec569bc48ec46979")
        self.assertEqual(component.name, 'OpenSearch-Dashboards')
        self.assertEqual(component.ref, "1.1")
        self.assertEqual(component.repository, 'https://github.com/opensearch-project/OpenSearch-Dashboards.git')
        self.assertEqual(component.artifacts['dist'], ['dist/opensearch-dashboards-min-1.1.0-linux-x64.tar.gz'])

        urlopen.assert_called_once_with('http://fakeurl')

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
        self.assertEqual(len(list(manifest.components.select(focus=["common-utils"]))), 1)
        self.assertEqual(len(list(manifest.components.select(focus=["common-utils", "job-scheduler"]))), 2)

    def test_select_one_is_unknown(self) -> None:
        path = os.path.join(self.data_path, "build", "opensearch-build-schema-version-1.2.yml")
        manifest = BuildManifest.from_path(path)
        with self.assertRaises(ValueError) as ctx:
            self.assertEqual(len(list(manifest.components.select(focus=["common-utils", "x"]))), 0)
        self.assertEqual(str(ctx.exception), "Unknown component=x.")

    def test_select_two_are_unknown(self) -> None:
        path = os.path.join(self.data_path, "build", "opensearch-build-schema-version-1.2.yml")
        manifest = BuildManifest.from_path(path)
        with self.assertRaises(ValueError) as ctx:
            self.assertEqual(len(list(manifest.components.select(focus=["x", "y"]))), 0)
        self.assertEqual(str(ctx.exception), "Unknown components=x,y.")

    def test_component_matches(self) -> None:
        self.assertTrue(BuildComponent({"name": "x", "repository": "", "ref": "", "commit_id": "", "version": ""}).__matches__())

    def test_component_matches_focus(self) -> None:
        component = BuildComponent({"name": "x", "repository": "", "ref": "", "commit_id": "", "version": ""})
        self.assertTrue(component.__matches__(focus=None))
        self.assertTrue(component.__matches__(focus=[]))
        self.assertTrue(component.__matches__(focus=["x"]))
        self.assertTrue(component.__matches__(focus=["x", "y"]))
        self.assertFalse(component.__matches__(focus=["y"]))
