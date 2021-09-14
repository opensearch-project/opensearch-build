# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from manifests_workflow.component import Component


class TestComponent(unittest.TestCase):
    def test_gradle_cmd_target(self):
        self.assertEqual(Component.gradle_cmd("properties"), "./gradlew properties")

    def test_gradle_cmd_prop(self):
        self.assertEqual(
            Component.gradle_cmd("properties", {"build.snapshot": "false"}),
            "./gradlew properties -Dbuild.snapshot=false",
        )

    def test_gradle_cmd_props(self):
        self.assertEqual(
            Component.gradle_cmd(
                "properties", {"build.snapshot": "false", "opensearch.version": "1.0"}
            ),
            "./gradlew properties -Dbuild.snapshot=false -Dopensearch.version=1.0",
        )
