# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, call, mock_open, patch

from test_workflow.test_recorder.test_recorder import LocalClusterLogs, TestRecorder, TestResultsLogs


@patch("os.makedirs")
@patch("os.chdir")
class TestTestRecorder(unittest.TestCase):

    def setUp(self) -> None:
        self.local_cluster_logs = MagicMock()
        self.remote_cluster_logs = MagicMock()
        self.test_results_logs = MagicMock()

    @patch("test_workflow.test_recorder.test_recorder.TestResultsLogs")
    @patch("test_workflow.test_recorder.test_recorder.RemoteClusterLogs")
    @patch("test_workflow.test_recorder.test_recorder.LocalClusterLogs")
    def test_get_file_path_url(self, mock_local_cluster_logs: Mock, mock_remote_cluster_logs: Mock, mock_test_results_logs: Mock, *mock: Any) -> None:
        test_recorder_with_url = TestRecorder(
            "1234",
            "integ-test",
            "working-directory",
            "https://ci.opensearch.org/ci/dbc/integ-test/"
        )
        file_path_with_url = test_recorder_with_url._get_file_path("https://ci.opensearch.org/ci/dbc/integ-test/", "sql", "with-security")
        self.assertEqual(file_path_with_url, "https://ci.opensearch.org/ci/dbc/integ-test/test-results/1234/integ-test/sql/with-security")

    @patch("test_workflow.test_recorder.test_recorder.TestResultsLogs")
    @patch("test_workflow.test_recorder.test_recorder.RemoteClusterLogs")
    @patch("test_workflow.test_recorder.test_recorder.LocalClusterLogs")
    def test_get_file_path_local(self, mock_local_cluster_logs: Mock, mock_remote_cluster_logs: Mock, mock_test_results_logs: Mock, *mock: Any) -> None:
        test_recorder_no_url = TestRecorder(
            "1234",
            "integ-test",
            "working-directory"
        )
        file_path_no_url = test_recorder_no_url._get_file_path("", "sql", "with-security")
        self.assertEqual(file_path_no_url, os.path.realpath(os.path.join("working-directory", "1234", "integ-test", "sql", "with-security")))

    @patch("builtins.open", new_callable=mock_open)
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    @patch("test_workflow.test_recorder.test_recorder.TestResultsLogs")
    @patch("test_workflow.test_recorder.test_recorder.RemoteClusterLogs")
    @patch("test_workflow.test_recorder.test_recorder.LocalClusterLogs")
    def test_generate_yml(self, mock_local_cluster_logs: Mock, mock_remote_cluster_logs: Mock, mock_test_results_logs: Mock, mock_test_recorder: Mock, mock_open: Mock, *mock: Any) -> None:
        test_recorder = TestRecorder(
            "1234",
            "integ-test",
            "working-directory"
        )

        mock_test_result_data = MagicMock()

        mock_test_result_data.component_name = "sql"
        mock_test_result_data.component_test_config = "with-security"
        mock_test_result_data.exit_code = 0

        mock_file_path = MagicMock()
        mock_file_path.return_value = "working-directory"
        test_recorder._get_file_path = mock_file_path   # type: ignore

        mock_list_files = MagicMock()
        mock_list_files.return_value = ["file1", "file2"]
        test_recorder._get_list_files = mock_list_files  # type: ignore

        mock_update_path = MagicMock()
        mock_update_path.return_value = ["working-directory/file1", "working-directory/file2"]
        test_recorder._update_absolute_file_paths = mock_update_path    # type: ignore

        component_yml = test_recorder._generate_yml(mock_test_result_data, "working-directory")

        mock_open.assert_has_calls([call(os.path.join("working-directory", "sql.yml"), 'w', encoding='utf-8')])
        mock_file_path.assert_called_once_with(None, "sql", "with-security")
        mock_list_files.assert_called()
        mock_update_path.assert_called()
        self.assertEqual(component_yml, os.path.realpath("sql.yml"))

    @patch("test_workflow.test_recorder.test_recorder.TestResultsLogs")
    @patch("test_workflow.test_recorder.test_recorder.RemoteClusterLogs")
    @patch("test_workflow.test_recorder.test_recorder.LocalClusterLogs")
    def test_update_absolute_file_paths(self, mock_local_cluster_logs: Mock, mock_remote_cluster_logs: Mock, mock_test_results_logs: Mock, *mock: Any) -> None:
        test_recorder = TestRecorder(
            "1234",
            "integ-test",
            "working-directory",
            "https://ci.opensearch.org/ci/dbc/integ-test/"
        )
        file_path = test_recorder._update_absolute_file_paths(["file1", "file2"], "working-directory", "sub-directory")
        self.assertEqual(file_path, [os.path.join("working-directory", "sub-directory", "file1"), os.path.join("working-directory", "sub-directory", "file2")])

    @patch("os.walk")
    @patch("test_workflow.test_recorder.test_recorder.TestResultsLogs")
    @patch("test_workflow.test_recorder.test_recorder.RemoteClusterLogs")
    @patch("test_workflow.test_recorder.test_recorder.LocalClusterLogs")
    def test_get_list_files(self, mock_local_cluster_logs: Mock, mock_remote_cluster_logs: Mock, mock_test_results_logs: Mock, mock_os_walk: Mock, *mock: Any) -> None:
        test_recorder = TestRecorder(
            "1234",
            "integ-test",
            "working-directory",
            "https://ci.opensearch.org/ci/dbc/integ-test/"
        )
        mock_os_walk.return_value = [("mock_dir", (), ("file1", "file2"))]
        list_files = test_recorder._get_list_files("mock_dir")
        self.assertEqual(list_files, ["file1", "file2"])

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_std_files(self, mock_open: Mock, *mock: Any) -> None:
        test_recorder = TestRecorder(
            "1234",
            "integ-test",
            "working-directory"
        )
        test_recorder._generate_std_files("mock_stdout", "mock_stderr", "mock_path")

        mock_file = MagicMock()
        mock_open.return_value = mock_file

        mock_open.assert_has_calls([call(os.path.join("mock_path", "stdout.txt"), 'w', encoding='utf-8')])
        mock_open.assert_has_calls([call(os.path.join("mock_path", "stderr.txt"), 'w', encoding='utf-8')])

        mock_open.assert_has_calls([call().write("mock_stdout")])
        mock_open.assert_has_calls([call().write("mock_stderr")])


