# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, patch

from test_workflow.bwc_test.bwc_test_start_properties_opensearch_dashboards import BwcTestStartPropertiesOpenSearchDashboards


class TestBwcTestStartPropertiesOpenSearchDashboards(unittest.TestCase):

    @patch("test_workflow.bwc_test.bwc_test_start_properties.BundleManifest")
    @patch("test_workflow.bwc_test.bwc_test_start_properties.BuildManifest")
    def test(self, mock_build: Mock, mock_bundle: Mock) -> None:
        path = "test-path"

        mock_bundle_object = MagicMock()
        mock_bundle.from_urlpath.return_value = mock_bundle_object

        mock_build_object = MagicMock()
        mock_build.from_urlpath.return_value = mock_build_object

        BwcTestStartPropertiesOpenSearchDashboards(path)

        mock_bundle.from_urlpath.assert_called_once_with("/".join([path.rstrip("/"), "dist/opensearch-dashboards/manifest.yml"]))
        mock_build.from_urlpath.assert_called_once_with("/".join([path.rstrip("/"), "builds/opensearch-dashboards/manifest.yml"]))
