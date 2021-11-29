# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import copy
import os
import unittest
from unittest.mock import patch

import yaml

from manifests.input_manifest import InputManifest


class TestInputManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.manifests_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))

    def test_1_0(self):
        path = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.version, "1.0.0")
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        opensearch_component = manifest.components["OpenSearch"]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "1.0")
        for component in manifest.components.values():
            self.assertIsInstance(component.ref, str)

    def test_1_1(self):
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.version, "1.1.0")
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        # opensearch component
        opensearch_component = manifest.components["OpenSearch"]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "tags/1.1.0")
        # components
        for component in manifest.components.values():
            self.assertIsInstance(component.ref, str)
        # alerting component checks
        alerting_component = manifest.components["alerting"]
        self.assertIsNotNone(alerting_component)
        self.assertEqual(len(alerting_component.checks), 2)
        for check in alerting_component.checks:
            self.assertIsInstance(check, InputManifest.Check)
        self.assertIsNone(alerting_component.checks[0].args)
        self.assertEqual(alerting_component.checks[1].args, "alerting")

    def test_1_2(self):
        path = os.path.join(self.manifests_path, "1.2.0/opensearch-1.2.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.version, "1.2.0")
        self.assertEqual(manifest.ci.image.name, "opensearchstaging/ci-runner:centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211028")
        self.assertEqual(manifest.ci.image.args, "-e JAVA_HOME=/usr/lib/jvm/adoptopenjdk-14-hotspot")
        self.assertNotEqual(len(manifest.components), 0)
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        # opensearch component
        opensearch_component = manifest.components["OpenSearch"]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "tags/1.2.0")
        # components
        for component in manifest.components.values():
            self.assertIsInstance(component.ref, str)
        # alerting component checks
        alerting_component = manifest.components["alerting"]
        self.assertIsNotNone(alerting_component)
        self.assertEqual(len(alerting_component.checks), 2)
        for check in alerting_component.checks:
            self.assertIsInstance(check, InputManifest.Check)
        self.assertIsNone(alerting_component.checks[0].args)
        self.assertEqual(alerting_component.checks[1].args, "alerting")

    def test_to_dict(self):
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        data = manifest.to_dict()
        with open(path) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_invalid_ref(self):
        data_path = os.path.join(os.path.dirname(__file__), "data")
        manifest_path = os.path.join(data_path, "invalid-ref.yml")

        with self.assertRaises(Exception) as context:
            InputManifest.from_path(manifest_path)
        self.assertTrue(str(context.exception).startswith("Invalid manifest schema: {'components': "))

    def test_select(self):
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        self.assertNotEqual(len(list(manifest.components.select(platform="windows"))), 0)
        self.assertEqual(len(list(manifest.components.select(focus="k-NN", platform="linux"))), 1)

    def test_select_none(self):
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        with self.assertRaises(ValueError) as ctx:
            self.assertEqual(len(list(manifest.components.select(focus="k-NN", platform="windows"))), 0)
        self.assertEqual(str(ctx.exception), "No components matched focus=k-NN, platform=windows.")

    def test_component___matches__(self):
        self.assertTrue(InputManifest.Component({"name": "x", "repository": "", "ref": ""}).__matches__())

    def test_component___matches_platform__(self):
        data = {"name": "x", "repository": "", "ref": ""}
        self.assertTrue(InputManifest.Component(data).__matches__(platform=None))
        self.assertTrue(InputManifest.Component(data).__matches__(platform="x"))
        self.assertTrue(InputManifest.Component({**data, "platforms": ["linux"]}).__matches__(platform="linux"))
        self.assertTrue(InputManifest.Component({**data, "platforms": ["linux", "windows"]}).__matches__(platform="linux"))
        self.assertFalse(InputManifest.Component({**data, "platforms": ["linux"]}).__matches__(platform="x"))

    def test_component___matches_focus__(self):
        component = InputManifest.Component({"name": "x", "repository": "", "ref": ""})
        self.assertTrue(component.__matches__(focus=None))
        self.assertTrue(component.__matches__(focus="x"))
        self.assertFalse(component.__matches__(focus="y"))

    @patch("subprocess.check_output")
    def test_stable(self, mock_output):
        mock_output.return_value.decode.return_value = "updated\tHEAD"
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path).stable()
        opensearch = manifest.components["OpenSearch"]
        self.assertEqual(opensearch.ref, "updated")

    @patch("subprocess.check_output")
    def test_stable_override_build(self, mock_output):
        mock_output.return_value.decode.return_value = "updated\tHEAD"
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path).stable(platform="windows", architecture="arm64", snapshot=True)
        self.assertEqual(manifest.build.platform, "windows")
        self.assertEqual(manifest.build.architecture, "arm64")
        self.assertTrue(manifest.build.snapshot)

    def test_eq(self):
        path = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        manifest1 = InputManifest.from_path(path)
        manifest2 = InputManifest.from_path(path)
        self.assertEqual(manifest1, manifest1)
        self.assertEqual(manifest1, manifest2)

    def test_neq(self):
        path1 = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        path2 = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest1 = InputManifest.from_path(path1)
        manifest2 = InputManifest.from_path(path2)
        self.assertNotEqual(manifest1, manifest2)

    def test_neq_update(self):
        path = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        manifest1 = InputManifest.from_path(path)
        manifest2 = copy.deepcopy(manifest1)
        self.assertEqual(manifest1, manifest2)
        manifest2.components["name"] = InputManifest.ComponentFromDist({
            "name": "name",
            "dist": "dist"
        })
        self.assertNotEqual(manifest1, manifest2)