class TestLocalClusterLogs(unittest.TestCase):

    def test(self) -> None:
        mock_parent_class = MagicMock()

        mock_parent_class._create_base_folder_structure.return_value = "test_base"

        mock_parent_class._copy_log_files = MagicMock()

        logs = LocalClusterLogs(mock_parent_class)

        mock_test_result_data = MagicMock()

        dest_directory = os.path.join("test_base", "local-cluster-logs/id-0")

        source_file_1 = os.path.join("dir", "opensearch_index_indexing_slowlog.log")
        source_file_2 = os.path.join("dir", "opensearch_deprecation.json")

        mock_test_result_data.log_files = {
            "slowlog": source_file_1,
            "deprecation-log": source_file_2,
        }
        mock_test_result_data.component_name = "sql"
        mock_test_result_data.component_test_config = "with-security"

        logs.save_test_result_data(mock_test_result_data)

        mock_parent_class._copy_log_files.assert_called_once_with(mock_test_result_data.log_files, dest_directory)


class TestTestResultsLogs(unittest.TestCase):

    def test(self) -> None:
        mock_parent_class = MagicMock()

        mock_parent_class._create_base_folder_structure.return_value = "test_base"

        mock_parent_class._copy_log_files = MagicMock()

        logs = TestResultsLogs(mock_parent_class)

        mock_test_result_data = MagicMock()

        dest_directory = "test_base"

        source_file_1 = "stdout.txt"
        source_file_2 = "stderr.txt"

        mock_test_result_data.log_files = {
            source_file_1,
            source_file_2
        }
        mock_test_result_data.component_name = "sql"
        mock_test_result_data.component_test_config = "with-security"

        logs.save_test_result_data(mock_test_result_data)

        mock_parent_class._copy_log_files.assert_called_once_with(mock_test_result_data.log_files, dest_directory)

        logs.generate_component_yml(mock_test_result_data)

        mock_parent_class._generate_yml.assert_called_once_with(mock_test_result_data, dest_directory)
