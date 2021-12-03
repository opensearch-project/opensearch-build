# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import call, patch

import pytest

from run_ci import main


class TestRunCi(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_ci.py", "--help"])
    def test_usage(self):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(os.path.dirname(__file__), "../manifests/1.1.1/opensearch-1.1.1.yml"))

    @patch("argparse._sys.argv", ["run_ci.py", OPENSEARCH_MANIFEST])
    @patch("ci_workflow.ci_input_manifest.TemporaryDirectory")
    @patch("ci_workflow.ci_input_manifest.CiCheckLists.from_component")
    def test_main(self, mock_lists, mock_temp, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertNotEqual(mock_lists.call_count, 0)
        self.assertEqual(mock_lists.return_value.checkout.call_count, mock_lists.call_count)
        self.assertEqual(mock_lists.return_value.check.call_count, mock_lists.call_count)

    OPENSEARCH_TEST_MANIFEST = os.path.realpath(os.path.join(os.path.dirname(__file__), "../manifests/1.3.0/opensearch-1.3.0-test.yml"))

    @patch("argparse._sys.argv", ["run_ci.py", OPENSEARCH_TEST_MANIFEST])
    @patch("logging.info")
    def test_main_test_manifest(self, mock_logging, *mocks):
        main()
        mock_logging.assert_has_calls([
            call("TestManifest schema validation succeeded"),
            call("Done.")
        ])

    OPENSEARCH_TEST_MANIFEST_NOT_EXIST = os.path.realpath(os.path.join(os.path.dirname(__file__), "../manifests/1.4.0/opensearch-1.3.0-test.yml"))

    @patch("argparse._sys.argv", ["run_ci.py", OPENSEARCH_TEST_MANIFEST_NOT_EXIST])
    def test_main_test_manifest_empty(self, *mocks):
        with self.assertRaises(SystemExit):
            main()
