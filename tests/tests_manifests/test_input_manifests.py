# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from manifests.input_manifests import InputManifests


class TestInputManifests(unittest.TestCase):
    def setUp(self):
        self.manifests = InputManifests()

    def tests_configs(self):
        self.assertTrue(len(self.manifests))

    def test_1_1_0(self):
        manifest = self.manifests["1.1.0"]
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.version, "1.0")
        self.assertEqual(manifest.build.version, "1.1.0")

    def test_latest(self):
        manifest = self.manifests.latest
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.build.version, max(self.manifests.keys()))
