# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from manifests.test_manifest import TestManifest
from run_integ_test import main
from test_workflow.integ_test.integ_test_runners import IntegTestRunners
from test_workflow.test_args import TestArgs


class TestRunIntegTest(unittest.TestCase):
    @patch(
        "argparse._sys.argv",
        [
            "run_integ_test.py",
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "test_manifest.yml"),
            "--paths",
            "opensearch=" + os.path.join(os.path.dirname(__file__), "..", "..", "data", "remote")
        ])
    def test_run_integ_test(self, *mock):

        mock_runner = MagicMock()
        mock_result = MagicMock()
        mock_result.failed.return_value = False

        mock_runner.run.return_value = mock_result
        mock_from_test_manifest = MagicMock()
        mock_from_test_manifest.return_value = mock_runner
        IntegTestRunners.from_test_manifest = mock_from_test_manifest

        main()

        args, kwargs = mock_from_test_manifest.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertIsInstance(args[0], TestArgs)
        self.assertIsInstance(args[1], TestManifest)

        mock_result.log.assert_called_once_with()
        mock_result.failed.assert_called_once_with()
