# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, PropertyMock, call, mock_open, patch

from system.os import current_platform
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.service_opensearch_dashboards import ServiceOpenSearchDashboards


class ServiceOpenSearchDashboardsTests(unittest.TestCase):
    version: str
    distribution: str
    work_dir: str
    additional_config: dict
    dependency_installer: DependencyInstaller

    def setUp(self) -> None:
        self.version = "1.1.0"
        self.distribution = "tar"
        self.work_dir = "test_work_dir"
        self.additional_config = {"script.context.field.max_compilations_rate": "1000/1m"}
        self.dependency_installer = None

    @patch("test_workflow.integ_test.service.Process.start")
    @patch('test_workflow.integ_test.service.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start(self, mock_tarfile_open: Mock, mock_dump: Mock, mock_file: Mock, mock_pid: Mock, mock_process: Mock) -> None:

        mock_dependency_installer = MagicMock()

        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            mock_dependency_installer,
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
        mock_tarfile_open.assert_called_once_with(bundle_full_name, "r:gz")
        mock_bundle_tar.extractall.assert_called_once_with(self.work_dir)

        mock_file.assert_called_once_with(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "config", "opensearch_dashboards.yml"), "a")
        mock_dump.assert_called_once_with(
            {
                "script.context.field.max_compilations_rate": "1000/1m",
                "logging.dest": os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "logs", "opensearch_dashboards.log")
            }
        )
        mock_file.return_value.write.assert_called_once_with(mock_dump_result)

        mock_process.assert_called_once_with("./opensearch-dashboards", os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "bin"))
        self.assertEqual(mock_pid.call_count, 1)

    @patch("os.path.isdir")
    @patch("subprocess.check_call")
    @patch("test_workflow.integ_test.service.Process.start")
    @patch('test_workflow.integ_test.service.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start_without_security(self, mock_tarfile_open: Mock, mock_dump: Mock, mock_file: Any, mock_pid: Mock, mock_process: Mock, mock_check_call: Mock, mock_os_isdir: Mock) -> None:

        mock_dependency_installer = MagicMock()

        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            {},
            False,
            mock_dependency_installer,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        mock_dependency_installer.download_dist.return_value = bundle_full_name

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_bundle_tar

        mock_file_handler_for_security = mock_open().return_value
        mock_file_handler_for_additional_config = mock_open().return_value

        # open() will be called twice, one for disabling security, second for additional_config
        mock_file.side_effect = [mock_file_handler_for_security, mock_file_handler_for_additional_config]

        mock_dump_result = MagicMock()
        mock_dump.return_value = mock_dump_result

        mock_os_isdir.return_value = True

        # call the target test function
        service.start()

        mock_file.assert_has_calls(
            [call(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "config", "opensearch_dashboards.yml"), "w")],
            [call(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "config", "opensearch_dashboards.yml"), "a")],
        )

        plugin_script = "opensearch-dashboards-plugin.bat" if current_platform() == "windows" else "bash opensearch-dashboards-plugin"
        mock_check_call.assert_called_once_with(
            f"{plugin_script} remove --allow-root securityDashboards",
            cwd=os.path.join("test_work_dir", "opensearch-dashboards-1.1.0", "bin"),
            shell=True
        )

        mock_dump.assert_called_once_with({"logging.dest": os.path.join(
            self.work_dir, "opensearch-dashboards-1.1.0", "logs", "opensearch_dashboards.log")})

        mock_file_handler_for_security.close.assert_called_once()
        mock_file_handler_for_additional_config.write.assert_called_once_with(mock_dump_result)

    @patch("os.path.isdir")
    @patch("subprocess.check_call")
    @patch("test_workflow.integ_test.service.Process.start")
    @patch('test_workflow.integ_test.service.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start_without_security_and_not_installed(
        self,
        mock_tarfile_open: Mock,
        mock_dump: Mock,
        mock_file: Any,
        mock_pid: Mock,
        mock_process: Mock,
        mock_check_call: Mock,
        mock_os_isdir: Mock
    ) -> None:

        mock_dependency_installer = MagicMock()

        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            {},
            False,
            mock_dependency_installer,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        mock_dependency_installer.download_dist.return_value = bundle_full_name

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_bundle_tar

        mock_file_handler_for_security = mock_open().return_value
        mock_file_handler_for_additional_config = mock_open().return_value

        # open() will be called twice, one for disabling security, second for additional_config
        mock_file.side_effect = [mock_file_handler_for_security, mock_file_handler_for_additional_config]

        mock_dump_result = MagicMock()
        mock_dump.return_value = mock_dump_result

        mock_os_isdir.side_effect = [False, True]

        # call the target test function
        service.start()

        mock_check_call.assert_not_called()

        mock_file.assert_has_calls(
            [call(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "config", "opensearch_dashboards.yml"), "w")],
            [call(os.path.join(self.work_dir, "opensearch-dashboards-1.1.0", "config", "opensearch_dashboards.yml"), "a")],
        )

        mock_dump.assert_called_once_with({"logging.dest": os.path.join(
            self.work_dir, "opensearch-dashboards-1.1.0", "logs", "opensearch_dashboards.log")})

        mock_file_handler_for_security.close.assert_called_once()
        mock_file_handler_for_additional_config.write.assert_called_once_with(mock_dump_result)

    def test_endpoint_port_url(self) -> None:
        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        self.assertEqual(service.endpoint(), "localhost")
        self.assertEqual(service.port(), 5601)
        self.assertEqual(service.url(), "http://localhost:5601")

    @patch("requests.get")
    @patch.object(ServiceOpenSearchDashboards, "url")
    def test_get_service_response_with_security(self, mock_url: Mock, mock_requests_get: Mock) -> None:
        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_url_result = MagicMock()
        mock_url.return_value = mock_url_result

        service.get_service_response()

        mock_url.assert_called_once_with("/api/status")
        mock_requests_get.assert_called_once_with(mock_url_result, verify=False, auth=("admin", "admin"))

    @patch("requests.get")
    @patch.object(ServiceOpenSearchDashboards, "url")
    def test_get_service_response_without_security(self, mock_url: Mock, mock_requests_get: Mock) -> None:
        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            False,
            self.dependency_installer,
            self.work_dir
        )

        mock_url_result = MagicMock()
        mock_url.return_value = mock_url_result

        service.get_service_response()

        mock_url.assert_called_once_with("/api/status")
        mock_requests_get.assert_called_once_with(mock_url_result, auth=None, verify=False)

    @patch.object(ServiceOpenSearchDashboards, "get_service_response")
    def test_service_alive_green_available(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"state":"green"'

        mock_get_service_response.return_value = mock_response

        self.assertTrue(service.service_alive())

    @patch.object(ServiceOpenSearchDashboards, "get_service_response")
    def test_service_alive_yellow_available(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"state":"yellow"'

        mock_get_service_response.return_value = mock_response

        self.assertTrue(service.service_alive())

    @patch.object(ServiceOpenSearchDashboards, "get_service_response")
    def test_service_alive_red_unavailable(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearchDashboards(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"state":"red"'

        mock_get_service_response.return_value = mock_response

        self.assertFalse(service.service_alive())
