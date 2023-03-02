# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from validation_workflow.api_request import ApiTest, subprocess


class TestApiTest(unittest.TestCase):

    @patch('validation_workflow.api_request.subprocess.run')
    def test_api_get(self, mock_run: Mock) -> None:
        mock_run.return_value.stdout = b'{"key": "value"}'
        mock_run.return_value.stderr = b''
        mock_run.return_value.returncode = 0

        request_url = 'http://localhost:9200'
        api_test = ApiTest(request_url)
        status_code, response_text = api_test.api_get()

        self.assertEqual(status_code, 0)
        self.assertEqual(response_text, '{"key": "value"}')

        mock_run.assert_called_once_with(
            ['curl', request_url, '-u', 'admin:admin', '--insecure'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


if __name__ == '__main__':
    unittest.main()
