# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from abc import abstractmethod

from manifests.component_manifest import ComponentManifest


class TestComponentManifest(unittest.TestCase):
    class UnitTestManifest(ComponentManifest):
        class Components(ComponentManifest.Components):
            @abstractmethod
            def __create__(self, data):
                return TestComponentManifest.UnitTestManifest.Component(data)

        class Component(ComponentManifest.Component):
            pass

    def test_select(self):
        manifest = TestComponentManifest.UnitTestManifest({
            "schema-version": "1.0",
            "components": [
                {"name": "one"},
                {"name": "two"}
            ]
        })

        self.assertEqual(len(list(manifest.components.select(focus=None))), 2)
        self.assertEqual(len(list(manifest.components.select(focus="one"))), 1)
        self.assertEqual(next(manifest.components.select(focus="two")).name, "two")
