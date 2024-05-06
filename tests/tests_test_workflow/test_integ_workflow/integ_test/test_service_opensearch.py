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

import requests

from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.service_opensearch import ServiceOpenSearch


class ServiceOpenSearchTests(unittest.TestCase):
    version: str
    distribution: str
    work_dir: str
    additional_config: dict
    dependency_installer: DependencyInstaller
    save_logs: str

    def setUp(self) -> None:
        self.version = "1.1.0"
        self.distribution = "tar"
        self.work_dir = "test_work_dir"
        self.additional_config = {"script.context.field.max_compilations_rate": "1000/1m"}
        self.dependency_installer = None
        self.save_logs = ""

    @patch("test_workflow.integ_test.service.Process.start")
    @patch('test_workflow.integ_test.service.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start(self, mock_tarfile_open: Mock, mock_dump: Mock, mock_file: Mock, mock_pid: Mock,
                   mock_process: Mock) -> None:
        dependency_installer = MagicMock()

        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            dependency_installer,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        dependency_installer.download_dist.return_value = bundle_full_name

        mock_dump_result = MagicMock()
        mock_dump.return_value = mock_dump_result

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_bundle_tar

        # call test target function
        service.start()

        mock_process.assert_called_once_with(
            "export OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123! && ./opensearch-tar-install.sh",
            os.path.join(self.work_dir, "opensearch-1.1.0"), False)

        mock_dump.assert_called_once_with(self.additional_config)

        assert mock_file.call_count == 3
        mock_file.assert_any_call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "jvm.options"), "r")
        mock_file.assert_any_call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "jvm.options"), "w")
        mock_file.assert_any_call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a")

        mock_file.return_value.write.assert_has_calls([call(''), call(mock_dump_result)])

        dependency_installer.download_dist.assert_called_once_with(self.work_dir)
        mock_tarfile_open.assert_called_once_with(bundle_full_name, "r:gz")
        mock_bundle_tar.extractall.assert_called_once_with(self.work_dir)

        self.assertEqual(mock_pid.call_count, 1)

    @patch("os.path.isdir")
    @patch("test_workflow.integ_test.service.Process.start")
    @patch('test_workflow.integ_test.service.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start_security_disabled(self, mock_tarfile_open: Mock, mock_dump: Mock, mock_file: Any, mock_pid: Mock,
                                     mock_process: Mock, mock_os_isdir: Mock) -> None:
        dependency_installer = MagicMock()

        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            False,
            dependency_installer,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        dependency_installer.download_dist.return_value = bundle_full_name

        mock_dump_result_for_security = MagicMock()
        mock_dump_result_for_additional_config = MagicMock()

        mock_dump.side_effect = [mock_dump_result_for_security, mock_dump_result_for_additional_config]

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value = mock_bundle_tar

        mock_file_handler_for_security = mock_open().return_value
        mock_file_handler_for_additional_config = mock_open().return_value
        mock_file_handler_for_jvm_read = mock_open().return_value
        mock_file_handler_for_jvm_write = mock_open().return_value

        # open() will be called twice, one for disabling security, second for additional_config
        mock_file.side_effect = [mock_file_handler_for_jvm_read, mock_file_handler_for_jvm_write,
                                 mock_file_handler_for_security, mock_file_handler_for_additional_config]

        mock_os_isdir.return_value = True

        # call test target function
        service.start()

        mock_dump.assert_has_calls([call({"plugins.security.disabled": "true"}), call(self.additional_config)])

        assert mock_file.call_count == 4
        mock_file.assert_has_calls(
            [call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "jvm.options"), "r"),
             call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "jvm.options"), "w"),
             call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a"),
             call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a"), ]
        )

        mock_file_handler_for_security.write.assert_called_once_with(mock_dump_result_for_security)
        mock_file_handler_for_additional_config.write.assert_called_once_with(mock_dump_result_for_additional_config)

    @patch("os.path.isdir")
    @patch("test_workflow.integ_test.service.Process.start")
    @patch('test_workflow.integ_test.service.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start_security_disabled_and_not_installed(self, mock_tarfile_open: Mock, mock_dump: Mock, mock_file: Any,
                                                       mock_pid: Mock, mock_process: Mock, mock_os_isdir: Mock) -> None:
        dependency_installer = MagicMock()

        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            False,
            dependency_installer,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        dependency_installer.download_dist.return_value = bundle_full_name

        mock_dump_result_for_additional_config = MagicMock()

        mock_dump.side_effect = [mock_dump_result_for_additional_config]

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value = mock_bundle_tar

        mock_file_handler_for_security = mock_open().return_value
        mock_file_handler_for_additional_config = mock_open().return_value
        mock_file_handler_for_jvm_read = mock_open().return_value
        mock_file_handler_for_jvm_write = mock_open().return_value

        # open() will be called twice, one for disabling security, second for additional_config
        mock_file.side_effect = [mock_file_handler_for_jvm_read, mock_file_handler_for_jvm_write,
                                 mock_file_handler_for_additional_config]

        mock_os_isdir.return_value = False

        # call test target function
        service.start()

        mock_dump.assert_has_calls([call(self.additional_config)])

        assert mock_file.call_count == 3

        mock_file.assert_has_calls(
            [call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "jvm.options"), "r"),
             call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "jvm.options"), "w"),
             call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a")
             ]
        )
        mock_file_handler_for_security.write.assert_not_called()
        mock_file_handler_for_additional_config.write.assert_called_once_with(mock_dump_result_for_additional_config)

    @patch("test_workflow.integ_test.service.Process.terminate", return_value=123)
    @patch('test_workflow.integ_test.service.Process.started', new_callable=PropertyMock, return_value=True)
    @patch('test_workflow.integ_test.service.Process.stdout_data', new_callable=PropertyMock,
           return_value="test stdout_data")
    @patch('test_workflow.integ_test.service.Process.stderr_data', new_callable=PropertyMock,
           return_value="test stderr_data")
    def test_terminate(
            self,
            mock_process_stderr_data: Mock,
            mock_process_stdout_data: Mock,
            mock_process_started: Mock,
            mock_process_terminate: Mock
    ) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        termination_result = service.terminate()

        mock_process_terminate.assert_called_once()

        self.assertEqual(termination_result.return_code, 123)
        self.assertEqual(termination_result.stdout_data, "test stdout_data")
        self.assertEqual(termination_result.stderr_data, "test stderr_data")
        self.assertEqual(termination_result.log_files,
                         {"opensearch-service-logs": os.path.join("test_work_dir", "opensearch-1.1.0", "logs")})

    @patch("test_workflow.integ_test.service.Process.terminate")
    @patch('test_workflow.integ_test.service.Process.started', new_callable=PropertyMock, return_value=False)
    def test_terminate_process_not_started(self, mock_process_started: Mock, mock_process_terminate: Mock) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        service.terminate()

        mock_process_terminate.assert_not_called()
        mock_process_started.assert_called_once()

    def test_endpoint_port(self) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        self.assertEqual(service.endpoint(), "localhost")
        self.assertEqual(service.port(), 9200)

    def test_url_security_enabled(self) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        self.assertEqual(service.url(), "https://localhost:9200")

    def test_url_security_disabled(self) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            False,
            self.dependency_installer,
            self.work_dir
        )

        self.assertEqual(service.url(), "http://localhost:9200")

    @patch("requests.get")
    @patch.object(ServiceOpenSearch, "url")
    def test_get_service_response(self, mock_url: Mock, mock_requests_get: Mock) -> None:
        service = ServiceOpenSearch(
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

        mock_url.assert_called_once_with("/_cluster/health")
        mock_requests_get.assert_called_once_with(mock_url_result, verify=False, auth=('admin', 'admin'))

    # Below are tests against functions implemented in the base Service class

    @patch("time.sleep")
    @patch.object(ServiceOpenSearch, "service_alive", return_value=True)
    @patch('test_workflow.integ_test.service.Process.stdout_data', new_callable=PropertyMock,
           return_value="test stdout_data")
    @patch('test_workflow.integ_test.service.Process.stderr_data', new_callable=PropertyMock,
           return_value="test stderr_data")
    def test_wait_for_service_succeed_on_first_attemp(self, mock_process_stderr_data: Mock,
                                                      mock_process_stdout_data: Mock, mock_service_alive: Mock,
                                                      mock_time_sleep: Mock) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        service.wait_for_service()

        mock_service_alive.assert_called_once()
        mock_time_sleep.assert_not_called()
        mock_process_stdout_data.assert_not_called()
        mock_process_stderr_data.assert_not_called()

    @patch('test_workflow.integ_test.service.logging.error')
    @patch("time.sleep")
    @patch.object(ServiceOpenSearch, "service_alive", return_value=False)
    @patch('test_workflow.integ_test.service.Process.stdout_data', new_callable=PropertyMock,
           return_value="test stdout_data")
    @patch('test_workflow.integ_test.service.Process.stderr_data', new_callable=PropertyMock,
           return_value="test stderr_data")
    def test_wait_for_service_always_fail_without_exception(
            self,
            mock_process_stderr_data: Mock,
            mock_process_stdout_data: Mock,
            mock_service_alive: Mock,
            mock_time_sleep: Mock,
            mock_logging_error: Mock
    ) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        service.wait_for_service()

        self.assertEqual(mock_service_alive.call_count, 10)
        self.assertEqual(mock_time_sleep.call_count, 10)
        mock_process_stdout_data.assert_not_called()
        mock_process_stderr_data.assert_not_called()
        mock_logging_error.assert_called_with('Cluster is not available after 10 attempts')

    @patch('test_workflow.integ_test.service.logging.error')
    @patch("time.sleep")
    @patch.object(ServiceOpenSearch, "service_alive", side_effect=requests.exceptions.ConnectionError())
    @patch('test_workflow.integ_test.service.Process.stdout_data', new_callable=PropertyMock,
           return_value="test stdout_data")
    @patch('test_workflow.integ_test.service.Process.stderr_data', new_callable=PropertyMock,
           return_value="test stderr_data")
    def test_wait_for_service_always_fail_with_exception(
            self,
            mock_process_stderr_data: Mock,
            mock_process_stdout_data: Mock,
            mock_service_alive: Mock,
            mock_time_sleep: Mock,
            mock_logging_error: Mock
    ) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        service.wait_for_service()

        self.assertEqual(mock_service_alive.call_count, 10)
        self.assertEqual(mock_time_sleep.call_count, 10)
        self.assertEqual(mock_process_stdout_data.call_count, 10)
        self.assertEqual(mock_process_stderr_data.call_count, 10)
        mock_logging_error.assert_called_with('Cluster is not available after 10 attempts')

    @patch("time.sleep")
    @patch.object(
        ServiceOpenSearch,
        "service_alive",
        side_effect=[requests.exceptions.ConnectionError(), requests.exceptions.ConnectionError(), True])
    @patch('test_workflow.integ_test.service.Process.stdout_data', new_callable=PropertyMock,
           return_value="test stdout_data")
    @patch('test_workflow.integ_test.service.Process.stderr_data', new_callable=PropertyMock,
           return_value="test stderr_data")
    def test_wait_for_service_suceed_on_third_attempt(
            self,
            mock_process_stderr_data: Mock,
            mock_process_stdout_data: Mock,
            mock_service_alive: Mock,
            mock_time_sleep: Mock
    ) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        service.wait_for_service()

        self.assertEqual(mock_service_alive.call_count, 3)
        self.assertEqual(mock_time_sleep.call_count, 2)
        self.assertEqual(mock_process_stdout_data.call_count, 2)
        self.assertEqual(mock_process_stderr_data.call_count, 2)

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_green_available(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"status":"green"'

        mock_get_service_response.return_value = mock_response

        self.assertTrue(service.service_alive())

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_yellow_available(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"status":"yellow"'

        mock_get_service_response.return_value = mock_response

        self.assertTrue(service.service_alive())

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_red_unavailable(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"status":"red"'

        mock_get_service_response.return_value = mock_response

        self.assertFalse(service.service_alive())

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_unavailable(self, mock_get_service_response: Mock) -> None:
        service = ServiceOpenSearch(
            self.version,
            self.distribution,
            self.additional_config,
            True,
            self.dependency_installer,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 300
        mock_response.text = '"status": "red"'

        mock_get_service_response.return_value = mock_response

        self.assertFalse(service.service_alive())
