# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import datetime
import logging
import os
import unittest
from unittest.mock import patch

from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs


class TestReleaseNotesCheckArgs(unittest.TestCase):

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

    gitLogDateAssert = datetime.datetime.strptime(gitLogDate, "%Y-%m-%d").date()

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", gitLogDate])
    def test_manifest(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().manifest.name, TestReleaseNotesCheckArgs.OPENSEARCH_MANIFEST)
        self.assertEqual(ReleaseNotesCheckArgs().date, TestReleaseNotesCheckArgs.gitLogDateAssert)

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", gitLogDate, "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(ReleaseNotesCheckArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", gitLogDate, "--verbose", "--save"])
    def test_verbose_true_withsave(self) -> None:
        self.assertTrue(ReleaseNotesCheckArgs().logging_level, logging.DEBUG)
