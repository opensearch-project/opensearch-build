# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, PropertyMock
from manifests.input_manifest import InputManifest

from ci_workflow.check import Check

class DummyTestCheck(Check):
    def check():
        pass

class TestCheck(unittest.TestCase):
    def setUp(self):
        self.check = DummyTestCheck(
            component=MagicMock(),
            git_repo=MagicMock(),
            version="1.1.0",
            arch="x86",
            snapshot=False,
        )

    def test_properties(self):
        self.assertEqual(self.check.arch, "x86")
        self.assertEqual(self.check.version, "1.1.0")
        self.assertFalse(self.check.snapshot)
        self.assertEqual(self.check.opensearch_version, "1.1.0")
        self.assertEqual(self.check.component_version, "1.1.0.0")

class TestCheckSnapshot(unittest.TestCase):
    def setUp(self):
        self.check = DummyTestCheck(
            component=MagicMock(),
            git_repo=MagicMock(),
            version="1.1.0",
            arch="x86",
            snapshot=True,
        )

    def test_snapshot_version(self):
        self.assertTrue(self.check.snapshot)
        self.assertEqual(self.check.opensearch_version, "1.1.0-SNAPSHOT")
        self.assertEqual(self.check.component_version, "1.1.0.0-SNAPSHOT")

class TestCheckOpenSearch(unittest.TestCase):
    def setUp(self):
        self.check = DummyTestCheck(
            component=InputManifest.Component({ 
                "name": "OpenSearch",
                "repository": "",
                "ref": "",
            }),
            git_repo=MagicMock(),
            version="1.1.0",
            arch="x86",
            snapshot=True,
        )

    def test_component_version(self):
        self.assertEqual(self.check.component_version, "1.1.0-SNAPSHOT")
