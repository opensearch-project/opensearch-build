# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import unittest
from unittest.mock import patch

from sign_workflow.sign_args import SignArgs


class TestSignArgs(unittest.TestCase):

    SIGN_PY = "./src/run_sign.py"

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "1.1.0",
            "opensearch-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST])
    def test_verbose_default(self) -> None:
        self.assertEqual(SignArgs().logging_level, logging.INFO)

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST])
    def test_sigtype_default(self) -> None:
        self.assertEqual(SignArgs().sigtype, ".asc")

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST, "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(SignArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST])
    def test_component_default(self) -> None:
        self.assertIsNone(SignArgs().components)

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_component(self) -> None:
        self.assertEqual(SignArgs().components, ["xyz"])

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST, "--component", "foo", "bar"])
    def test_components(self) -> None:
        self.assertEqual(SignArgs().components, ["foo", "bar"])

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST])
    def test_platform_default(self) -> None:
        self.assertEqual(SignArgs().platform, "linux")

    @patch("argparse._sys.argv", [SIGN_PY, OPENSEARCH_MANIFEST, "--platform", "windows"])
    def test_platform_windows(self) -> None:
        self.assertEqual(SignArgs().platform, "windows")
