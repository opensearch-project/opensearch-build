# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import datetime
import os
import unittest
from typing import Any
from unittest.mock import patch

import pytest

from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from run_releasenotes_check import main


class TestRunReleaseNotesCheck(unittest.TestCase):

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "manifests",
            "templates",
            "opensearch",
            "2.x",
            "manifest.yml"
        )
    )

    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_releasenotes_check.py", "--help"])
    def test_usage(self) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_releasenotes_check.py", "check", OPENSEARCH_MANIFEST, "--date", "2022-07-26"])
    @patch('subprocess.check_call')
    @patch("run_releasenotes_check.ReleaseNotes")
    @patch("run_releasenotes_check.main", return_value=0)
    def test_main(self, *mocks: Any) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().action, 'check')
        self.assertEqual(ReleaseNotesCheckArgs().date, datetime.date(2022, 7, 26))
        self.assertTrue(ReleaseNotesCheckArgs().manifest)

    @patch('subprocess.check_call')
    @patch("argparse._sys.argv", ["run_releasenotes_check.py", "check", OPENSEARCH_MANIFEST, "--date", "2022-07-26", "--output", "test.md"])
    @patch("run_releasenotes_check.ReleaseNotes")
    @patch("run_releasenotes_check.main", return_value=0)
    def test_main_with_save(self, *mocks: Any) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().output, "test.md")
