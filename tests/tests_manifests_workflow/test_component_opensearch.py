# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from git.git_repository import GitRepository
from manifests_workflow.component_opensearch import ComponentOpenSearch


class TestComponentOpenSearch(unittest.TestCase):
    @patch("os.makedirs")
    @patch.object(GitRepository, "__checkout__")
    def test_checkout(self, *mocks: MagicMock) -> None:
        component = ComponentOpenSearch.checkout("common-utils", "path", "1.1.0")
        self.assertEqual(component.name, "common-utils")
        self.assertFalse(component.snapshot)

    def test_version(self) -> None:
        repo = MagicMock()
        repo.output.return_value = "version=2.1"
        component = ComponentOpenSearch("common-utils", repo, "1.1.0")
        self.assertEqual(component.version, "2.1")

    def test_properties(self) -> None:
        repo = MagicMock()
        repo.output.return_value = "version=2.1"
        component = ComponentOpenSearch("common-utils", repo, "1.1.0")
        self.assertEqual(component.properties.get_value("version"), "2.1")

    def test_to_dict(self) -> None:
        repo = MagicMock(ref="ref", url="repo")
        repo.output.return_value = "version=2.1"
        component = ComponentOpenSearch("common-utils", repo, "1.1.0")
        self.assertEqual(
            component.to_dict(),
            {"name": "common-utils", "ref": "ref", "repository": "repo"},
        )

    def test_gradle_cmd_target(self) -> None:
        self.assertEqual(ComponentOpenSearch.gradle_cmd("properties"), "./gradlew properties")

    def test_gradle_cmd_prop(self) -> None:
        self.assertEqual(
            ComponentOpenSearch.gradle_cmd("properties", {"build.snapshot": "false"}),
            "./gradlew properties -Dbuild.snapshot=false",
        )

    def test_gradle_cmd_props(self) -> None:
        self.assertEqual(
            ComponentOpenSearch.gradle_cmd("properties", {"build.snapshot": "false", "opensearch.version": "1.0"}),
            "./gradlew properties -Dbuild.snapshot=false -Dopensearch.version=1.0",
        )
