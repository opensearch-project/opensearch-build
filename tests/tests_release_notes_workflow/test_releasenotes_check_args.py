# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import datetime
import logging
import os
import unittest
from typing import Any
from unittest.mock import patch

import pytest

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

    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", '2022-07-26'])
    def test_manifest(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().manifest.name, TestReleaseNotesCheckArgs.OPENSEARCH_MANIFEST)
        self.assertEqual(ReleaseNotesCheckArgs().date, datetime.date(2022, 7, 26))

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST])
    def test_manifest_withoutdate(self) -> None:
        with self.assertRaises(SystemExit) as cm:
            ReleaseNotesCheckArgs()
        _, err = self.capfd.readouterr()
        self.assertTrue("error: check option requires --date argument" in err)
        self.assertEqual(cm.exception.code, 2)

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", '2022-07-26', "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(ReleaseNotesCheckArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", '2022-07-26', "--output", "test.md"])
    def test_output(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().output, "test.md")
