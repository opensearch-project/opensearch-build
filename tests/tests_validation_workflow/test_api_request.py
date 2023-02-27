# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from validation_workflow.api_request import ApiTest


class TestApiTest(unittest.TestCase):

    @patch('validation_workflow.api_request.requests.get')
    def test_api_get(self, mock_get: Mock) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '{"key": "value"}'
        request_url = 'http://localhost:9200'
        api_test = ApiTest(request_url)
        status_code, response_text = api_test.api_get()
        self.assertEqual(status_code, 200)
        self.assertEqual(response_text, '{"key": "value"}')
        mock_get.assert_called_once_with(request_url, headers={'Authorization': 'Basic YWRtaW46YWRtaW4=', 'Accept': '*/*', 'Content-Type': 'application/json'}, verify=False)


if __name__ == '__main__':
    unittest.main()
