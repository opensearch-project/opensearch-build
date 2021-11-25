# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from unittest.mock import MagicMock, call, patch

from test_workflow.test_recorder.test_recorder import TestRecorder


class LocalClusterLogsTests(unittest.TestCase):

    @patch("shutil.copyfile")
    def test(self, mock_copyfile):

        mock_parent_class = MagicMock()

        mock_parent_class._create_base_folder_structure.return_value = "test_base"

        logs = TestRecorder.LocalClusterLogs(mock_parent_class)

        mock_test_result_data = MagicMock()

        mock_test_result_data.log_files = [
            (
                "dir",
                [],
                [
                    "opensearch_index_indexing_slowlog.log",
                    "opensearch_deprecation.json"
                ]
            )
        ]

        dest_directory = os.path.join("test_base", "local-cluster-logs")

        dest_file_1 = os.path.join(dest_directory, "opensearch_index_indexing_slowlog.log")
        dest_file_2 = os.path.join(dest_directory, "opensearch_deprecation.json")

        source_file_1 = os.path.join("dir", "opensearch_index_indexing_slowlog.log")
        source_file_2 = os.path.join("dir", "opensearch_deprecation.json")

        logs.save_test_result_data(mock_test_result_data)

        mock_copyfile.assert_has_calls(
            [call(source_file_1, dest_file_1)],
            [call(source_file_2, dest_file_2)]
        )
