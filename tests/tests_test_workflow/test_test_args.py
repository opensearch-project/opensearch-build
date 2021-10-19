import logging
import os
import unittest
from unittest.mock import patch

from test_workflow.test_args import TestArgs


class TestTestArgs(unittest.TestCase):

    ARGS_PY = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "run_bwc_test.py"))

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_required_arguments(self):
        self.assertEqual(TestArgs().s3_bucket, "xyz")
        self.assertEqual(TestArgs().opensearch_version, "1.1.0")
        self.assertEqual(TestArgs().build_id, 30)
        self.assertEqual(TestArgs().platform, "linux")
        self.assertEqual(TestArgs().architecture, "x64")
        self.assertEqual(TestArgs().test_run_id, 6)

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "xyz",
            "--test-run-id",
            "6",
        ],
    )
    def test_invalid_architecture(self):
        with self.assertRaises(SystemExit):
            self.assertEqual(TestArgs().architecture, "invalid")

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "xyz",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_invalid_platform(self):
        with self.assertRaises(SystemExit):
            self.assertEqual(TestArgs().platform, "invalid")

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1111",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_invalid_version(self):
        with self.assertRaises(ValueError) as context:
            TestArgs().CheckSemanticVersion
        self.assertEqual("Invalid version number: 1111", str(context.exception))

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_keep_default(self):
        self.assertFalse(TestArgs().keep)

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
            "--keep",
        ],
    )
    def test_keep_true(self):
        self.assertTrue(TestArgs().keep)

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_verbose_default(self):
        self.assertEqual(TestArgs().logging_level, logging.INFO)

    @patch(
        "argparse._sys.argv",
        [
            ARGS_PY,
            "--s3-bucket",
            "xyz",
            "--opensearch-version",
            "1.1.0",
            "--build-id",
            "30",
            "--platform",
            "linux",
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
            "--verbose",
        ],
    )
    def test_verbose_true(self):
        self.assertTrue(TestArgs().logging_level, logging.DEBUG)
