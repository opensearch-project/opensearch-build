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
        mock_api_get.side_effect = [
            (200, '"number" : "1.3.0"'),
            (200, ''),
            (200, 'green'),
        ]
        testcases = ApiTestCases()
        result = testcases.test_apis("1.3.0", ['opensearch'], True)

        self.assertEqual(result[1], 'There are 3/3 test cases Pass')
        self.assertEqual(mock_api_get.call_count, 3)

    @patch('validation_workflow.api_test_cases.ApiTest.api_get')
    def test_both(self, mock_api_get: Mock) -> None:
        mock_api_get.side_effect = [
            (200, '"number" : "2.1.1"'),
            (200, ''),
            (200, 'green'),
            (200, '"number":"2.1.1"'),
        ]
        testcases = ApiTestCases()
        result = testcases.test_apis("2.1.1", ['opensearch', 'opensearch-dashboards'], True)

        self.assertEqual(result[1], 'There are 4/4 test cases Pass')
        self.assertEqual(mock_api_get.call_count, 4)

    @patch('validation_workflow.api_test_cases.ApiTest.api_get')
    def test_without_security(self, mock_api_get: Mock) -> None:
        mock_api_get.side_effect = [
            (200, '"number" : "1.3.0"'),
            (200, ''),
            (200, 'green'),
        ]
        testcases = ApiTestCases()
        result = testcases.test_apis("1.3.0", ['opensearch'], False)

        self.assertEqual(result[1], 'There are 3/3 test cases Pass')
        self.assertEqual(mock_api_get.call_count, 3)

    @patch('validation_workflow.api_test_cases.ApiTest.api_get')
    def test_dashboards_status_200_with_wrong_content_fails(self, mock_api_get: Mock) -> None:
        # #5117: a 200 does not mean OSD actually served the expected build;
        # validate_string must match too, or a broken page behind a 200
        # silently passed, as it did before this fix.
        mock_api_get.side_effect = [
            (200, '"number" : "2.1.1"'),
            (200, ''),
            (200, 'green'),
            (200, '<html>plugin error page</html>'),
        ]
        testcases = ApiTestCases()
        result = testcases.test_apis("2.1.1", ['opensearch', 'opensearch-dashboards'], True)

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], 'There are 3/4 test cases Pass')

    @patch('validation_workflow.api_test_cases.ApiTest.api_get')
    def test_opensearch_root_200_with_wrong_version_fails(self, mock_api_get: Mock) -> None:
        # Same regression on the OpenSearch-root check: a 200 whose body
        # carries a different build's version number should not pass.
        mock_api_get.side_effect = [
            (200, '"number" : "1.2.9"'),
            (200, ''),
            (200, 'green'),
        ]
        testcases = ApiTestCases()
        result = testcases.test_apis("1.3.0", ['opensearch'], True)

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], 'There are 2/3 test cases Pass')


if __name__ == '__main__':
    unittest.main()
