# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import unittest
from unittest.mock import MagicMock

from test_workflow.test_result.test_result import TestResult


class TestTestResult(unittest.TestCase):
    test_result: TestResult

    def setUp(self) -> None:
        self.test_result = TestResult("sql", {"with-security": {}}, 0)

    def test_failed(self) -> None:
        failed = self.test_result.failed
        self.assertFalse(failed)

    def test_log(self) -> None:
        result = MagicMock()
        with self.assertLogs() as captured:
            self.test_result.log(result)
        self.assertEqual(len(captured), 2)
        self.assertEqual(captured.records[0].getMessage(), str(result))
