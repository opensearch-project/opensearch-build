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
from run_releasenotes_check import main


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

    DASHBOARDS_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "templates",
            "opensearch-dashboards",
            "1.x",
            "osd-template-1.1.0.yml",
        )
    )

    DASHBOARDS_MANIFEST_2_0 = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "templates",
            "opensearch-dashboards",
            "2.x",
            "osd-template-2.0.0.yml",
        )
    )

    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", '2022-07-26'])
    def test_manifest(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().manifest[0].name, TestReleaseNotesCheckArgs.OPENSEARCH_MANIFEST)
        self.assertEqual(ReleaseNotesCheckArgs().date, datetime.date(2022, 7, 26))

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "compile", OPENSEARCH_MANIFEST, DASHBOARDS_MANIFEST, "--date", '2022-07-26'])
    def test_manifest_compile(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().manifest[0].name, TestReleaseNotesCheckArgs.OPENSEARCH_MANIFEST)
        self.assertEqual(ReleaseNotesCheckArgs().manifest[1].name, TestReleaseNotesCheckArgs.DASHBOARDS_MANIFEST)
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

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "compile", OPENSEARCH_MANIFEST, "--date", '2022-07-26', "--verbose"])
    def test_verbose_true_compile(self) -> None:
        self.assertTrue(ReleaseNotesCheckArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "check", OPENSEARCH_MANIFEST, "--date", '2022-07-26', "--output", "test.md"])
    def test_output(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().output, "test.md")

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "compile", OPENSEARCH_MANIFEST, "--date", '2022-07-26', "--output", "test.md"])
    def test_output_compile(self) -> None:
        self.assertEqual(ReleaseNotesCheckArgs().output, "test.md")

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "compile", OPENSEARCH_MANIFEST, DASHBOARDS_MANIFEST_2_0])
    def test_error_on_different_release_version_manifest(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            main()
        assert str(exc_info.value) == 'OS and OSD manifests must be provided for the same release version'

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "compile", OPENSEARCH_MANIFEST, OPENSEARCH_MANIFEST])
    def test_error_on_same_manifest_product_name(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            main()
        assert str(exc_info.value) == 'Both manifests are for the same product, OS and OSD manifests must be provided'

    @patch("argparse._sys.argv", [RELEASE_NOTES_CHECK_PY, "compile", OPENSEARCH_MANIFEST, OPENSEARCH_MANIFEST, OPENSEARCH_MANIFEST])
    def test_error_on_more_than_two_manifests(self, *mocks: Any) -> None:
        with pytest.raises(ValueError) as exc_info:
            main()
        assert str(exc_info.value) == 'Only two manifests, OS and OSD, can be provided'
