# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from manifests.test_manifest import TestManifest


class TestTestManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-test-1.1.0.yml")
        self.manifest = TestManifest.from_path(self.manifest_filename)

    def test_component(self):
        component = self.manifest.components["index-management"]
        self.assertEqual(component.name, "index-management")
        self.assertEqual(component.integ_test, {"test-configs": ["with-security", "without-security"]})
        self.assertEqual(component.bwc_test, {"test-configs": ["with-security", "without-security"]})

    def test_component_with_working_directory(self):
        component = self.manifest.components["dashboards-reports"]
        self.assertEqual(component.name, "dashboards-reports")
        self.assertEqual(component.working_directory, "reports-scheduler")
        self.assertEqual(component.integ_test, {"test-configs": ["without-security"]})
        self.assertEqual(component.bwc_test, {"test-configs": ["without-security"]})

    def test_to_dict(self):
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)

    def test_versions(self):
        self.assertTrue(len(TestManifest.VERSIONS))
        for version in TestManifest.VERSIONS:
            manifest = TestManifest.from_path(os.path.join(self.data_path, "test", f"opensearch-test-schema-version-{version}.yml"))
            self.assertEqual(version, manifest.version)
