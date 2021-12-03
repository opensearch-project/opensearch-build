# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from typing import Any

from manifests.component_manifest import Component, ComponentManifest, Components


class TestComponentManifest(unittest.TestCase):
    class UnitTestManifest(ComponentManifest['TestComponentManifest.UnitTestManifest', 'TestComponentManifest.TestComponents']):
        pass

    class TestComponents(Components['TestComponentManifest.TestComponent']):
        @classmethod
        def __create__(self, data: Any) -> 'TestComponentManifest.TestComponent':
            return TestComponentManifest.TestComponent(data)

    class TestComponent(Component):
        pass

    def test_select(self) -> None:
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
