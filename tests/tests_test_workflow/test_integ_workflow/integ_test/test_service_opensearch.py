# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, PropertyMock, call, mock_open, patch

import requests

from manifests.bundle_manifest import BundleManifest
from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.test_cluster import ClusterCreationException


class ServiceOpenSearchTests(unittest.TestCase):
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

    @patch("test_workflow.integ_test.service_opensearch.Process.start")
    @patch('test_workflow.integ_test.service_opensearch.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start(self, mock_tarfile_open, mock_dump, mock_file, mock_pid, mock_process):

        dependency_installer = MagicMock()

        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            dependency_installer,
            self.save_logs,
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

        mock_process.assert_called_once_with("./opensearch-tar-install.sh", os.path.join(self.work_dir, "opensearch-1.1.0"))

        mock_dump.assert_called_once_with(self.additional_cluster_config)

        mock_file.assert_called_once_with(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a")
        mock_file.return_value.write.assert_called_once_with(mock_dump_result)

        dependency_installer.download_dist.assert_called_once_with(self.work_dir)
        mock_tarfile_open.assert_called_once_with(bundle_full_name, "r")
        mock_bundle_tar.extractall.assert_called_once_with(self.work_dir)

        self.assertEqual(mock_pid.call_count, 1)

    @patch("test_workflow.integ_test.service_opensearch.Process.start")
    @patch('test_workflow.integ_test.service_opensearch.Process.pid', new_callable=PropertyMock, return_value=12345)
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    @patch("tarfile.open")
    def test_start_security_disabled(self, mock_tarfile_open, mock_dump, mock_file, mock_pid, mock_process):

        dependency_installer = MagicMock()

        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            False,
            dependency_installer,
            self.save_logs,
            self.work_dir
        )

        bundle_full_name = "test_bundle_name"
        dependency_installer.download_dist.return_value = bundle_full_name

        mock_dump_result_for_security = MagicMock()
        mock_dump_result_for_additional_cluster_config = MagicMock()

        mock_dump.side_effect = [mock_dump_result_for_security, mock_dump_result_for_additional_cluster_config]

        mock_bundle_tar = MagicMock()
        mock_tarfile_open.return_value = mock_bundle_tar

        mock_file_hanlder_for_security = mock_open().return_value
        mock_file_hanlder_for_additional_cluster_config = mock_open().return_value

        # open() will be called twice, one for disabling security, second for additional_cluster_config
        mock_file.side_effect = [mock_file_hanlder_for_security, mock_file_hanlder_for_additional_cluster_config]\

        # call test target function
        service.start()

        mock_dump.assert_has_calls([call({"plugins.security.disabled": "true"}), call(self.additional_cluster_config)])

        mock_file.assert_has_calls(
            [call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a")],
            [call(os.path.join(self.work_dir, "opensearch-1.1.0", "config", "opensearch.yml"), "a")],
        )
        mock_file_hanlder_for_security.write.assert_called_once_with(mock_dump_result_for_security)
        mock_file_hanlder_for_additional_cluster_config.write.assert_called_once_with(mock_dump_result_for_additional_cluster_config)

    @patch("test_workflow.integ_test.service_opensearch.Process.terminate", return_value=123)
    @patch('test_workflow.integ_test.service_opensearch.Process.started', new_callable=PropertyMock, return_value=True)
    @patch('test_workflow.integ_test.service_opensearch.Process.stdout_data', new_callable=PropertyMock, return_value="test stdout_data")
    @patch('test_workflow.integ_test.service_opensearch.Process.stderr_data', new_callable=PropertyMock, return_value="test stderr_data")
    @patch("test_workflow.integ_test.service.walk")
    @patch("test_workflow.integ_test.service.TestResultData")
    def test_terminate(
        self,
        mock_test_result_data,
        mock_walk,
        mock_process_stderr_data,
        mock_process_stdout_data,
        mock_process_started,
        mock_process_terminate
    ):

        save_logs = MagicMock()

        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            save_logs,
            self.work_dir
        )

        mock_log_files = MagicMock()
        mock_walk.return_value = mock_log_files

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        service.terminate()

        mock_process_terminate.assert_called_once()

        mock_walk.assert_called_once()
        mock_test_result_data.assert_called_once_with(
            self.component_name,
            self.component_test_config,
            123,
            "test stdout_data",
            "test stderr_data",
            mock_log_files
        )

        save_logs.save_test_result_data.assert_called_once_with(mock_test_result_data_object)

    @patch("test_workflow.integ_test.service_opensearch.Process.terminate")
    @patch('test_workflow.integ_test.service_opensearch.Process.started', new_callable=PropertyMock, return_value=False)
    def test_terminate_process_not_started(self, mock_process_started, mock_process_terminate):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        service.terminate()

        mock_process_terminate.assert_not_called()
        mock_process_started.assert_called_once()

    def test_endpoint_port(self):
        service = ServiceOpenSearch(
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
        self.assertEqual(service.port(), 9200)

    def test_url_security_enabled(self):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        self.assertEqual(service.url(), "https://localhost:9200")

    def test_url_security_disabled(self):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            False,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        self.assertEqual(service.url(), "http://localhost:9200")

    @patch("requests.get")
    @patch.object(ServiceOpenSearch, "url")
    def test_get_service_response(self, mock_url, mock_requests_get):
        service = ServiceOpenSearch(
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

        mock_url.assert_called_once_with("/_cluster/health")
        mock_requests_get.assert_called_once_with(mock_url_result, verify=False, auth=('admin', 'admin'))

    # Below are tests against functions implemented in the base Service class

    @patch("time.sleep")
    @patch.object(ServiceOpenSearch, "service_alive", return_value=True)
    @patch('test_workflow.integ_test.service_opensearch.Process.stdout_data', new_callable=PropertyMock, return_value="test stdout_data")
    @patch('test_workflow.integ_test.service_opensearch.Process.stderr_data', new_callable=PropertyMock, return_value="test stderr_data")
    def test_wait_for_service_succeed_on_first_attemp(self, mock_process_stderr_data, mock_process_stdout_data, mock_service_alive, mock_time_sleep):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        service.wait_for_service()

        mock_service_alive.assert_called_once()
        mock_time_sleep.assert_not_called()
        mock_process_stdout_data.assert_not_called()
        mock_process_stderr_data.assert_not_called()

    @patch("time.sleep")
    @patch.object(ServiceOpenSearch, "service_alive", return_value=False)
    @patch('test_workflow.integ_test.service_opensearch.Process.stdout_data', new_callable=PropertyMock, return_value="test stdout_data")
    @patch('test_workflow.integ_test.service_opensearch.Process.stderr_data', new_callable=PropertyMock, return_value="test stderr_data")
    def test_wait_for_service_always_fail_without_exception(
        self,
        mock_process_stderr_data,
        mock_process_stdout_data,
        mock_service_alive,
        mock_time_sleep
    ):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        with self.assertRaises(ClusterCreationException) as ctx:
            service.wait_for_service()

        self.assertEqual(str(ctx.exception), "Cluster is not available after 10 attempts")

        self.assertEqual(mock_service_alive.call_count, 10)
        self.assertEqual(mock_time_sleep.call_count, 10)
        mock_process_stdout_data.assert_not_called()
        mock_process_stderr_data.assert_not_called()

    @patch("time.sleep")
    @patch.object(ServiceOpenSearch, "service_alive", side_effect=requests.exceptions.ConnectionError())
    @patch('test_workflow.integ_test.service_opensearch.Process.stdout_data', new_callable=PropertyMock, return_value="test stdout_data")
    @patch('test_workflow.integ_test.service_opensearch.Process.stderr_data', new_callable=PropertyMock, return_value="test stderr_data")
    def test_wait_for_service_always_fail_with_exception(
        self,
        mock_process_stderr_data,
        mock_process_stdout_data,
        mock_service_alive,
        mock_time_sleep
    ):

        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        with self.assertRaises(ClusterCreationException) as ctx:
            service.wait_for_service()

        self.assertEqual(str(ctx.exception), "Cluster is not available after 10 attempts")

        self.assertEqual(mock_service_alive.call_count, 10)
        self.assertEqual(mock_time_sleep.call_count, 10)
        self.assertEqual(mock_process_stdout_data.call_count, 10)
        self.assertEqual(mock_process_stderr_data.call_count, 10)

    @patch("time.sleep")
    @patch.object(
        ServiceOpenSearch,
        "service_alive",
        side_effect=[requests.exceptions.ConnectionError(), requests.exceptions.ConnectionError(), True])
    @patch('test_workflow.integ_test.service_opensearch.Process.stdout_data', new_callable=PropertyMock, return_value="test stdout_data")
    @patch('test_workflow.integ_test.service_opensearch.Process.stderr_data', new_callable=PropertyMock, return_value="test stderr_data")
    def test_wait_for_service_suceed_on_third_attempt(
        self,
        mock_process_stderr_data,
        mock_process_stdout_data,
        mock_service_alive,
        mock_time_sleep
    ):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        service.wait_for_service()

        self.assertEqual(mock_service_alive.call_count, 3)
        self.assertEqual(mock_time_sleep.call_count, 2)
        self.assertEqual(mock_process_stdout_data.call_count, 2)
        self.assertEqual(mock_process_stderr_data.call_count, 2)

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_green_available(self, mock_get_service_response):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"status": "green"'

        mock_get_service_response.return_value = mock_response

        self.assertTrue(service.service_alive())

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_yellow_available(self, mock_get_service_response):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.text = '"status": "yellow"'

        mock_get_service_response.return_value = mock_response

        self.assertTrue(service.service_alive())

    @patch.object(ServiceOpenSearch, "get_service_response")
    def test_service_alive_unavailable(self, mock_get_service_response):
        service = ServiceOpenSearch(
            self.bundle_manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            True,
            self.dependency_installer,
            self.save_logs,
            self.work_dir
        )

        mock_response = MagicMock()

        mock_response.status_code = 300
        mock_response.text = '"status": "red"'

        mock_get_service_response.return_value = mock_response

        self.assertFalse(service.service_alive())
