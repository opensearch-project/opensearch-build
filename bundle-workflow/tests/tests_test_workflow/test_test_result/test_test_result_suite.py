import unittest

from test_workflow.test_result.test_result_suite import TestResultsSuite


class TestTestResultsSuite(unittest.TestCase):
    def setUp(self):
        self.test_test_results_suite = TestResultsSuite()

    def test_status(self):
        test_failed = self.test_test_results_suite.status()
        self.assertEqual(test_failed, False)


TestResultsSuite.__test__ = False  # type:ignore
