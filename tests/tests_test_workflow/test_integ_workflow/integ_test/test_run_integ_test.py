# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

from run_integ_test import main


class TestRunIntegTest(unittest.TestCase):
    @patch("argparse._sys.argv", ["run_integ_test.py", os.path.join(os.path.dirname(__file__), "..", "..", "data", "remote")])
    @patch("run_integ_test.DependencyInstaller")
    @patch("run_integ_test.TestSuiteResults")
    @patch("run_integ_test.IntegTestSuite")
    def test_run_integ_test(self, mock_integ_suite, mock_test_suite_results, *mock):
        mock_test_suite_results.return_value.failed.return_value = False
        main()
        self.assertEqual(mock_integ_suite.return_value.execute.call_count, 2)
