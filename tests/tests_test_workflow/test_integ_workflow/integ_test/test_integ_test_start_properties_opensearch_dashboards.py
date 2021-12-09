# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from test_workflow.integ_test.integ_test_start_properties_opensearch_dashboards import IntegTestStartPropertiesOpenSearchDashboards


class TestIntegTestStartPropertiesOpenSearchDashboards(unittest.TestCase):

    @patch("test_workflow.integ_test.integ_test_start_properties.BundleManifest")
    @patch("test_workflow.integ_test.integ_test_start_properties.BuildManifest")
    @patch("test_workflow.integ_test.integ_test_start_properties_opensearch_dashboards.DependencyInstallerOpenSearchDashboards")
    def test(self, mock_installer, mock_build, mock_bundle):
        path = "test-path"

        mock_bundle_object = MagicMock()
        mock_bundle.from_urlpath.return_value = mock_bundle_object

        mock_build_object = MagicMock()
        mock_build.from_urlpath.return_value = mock_build_object

        IntegTestStartPropertiesOpenSearchDashboards(path)

        mock_bundle.from_urlpath.assert_called_once_with("/".join([path.rstrip("/"), "dist/opensearch-dashboards/manifest.yml"]))
        mock_build.from_urlpath.assert_called_once_with("/".join([path.rstrip("/"), "builds/opensearch-dashboards/manifest.yml"]))

        mock_installer.assert_called_with(path, mock_build_object, mock_bundle_object)
