# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from git.git_repository import GitRepository
from manifests_workflow.component_opensearch_min import ComponentOpenSearchMin


class TestComponentOpenSearchMin(unittest.TestCase):
    @patch("subprocess.check_output")
    def test_branches(self, mock: MagicMock) -> None:
        mock.return_value = "\n".join(["main", "1.x", "1.21", "20.1", "something", "else"]).encode()
        self.assertEqual(ComponentOpenSearchMin.branches(), ["main", "1.x", "1.21", "20.1"])
        mock.assert_called_with(
            "git ls-remote https://github.com/opensearch-project/OpenSearch.git refs/heads/* | cut -f2 | cut -d/ -f3",
            shell=True,
        )

    @patch("os.makedirs")
    @patch.object(GitRepository, "__checkout__")
    def test_checkout(self, *mocks: MagicMock) -> None:
        component = ComponentOpenSearchMin.checkout("path")
        self.assertEqual(component.name, "OpenSearch")
        self.assertFalse(component.snapshot)

    def test_version(self) -> None:
        repo = MagicMock()
        repo.output.return_value = "version=2.1"
        component = ComponentOpenSearchMin(repo)
        self.assertEqual(component.version, "2.1")

    def test_properties(self) -> None:
        repo = MagicMock()
        repo.output.return_value = "version=2.1"
        component = ComponentOpenSearchMin(repo)
        self.assertEqual(component.properties.get_value("version"), "2.1")

    def test_to_dict(self) -> None:
        repo = MagicMock(ref="ref", url="repo")
        repo.output.return_value = "version=2.1"
        component = ComponentOpenSearchMin(repo)
        self.assertEqual(
            component.to_dict(),
            {
                "checks": ["gradle:publish", "gradle:properties:version"],
                "name": "OpenSearch",
                "ref": "ref",
                "repository": "repo",
            },
        )
