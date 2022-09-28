# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from unittest.mock import MagicMock

from test_workflow.test_recorder.test_recorder import LocalClusterLogs


class TestLocalClusterLogs(unittest.TestCase):

    def test(self) -> None:
        mock_parent_class = MagicMock()

        mock_parent_class._create_base_folder_structure.return_value = "test_base"

        mock_parent_class._copy_log_files = MagicMock()

        logs = LocalClusterLogs(mock_parent_class)

        mock_test_result_data = MagicMock()

        dest_directory = os.path.join("test_base", "local-cluster-logs")

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
