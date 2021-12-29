# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import copy
import os
import unittest
from unittest.mock import Mock, patch

import yaml

from manifests.input_manifest import Check, InputComponent, InputComponentFromDist, InputComponentFromSource, InputManifest


class TestInputManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.manifests_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))

    def test_1_1_1_dist(self) -> None:
        data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        path = os.path.join(data_path, "opensearch-dashboards-from-dist-1.1.1.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch Dashboards")
        self.assertEqual(manifest.build.filename, "opensearch-dashboards")
        self.assertEqual(manifest.build.version, "1.1.1")
        self.assertEqual(len(list(manifest.components.select(focus="alertingDashboards"))), 1)
        opensearch_component: InputComponentFromDist = manifest.components["OpenSearch-Dashboards"]  # type: ignore[assignment]
        self.assertIsInstance(opensearch_component, InputComponentFromDist)
        self.assertEqual(opensearch_component.name, "OpenSearch-Dashboards")
        self.assertEqual(
            opensearch_component.dist,
            "https://ci.opensearch.org/ci/dbc/bundle-build-dashboards/1.1.0/20210930",
        )
        for component in manifest.components.values():
            if component.name in ['reportsDashboards', 'functionalTestDashboards']:
                self.assertIsInstance(component, InputComponentFromSource)
            else:
                self.assertIsInstance(component, InputComponentFromDist)

    def test_1_0(self) -> None:
        path = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.filename, "opensearch")
        self.assertEqual(manifest.build.version, "1.0.0")
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        opensearch_component: InputComponentFromSource = manifest.components["OpenSearch"]  # type: ignore[assignment]
        self.assertIsInstance(opensearch_component, InputComponentFromSource)
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "1.0")
        for component in manifest.components.values():
            self.assertIsInstance(component, InputComponentFromSource)

    def test_1_1(self) -> None:
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.filename, "opensearch")
        self.assertEqual(manifest.build.version, "1.1.0")
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        # opensearch component
        opensearch_component: InputComponentFromSource = manifest.components["OpenSearch"]  # type: ignore[assignment]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "tags/1.1.0")
        # components
        for component in manifest.components.values():
            self.assertIsInstance(component, InputComponentFromSource)
        # alerting component checks
        alerting_component: InputComponentFromSource = manifest.components["alerting"]  # type: ignore[assignment]
        self.assertIsNotNone(alerting_component)
        self.assertEqual(len(alerting_component.checks), 2)
        for check in alerting_component.checks:
            self.assertIsInstance(check, Check)
        self.assertIsNone(alerting_component.checks[0].args)
        self.assertEqual(alerting_component.checks[1].args, "alerting")

    def test_1_2(self) -> None:
        path = os.path.join(self.manifests_path, "1.2.0/opensearch-1.2.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.filename, "opensearch")
        self.assertEqual(manifest.build.version, "1.2.0")
        self.assertEqual(manifest.ci.image.name, "opensearchstaging/ci-runner:centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211028")
        self.assertEqual(manifest.ci.image.args, "-e JAVA_HOME=/usr/lib/jvm/adoptopenjdk-14-hotspot")
        self.assertNotEqual(len(manifest.components), 0)
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        # opensearch component
        opensearch_component: InputComponentFromSource = manifest.components["OpenSearch"]  # type: ignore[assignment]
        self.assertEqual(opensearch_component.name, "OpenSearch")
        self.assertEqual(
            opensearch_component.repository,
            "https://github.com/opensearch-project/OpenSearch.git",
        )
        self.assertEqual(opensearch_component.ref, "tags/1.2.0")
        # components
        for component in manifest.components.values():
            self.assertIsInstance(component, InputComponentFromSource)
        # alerting component checks
        alerting_component = manifest.components["alerting"]
        self.assertIsNotNone(alerting_component)
        self.assertEqual(len(alerting_component.checks), 2)
        for check in alerting_component.checks:
            self.assertIsInstance(check, Check)
        self.assertIsNone(alerting_component.checks[0].args)
        self.assertEqual(alerting_component.checks[1].args, "alerting")

    def test_to_dict(self) -> None:
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        data = manifest.to_dict()
        with open(path) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_invalid_ref(self) -> None:
        data_path = os.path.join(os.path.dirname(__file__), "data")
        manifest_path = os.path.join(data_path, "invalid-ref.yml")

        with self.assertRaises(Exception) as context:
            InputManifest.from_path(manifest_path)
        self.assertTrue(str(context.exception).startswith("Invalid manifest schema: {'components': "))

    def test_select(self) -> None:
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        self.assertEqual(len(list(manifest.components.select(focus="common-utils"))), 1)
        self.assertNotEqual(len(list(manifest.components.select(platform="windows"))), 0)
        self.assertEqual(len(list(manifest.components.select(focus="k-NN", platform="linux"))), 1)

    def test_select_none(self) -> None:
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path)
        with self.assertRaises(ValueError) as ctx:
            self.assertEqual(len(list(manifest.components.select(focus="k-NN", platform="windows"))), 0)
        self.assertEqual(str(ctx.exception), "No components matched focus=k-NN, platform=windows.")

    def test_component___matches__(self) -> None:
        self.assertTrue(InputComponent({"name": "x", "repository": "", "ref": ""}).__matches__())

    def test_component___matches_platform__(self) -> None:
        data = {"name": "x", "repository": "", "ref": ""}
        self.assertTrue(InputComponent(data).__matches__(platform=None))
        self.assertTrue(InputComponent(data).__matches__(platform="x"))
        self.assertTrue(InputComponent({**data, "platforms": ["linux"]}).__matches__(platform="linux"))
        self.assertTrue(InputComponent({**data, "platforms": ["linux", "windows"]}).__matches__(platform="linux"))
        self.assertFalse(InputComponent({**data, "platforms": ["linux"]}).__matches__(platform="x"))

    def test_component___matches_focus__(self) -> None:
        component = InputComponent({"name": "x", "repository": "", "ref": ""})
        self.assertTrue(component.__matches__(focus=None))
        self.assertTrue(component.__matches__(focus="x"))
        self.assertFalse(component.__matches__(focus="y"))

    @patch("subprocess.check_output")
    def test_stable(self, mock_output: Mock) -> None:
        mock_output.return_value.decode.return_value = "updated\tHEAD"
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path).stable()
        opensearch: InputComponentFromSource = manifest.components["OpenSearch"]  # type: ignore[assignment]
        self.assertEqual(opensearch.ref, "updated")

    @patch("subprocess.check_output")
    @patch("git.git_repository.GitRepository.stable_ref", return_value=('abcd', '1234'))
    def test_stable_override_build(self, git_repo: Mock, mock_output: Mock) -> None:
        mock_output.return_value.decode.return_value = "updated\tHEAD"
        path = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest = InputManifest.from_path(path).stable()
        opensearch: InputComponentFromSource = manifest.components["OpenSearch"]  # type: ignore[assignment]
        self.assertEqual(opensearch.ref, "abcd")

    def test_eq(self) -> None:
        path = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        manifest1 = InputManifest.from_path(path)
        manifest2 = InputManifest.from_path(path)
        self.assertEqual(manifest1, manifest1)
        self.assertEqual(manifest1, manifest2)

    def test_neq(self) -> None:
        path1 = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        path2 = os.path.join(self.manifests_path, "1.1.0", "opensearch-1.1.0.yml")
        manifest1 = InputManifest.from_path(path1)
        manifest2 = InputManifest.from_path(path2)
        self.assertNotEqual(manifest1, manifest2)

    def test_neq_update(self) -> None:
        path = os.path.join(self.manifests_path, "1.0.0", "opensearch-1.0.0.yml")
        manifest1 = InputManifest.from_path(path)
        manifest2 = copy.deepcopy(manifest1)
        self.assertEqual(manifest1, manifest2)
        manifest2.components["name"] = InputComponentFromDist({
            "name": "name",
            "dist": "dist"
        })
        self.assertNotEqual(manifest1, manifest2)
