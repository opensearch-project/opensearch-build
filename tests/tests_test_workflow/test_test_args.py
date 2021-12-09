import logging
import os
import unittest
from unittest.mock import patch

from test_workflow.test_args import TestArgs


class TestTestArgs(unittest.TestCase):

    ARGS_PY = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "run_bwc_test.py"
        )
    )

    PATH = os.path.join(
        os.path.dirname(__file__), "data"
    )

    TEST_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__), "data", "test_manifest.yml"
    )

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH])
    def test_opensearch_default_opensearch_dashboards_default(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_path, os.getcwd())
        self.assertEqual(test_args.opensearch_dashboards_path, os.getcwd())

        self.assertIsNotNone(test_args.test_run_id)
        self.assertIsNone(test_args.component)
        self.assertFalse(test_args.keep)
        self.assertEqual(test_args.logging_level, logging.INFO)
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch=" + PATH])
    def test_opensearch_file_opensearch_dashboards_default(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_path, os.path.realpath(self.PATH))
        self.assertEqual(test_args.opensearch_dashboards_path, os.getcwd())

        self.assertIsNotNone(test_args.test_run_id)
        self.assertIsNone(test_args.component)
        self.assertFalse(test_args.keep)
        self.assertEqual(test_args.logging_level, logging.INFO)
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch-dashboards=" + PATH])
    def test_opensearch_default_opensearch_dashboards_file(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_dashboards_path, os.path.realpath(self.PATH))
        self.assertEqual(test_args.opensearch_path, os.getcwd())

        self.assertIsNotNone(test_args.test_run_id)
        self.assertIsNone(test_args.component)
        self.assertFalse(test_args.keep)
        self.assertEqual(test_args.logging_level, logging.INFO)
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch-dashboards=" + PATH, "opensearch=" + PATH])
    def test_opensearch_file_opensearch_dashboards_file(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_dashboards_path, os.path.realpath(self.PATH))
        self.assertEqual(test_args.opensearch_path, os.path.realpath(self.PATH))

        self.assertIsNotNone(test_args.test_run_id)
        self.assertIsNone(test_args.component)
        self.assertFalse(test_args.keep)
        self.assertEqual(test_args.logging_level, logging.INFO)
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @ patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch=" + PATH, "--test-run-id", "6"])
    def test_run_id(self):
        test_args = TestArgs()
        self.assertEqual(test_args.test_run_id, 6)
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @ patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch=" + PATH, "--verbose"])
    def test_verbose(self):
        test_args = TestArgs()
        self.assertEqual(test_args.logging_level, logging.DEBUG)
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @ patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch=https://ci.opensearch.org/x/y", "--verbose"])
    def test_opensearch_url_opensearch_dashboards_default(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_path, "https://ci.opensearch.org/x/y")
        self.assertEqual(test_args.opensearch_dashboards_path, os.getcwd())
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @ patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--paths", "opensearch-dashboards=https://ci.opensearch.org/x/y", "--verbose"])
    def test_opensearch_default_opensearch_dashboards_url(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_dashboards_path, "https://ci.opensearch.org/x/y")
        self.assertEqual(test_args.opensearch_path, os.getcwd())
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @ patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            TEST_MANIFEST_PATH,
            "--paths",
            "opensearch=https://ci.opensearch.org/x/y",
            "opensearch-dashboards=https://ci.opensearch.org/x/y/dashboards",
            "--verbose"
        ]
    )
    def test_opensearch_url_opensearch_dashboards_url(self):
        test_args = TestArgs()
        self.assertEqual(test_args.opensearch_path, "https://ci.opensearch.org/x/y")
        self.assertEqual(test_args.opensearch_dashboards_path, "https://ci.opensearch.org/x/y/dashboards")
        self.assertEqual(test_args.test_manifest_path, self.TEST_MANIFEST_PATH)
