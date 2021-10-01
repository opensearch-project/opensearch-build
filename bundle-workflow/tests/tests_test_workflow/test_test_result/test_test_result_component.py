import unittest

from test_workflow.test_result.test_result_component import \
    TestResultsComponent


class TestTestResultsComponent(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.test_test_results_component = TestResultsComponent()

    def test_test_status(self):
        test_failed = self.test_test_results_component.test_status()
        self.assertEqual(test_failed, False)


TestResultsComponent.__test__ = False  # type:ignore
