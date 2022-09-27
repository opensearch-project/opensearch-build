# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from git.git_repository import GitRepository
from manifests_workflow.component_opensearch_dashboards_min import ComponentOpenSearchDashboardsMin
from system.config_file import ConfigFile


class TestComponentOpenSearchDashboardsMin(unittest.TestCase):
    @patch("subprocess.check_output")
    def test_branches(self, mock: MagicMock) -> None:
        mock.return_value = "\n".join(["main", "1.x", "1.21", "20.1", "something", "else"]).encode()
        self.assertEqual(ComponentOpenSearchDashboardsMin.branches(), ["main", "1.x", "1.21", "20.1"])
        mock.assert_called_with(
            "git ls-remote https://github.com/opensearch-project/OpenSearch-Dashboards.git refs/heads/* | cut -f2 | cut -d/ -f3",
            shell=True,
        )

    @patch("os.makedirs")
    @patch.object(GitRepository, "__checkout__")
    def test_checkout(self, *mocks: MagicMock) -> None:
        component = ComponentOpenSearchDashboardsMin.checkout("path")
        self.assertEqual(component.name, "OpenSearch-Dashboards")
        self.assertFalse(component.snapshot)

    @patch.object(ConfigFile, "from_file")
    def test_version(self, mock_config: MagicMock) -> None:
        mock_config.return_value = ConfigFile('{"version":"2.1"}')
        component = ComponentOpenSearchDashboardsMin(MagicMock(working_directory="path"))
        self.assertEqual(component.version, "2.1")

    @patch.object(ConfigFile, "from_file")
    def test_properties(self, mock_config: MagicMock) -> None:
        mock_config.return_value = ConfigFile('{"version":"2.1"}')
        component = ComponentOpenSearchDashboardsMin(MagicMock(working_directory="path"))
        self.assertEqual(component.properties.get_value("version"), "2.1")

    @patch.object(ConfigFile, "from_file")
    def test_to_dict(self, mock_config: MagicMock) -> None:
        mock_config.return_value = ConfigFile('{"version":"2.1"}')
        repo = MagicMock(ref="ref", url="repo")
        component = ComponentOpenSearchDashboardsMin(repo)
        self.assertEqual(
            component.to_dict(),
            {"name": "OpenSearch-Dashboards", "ref": "ref", "repository": "repo"},
        )
