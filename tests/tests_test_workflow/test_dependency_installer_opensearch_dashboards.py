import unittest
from unittest.mock import MagicMock

from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards


class DependencyInstallerOpenSearchDashboardsTests(unittest.TestCase):

    def test(self):
        mock_root_url = MagicMock()
        mock_build_manifest = MagicMock()
        mock_bundle_manifest = MagicMock()

        dependency_installer = DependencyInstallerOpenSearchDashboards(mock_root_url, mock_build_manifest, mock_bundle_manifest)

        self.assertEqual(dependency_installer.root_url, mock_root_url)
        self.assertEqual(dependency_installer.build_manifest, mock_build_manifest)
        self.assertEqual(dependency_installer.bundle_manifest, mock_bundle_manifest)
