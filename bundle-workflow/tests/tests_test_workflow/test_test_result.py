import unittest

from test_workflow.test_result import TestResult


class TestTestResult(unittest.TestCase):
    def setUp(self):
        self.test_result = TestResult()

    def test_append_result(self):
        self.test_result.final_result.append(("alerting", "with-security", 1))
        self.test_result.final_result.append(("alerting", "without-security", 0))
        self.assertListEqual(
            self.test_result.final_result,
            [("alerting", "with-security", 1), ("alerting", "without-security", 0)],
        )

    def test_generate_summary_report(self):
        test_failed = self.test_result.generate_summary_report()
        self.assertEqual(test_failed, False)
