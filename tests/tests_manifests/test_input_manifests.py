# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from manifests.input_manifests import InputManifests


class TestInputManifests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifests = InputManifests()

    def tests_configs(self) -> None:
        self.assertTrue(len(self.manifests))

    def test_3_0_0(self) -> None:
        manifest = self.manifests["3.0.0"]
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.version, "3.0.0")
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.filename, "opensearch")

    def test_latest(self) -> None:
        manifest = self.manifests.latest
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.build.version, max(self.manifests.keys()))
        self.assertEqual(manifest.build.name, "OpenSearch")
        self.assertEqual(manifest.build.filename, "opensearch")
