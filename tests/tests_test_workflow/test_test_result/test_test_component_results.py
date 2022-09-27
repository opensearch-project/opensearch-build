# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import unittest

from test_workflow.test_result.test_component_results import TestComponentResults


class TestTestResultsComponent(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.test_test_results_component = TestComponentResults()

    def test_test_status(self) -> None:
        test_failed = self.test_test_results_component.failed
        self.assertFalse(test_failed)
