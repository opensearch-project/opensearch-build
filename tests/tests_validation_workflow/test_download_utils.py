# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from system.temporary_directory import TemporaryDirectory
from validation_workflow.download_utils import DownloadUtils


class TestDownloadUtils(unittest.TestCase):
    @patch('requests.head')
    def test_is_url_valid_true(self, mock_head: Mock) -> None:
        mock_head.return_value.status_code = 302
        url = "https://opensearch.org/release/2.11.0/opensearch-2.11.0-linux-arm64.tar.gz"
        result = DownloadUtils.is_url_valid(url)
        self.assertTrue(result)

        mock_head.return_value.status_code = 200
        result = DownloadUtils.is_url_valid(url)
        self.assertTrue(result)

    @patch('requests.head')
    def test_is_url_valid_false(self, mock_head: Mock) -> None:
        mock_head.return_value.status_code = 404

        url = "https://opensearch.org/release/2.11.0/opensearch-2.11.0-linux-arm64.tar.gz"
        result = DownloadUtils.is_url_valid(url)

        self.assertFalse(result)

    @patch('requests.get')
    @patch('builtins.open', create=True)
    @patch('os.mkdir', return_value=None)
    def test_download(self, mock_mkdir: Mock, mock_open: Mock, mock_get: Mock) -> None:
        mock_get.return_value.content = "exists"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        tmp_dir = TemporaryDirectory()

        url = "https://opensearch.org/release/2.11.0/opensearch-2.11.0-linux-arm64.tar.gz"
        result = DownloadUtils.download(url, tmp_dir)

        self.assertTrue(result)
        mock_open.assert_called_once()
        mock_get.assert_called_once()
