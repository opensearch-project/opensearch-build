import unittest

from test_workflow.test_result.test_suite_results import TestSuiteResults


class TestTestResultsSuite(unittest.TestCase):
    def setUp(self):
        self.test_test_results_suite = TestSuiteResults()

    def test_status(self):
        test_failed = self.test_test_results_suite.failed()
        self.assertFalse(test_failed)
