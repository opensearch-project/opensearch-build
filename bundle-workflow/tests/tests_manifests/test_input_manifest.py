# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from manifests.input_manifest import InputManifest


class TestInputManifest(unittest.TestCase):
    def setUp(self):
        self.manifests_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../../../manifests")
        )

    def test_from_file_1_0(self):
        with open(os.path.join(self.manifests_path, "opensearch-1.0.0.yml")) as f:
            manifest = InputManifest.from_file(f)
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

    def test_from_file_1_1(self):
        with open(os.path.join(self.manifests_path, "opensearch-1.1.0.yml")) as f:
            manifest = InputManifest.from_file(f)
            self.assertEqual(manifest.version, "1.0")
            self.assertEqual(manifest.build.name, "OpenSearch")
            self.assertEqual(manifest.build.version, "1.1.0")
            self.assertEqual(len(manifest.components), 15)
            opensearch_component = manifest.components[0]
            self.assertEqual(opensearch_component.name, "OpenSearch")
            self.assertEqual(
                opensearch_component.repository,
                "https://github.com/opensearch-project/OpenSearch.git",
            )
            self.assertEqual(opensearch_component.ref, "1.x")
            for component in manifest.components:
                self.assertIsInstance(component.ref, str)
