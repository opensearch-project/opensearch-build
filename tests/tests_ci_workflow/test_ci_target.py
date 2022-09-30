# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from ci_workflow.ci_target import CiTarget


class TestCiTarget(unittest.TestCase):
    def test_opensearch_version(self) -> None:
        self.assertEqual(CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=False).opensearch_version, "1.1.0")

    def test_opensearch_version_snapshot(self) -> None:
        self.assertEqual(
            CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=True).opensearch_version,
            "1.1.0-SNAPSHOT",
        )

    def test_opensearch_version_qualifier_snapshot(self) -> None:
        self.assertEqual(
            CiTarget(version="1.3.0", name="opensearch", qualifier="alpha1", snapshot=True).opensearch_version,
            "1.3.0-alpha1-SNAPSHOT",
        )

    def test_component_version(self) -> None:
        self.assertEqual(CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=False).component_version, "1.1.0.0")

    def test_component_version_snapshot(self) -> None:
        self.assertEqual(
            CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=True).component_version,
            "1.1.0.0-SNAPSHOT",
        )

    def test_component_version_qualifier_snapshot(self) -> None:
        self.assertEqual(
            CiTarget(version="1.3.0", name="opensearch", qualifier="alpha1", snapshot=True).component_version,
            "1.3.0.0-alpha1-SNAPSHOT",
        )
