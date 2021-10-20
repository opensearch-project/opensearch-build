import unittest

from test_workflow.test_result.test_component_results import TestComponentResults


class TestTestResultsComponent(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.test_test_results_component = TestComponentResults()

    def test_test_status(self):
        test_failed = self.test_test_results_component.failed
        self.assertFalse(test_failed)
