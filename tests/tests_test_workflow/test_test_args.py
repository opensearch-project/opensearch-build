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

    @patch("argparse._sys.argv", [ARGS_PY, PATH])
    def test_defaults(self):
        test_args = TestArgs()
        self.assertEqual(test_args.path, os.path.realpath(self.PATH))
        self.assertIsNotNone(test_args.test_run_id)
        self.assertIsNone(test_args.component)
        self.assertFalse(test_args.keep)
        self.assertEqual(test_args.logging_level, logging.INFO)

    @patch("argparse._sys.argv", [ARGS_PY, PATH, "--test-run-id", "6"])
    def test_run_id(self):
        self.assertEqual(TestArgs().test_run_id, 6)

    @patch("argparse._sys.argv", [ARGS_PY, PATH, "--verbose"])
    def test_verbose(self):
        self.assertEqual(TestArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [ARGS_PY, 'https://ci.opensearch.org/x/y', "--verbose"])
    def test_url(self):
        self.assertEqual(TestArgs().path, 'https://ci.opensearch.org/x/y')
