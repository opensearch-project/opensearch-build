# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, PropertyMock, mock_open, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.integ_test.service_opensearch_dashboards import ServiceOpenSearchDashboards


class ServiceOpenSearchDashboardsTests(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    def setUp(self):
        self.bundle_manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.component_name = "sql"
        self.work_dir = "test_work_dir"
        self.additional_cluster_config = {"script.context.field.max_compilations_rate": "1000/1m"}
        self.component_test_config = "test_config"
        self.dependency_installer = ""
        self.save_logs = ""

    @patch("test_workflow.integ_test.service_opensearch_dashboards.Process.start")
    @patch('test_workflow.integ_test.service_opensearch_dashboards.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start(self, mock_tarfile_open, mock_dump, mock_file, mock_pid, mock_process):

        mock_dependency_installer = MagicMock()

        service = ServiceOpenSearchDashboards(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            mock_dependency_installer,
            self.save_logs,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        mock_dependency_installer.download_dist.return_value = bundle_full_name

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_bundle_tar

        mock_dump_result = MagicMock()
        mock_dump.return_value = mock_dump_result

        # call the target test function
        service.start()

        mock_dependency_installer.download_dist.called_once_with(self.work_dir)
        mock_tarfile_open.assert_called_once_with(bundle_full_name, "r")
        mock_bundle_tar.extractall.assert_called_once_with(self.work_dir)

        mock_file.assert_called_once_with(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0-linux-x64", "config", "opensearch_dashboards.yml"), "a")
        mock_dump.assert_called_once_with(self.additional_cluster_config)
        mock_file.return_value.write.assert_called_once_with(mock_dump_result)

        mock_process.assert_called_once_with("./opensearch-dashboards", os.path.join(self.work_dir, "opensearch-dashboards-1.1.0-linux-x64", "bin"))
        self.assertEqual(mock_pid.call_count, 1)

    @patch("subprocess.check_call")
    @patch("test_workflow.integ_test.service_opensearch_dashboards.Process.start")
    @patch('test_workflow.integ_test.service_opensearch_dashboards.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("tarfile.open")
    def test_start_without_security(self, mock_tarfile_open, mock_file, mock_pid, mock_process, mock_check_call):

        mock_dependency_installer = MagicMock()

        service = ServiceOpenSearchDashboards(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            {},
            False,
            mock_dependency_installer,
            self.save_logs,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        mock_dependency_installer.download_dist.return_value = bundle_full_name

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_bundle_tar

        # call the target test function
        service.start()

        mock_check_call.assert_called_once_with(
            "./opensearch-dashboards-plugin remove securityDashboards",
            cwd=os.path.join("test_work_dir", "opensearch-dashboards-1.1.0-linux-x64", "bin"),
            shell=True
        )

        mock_file.assert_called_once_with(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0-linux-x64", "config", "opensearch_dashboards.yml"), "w")
        mock_file.return_value.close.assert_called_once()

    def test_endpoint_port_url(self):
        service = ServiceOpenSearchDashboards(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        self.assertEqual(service.endpoint(), "localhost")
        self.assertEqual(service.port(), 5601)
        self.assertEqual(service.url(), "http://localhost:5601")

    @patch("requests.get")
    @patch.object(ServiceOpenSearchDashboards, "url")
    def test_get_service_response_with_security(self, mock_url, mock_requests_get):
        service = ServiceOpenSearchDashboards(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        mock_url_result = MagicMock()
        mock_url.return_value = mock_url_result

        service.get_service_response()

        mock_url.assert_called_once_with("/api/status")
        mock_requests_get.assert_called_once_with(mock_url_result, verify=False, auth=("kibanaserver", "kibanaserver"))

    @patch("requests.get")
    @patch.object(ServiceOpenSearchDashboards, "url")
    def test_get_service_response_without_security(self, mock_url, mock_requests_get):
        service = ServiceOpenSearchDashboards(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            False,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        mock_url_result = MagicMock()
        mock_url.return_value = mock_url_result

        service.get_service_response()

        mock_url.assert_called_once_with("/api/status")
        mock_requests_get.assert_called_once_with(mock_url_result, auth=None, verify=False)
