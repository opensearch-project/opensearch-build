import logging
import os
import unittest
from unittest.mock import patch

from test_workflow.test_args import TestArgs


class TestTestArgs(unittest.TestCase):

    ARGS_PY = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "../../src/run_bwc_test.py")
    )

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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_s3_bucket(self):
        self.assertEqual(TestArgs().s3_bucket, "xyz")

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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_opensearch_version(self):
        self.assertEqual(TestArgs().opensearch_version, "1.1.0")

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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_build_id(self):
        self.assertEqual(TestArgs().build_id, 30)

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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_architecture(self):
        self.assertEqual(TestArgs().architecture, "x64")

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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
            "--component",
            "xyz",
        ],
    )
    def test_test_run_id(self):
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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
        ],
    )
    def test_verbose_default(self):
        self.assertTrue(TestArgs().logging_level, logging.INFO)

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
            "--architecture",
            "x64",
            "--test-run-id",
            "6",
            "--verbose",
        ],
    )
    def test_verbose_true(self):
        self.assertTrue(TestArgs().logging_level, logging.DEBUG)
