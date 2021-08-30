# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from manifests.manifest import Manifest


class TestManifest(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "data")

    def test_manifest_is_abstract(self):
        with self.assertRaises(TypeError) as context:
            Manifest(None)
            self.assertEqual(
                "Can't instantiate abstract class Manifest with abstract methods __init__",
                context.exception.__str__(),
            )

    def test_invalid_version(self):
        class TestManifest(Manifest):
            def __init__(self, data):
                super().__init__(data)

        manifest_path = os.path.join(self.data_path, "invalid-schema-version.yml")

        with self.assertRaises(ValueError) as context:
            TestManifest.from_path(manifest_path)
            self.assertEqual(
                "Unsupported schema version: invalid", context.exception.__str__()
            )
