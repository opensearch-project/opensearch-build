# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

from run_bwc_test import main


class TestRunBwcTest(unittest.TestCase):
    @patch(
        "argparse._sys.argv",
        [
            "run_bwc_test.py",
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "test_manifest.yml"),
            "--paths",
            "opensearch=" + os.path.join(os.path.dirname(__file__), "..", "..", "data", "remote", "dist", "opensearch", "manifest.yml")
        ])
    @ patch("run_bwc_test.BwcTestSuite")
    def test_run_bwc_test(self, mock_bwc_suite, *mock):
        main()
        self.assertEqual(mock_bwc_suite.return_value.execute.call_count, 1)
