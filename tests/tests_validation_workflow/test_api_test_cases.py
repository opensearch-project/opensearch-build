# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from validation_workflow.api_test_cases import ApiTestCases


class TestTestCases(unittest.TestCase):
    @patch('validation_workflow.api_test_cases.ApiTest.api_get')
    def test_opensearch(self, mock_api_get: Mock) -> None:
        mock_api_get.return_value = (200, 'green')
        testcases = ApiTestCases()
        result = testcases.test_apis(['opensearch'])

        self.assertEqual(result[1], 'There are 3/3 test cases Pass')
        self.assertEqual(mock_api_get.call_count, 3)

    @patch('validation_workflow.api_test_cases.ApiTest.api_get')
    def test_both(self, mock_api_get: Mock) -> None:
        mock_api_get.return_value = (200, 'green')
        testcases = ApiTestCases()
        result = testcases.test_apis(['opensearch', 'opensearch-dashboards'])

        self.assertEqual(result[1], 'There are 4/4 test cases Pass')
        self.assertEqual(mock_api_get.call_count, 4)


if __name__ == '__main__':
    unittest.main()
