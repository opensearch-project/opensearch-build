# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import unittest
from unittest.mock import patch

from releasenotes_check_workflow.releasenotes_check_args import ReleaseNotesCheckArgs


class TestCheckoutArgs(unittest.TestCase):

    RELEASE_NOTES_CHECK_PY = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "run_releasenotes_check.py"))

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
    gitLogDate = '2022-07-26'

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, OPENSEARCH_MANIFEST, "--gitlogdate", gitLogDate])
    def test_manifest(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().manifest.name, TestCheckoutArgs.OPENSEARCH_MANIFEST)
        self.assertEqual(ReleaseNotesCheckArgs().gitlogdate, TestCheckoutArgs.gitLogDate)

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, OPENSEARCH_MANIFEST, "--gitlogdate", gitLogDate, "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(ReleaseNotesCheckArgs().logging_level, logging.DEBUG)
