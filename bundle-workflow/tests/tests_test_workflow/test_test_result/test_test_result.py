import unittest
from unittest.mock import MagicMock

from test_workflow.test_result.test_result import TestResult


class TestTestResult(unittest.TestCase):
    def setUp(self):
        self.test_result = TestResult("sql", "with-security", 0)

    def test_log(self):
        result = MagicMock()
        with self.assertLogs() as captured:
            self.test_result.log(result)
        self.assertEqual(len(captured), 2)
        self.assertEqual(captured.records[0].getMessage(), str(result))


TestResult.__test__ = False  # type:ignore
