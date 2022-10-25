# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import unittest
from unittest.mock import MagicMock

from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards


class DependencyInstallerOpenSearchDashboardsTests(unittest.TestCase):

    def test(self) -> None:
        mock_root_url = MagicMock()
        mock_build_manifest = MagicMock()
        mock_bundle_manifest = MagicMock()

        dependency_installer = DependencyInstallerOpenSearchDashboards(mock_root_url, mock_build_manifest, mock_bundle_manifest)

        self.assertEqual(dependency_installer.root_url, mock_root_url)
        self.assertEqual(dependency_installer.build_manifest, mock_build_manifest)
        self.assertEqual(dependency_installer.bundle_manifest, mock_bundle_manifest)
