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

from assemble_workflow.assemble_args import AssembleArgs


class TestAssembleArgs(unittest.TestCase):

    ASSEMBLE_PY = "./src/run_assembly.py"

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "templates",
            "opensearch",
            "1.x",
            "os-template-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", [ASSEMBLE_PY, OPENSEARCH_MANIFEST])
    def test_manifest(self) -> None:
        self.assertEqual(AssembleArgs().manifest.name, TestAssembleArgs.OPENSEARCH_MANIFEST)

    @patch("argparse._sys.argv", [ASSEMBLE_PY, OPENSEARCH_MANIFEST])
    def test_keep_default(self) -> None:
        self.assertFalse(AssembleArgs().keep)

    @patch("argparse._sys.argv", [ASSEMBLE_PY, OPENSEARCH_MANIFEST, "--keep"])
    def test_keep_true(self) -> None:
        self.assertTrue(AssembleArgs().keep)

    @patch("argparse._sys.argv", [ASSEMBLE_PY, OPENSEARCH_MANIFEST])
    def test_verbose_default(self) -> None:
        self.assertEqual(AssembleArgs().logging_level, logging.INFO)

    @patch("argparse._sys.argv", [ASSEMBLE_PY, OPENSEARCH_MANIFEST, "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(AssembleArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [ASSEMBLE_PY, OPENSEARCH_MANIFEST, "--base-url", "url"])
    def test_base_url(self) -> None:
        self.assertEqual(AssembleArgs().base_url, "url")
