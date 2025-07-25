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
from unittest.mock import MagicMock, patch

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

    @patch('run_releasenotes_check.ReleaseNotes')
    @patch('run_releasenotes_check.InputManifest.from_file')
    @patch('run_releasenotes_check.ReleaseNotesCheckArgs')
    def test_generate_action(self, mock_args_class, mock_from_file, mock_release_notes_class):
        """Test the generate action in run_releasenotes_check.py."""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.action = "generate"
        mock_args.manifest = ["manifests/3.2.0/opensearch-3.2.0.yml"]
        mock_args.date = datetime.date(2025, 6, 24)
        mock_args.components = None
        mock_args_class.return_value = mock_args

        mock_manifest = MagicMock()
        mock_manifest.components.select.return_value = [MagicMock()]
        mock_manifest.build.version = "3.2.0"
        mock_manifest.build.qualifier = None
        mock_from_file.return_value = mock_manifest

        mock_release_notes = MagicMock()
        mock_release_notes_class.return_value = mock_release_notes

        # Call the main function
        main()

        # Verify the interactions
        mock_from_file.assert_called_once_with("manifests/3.2.0/opensearch-3.2.0.yml")
        mock_release_notes_class.assert_called_once_with([mock_manifest], datetime.date(2025, 6, 24), "generate")
        mock_release_notes.generate.assert_called_once()

    @patch('run_releasenotes_check.ReleaseNotes')
    @patch('run_releasenotes_check.InputManifest.from_file')
    @patch('run_releasenotes_check.ReleaseNotesCheckArgs')
    def test_generate_action_with_components(self, mock_args_class, mock_from_file, mock_release_notes_class):
        """Test the generate action with specific components."""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.action = "generate"
        mock_args.manifest = ["manifests/3.2.0/opensearch-3.2.0.yml"]
        mock_args.date = datetime.date(2025, 6, 24)
        mock_args.components = ["component1", "component2"]
        mock_args_class.return_value = mock_args

        mock_manifest = MagicMock()
        mock_component1 = MagicMock()
        mock_component1.name = "component1"
        mock_component2 = MagicMock()
        mock_component2.name = "component2"
        mock_manifest.components.select.return_value = [mock_component1, mock_component2]
        mock_manifest.build.version = "3.2.0"
        mock_manifest.build.qualifier = None
        mock_from_file.return_value = mock_manifest

        mock_release_notes = MagicMock()
        mock_release_notes_class.return_value = mock_release_notes

        main()

        # Verify the interactions
        mock_from_file.assert_called_once_with("manifests/3.2.0/opensearch-3.2.0.yml")
        mock_release_notes_class.assert_called_once_with([mock_manifest], datetime.date(2025, 6, 24), "generate")
        mock_manifest.components.select.assert_called_once_with(focus=["component1", "component2"], platform='linux')
        self.assertEqual(mock_release_notes.generate.call_count, 2)

    @patch('run_releasenotes_check.ReleaseNotes')
    @patch('run_releasenotes_check.InputManifest.from_file')
    @patch('run_releasenotes_check.ReleaseNotesCheckArgs')
    def test_generate_action_with_multiple_manifests(self, mock_args_class, mock_from_file, mock_release_notes_class):
        """Test the generate action with multiple manifests."""
        mock_args = MagicMock()
        mock_args.action = "generate"
        mock_args.manifest = ["manifests/3.2.0/opensearch-3.2.0.yml", "manifests/3.2.0/opensearch-dashboards-3.2.0.yml"]
        mock_args.date = datetime.date(2025, 6, 24)
        mock_args.components = None
        mock_args_class.return_value = mock_args

        mock_manifest1 = MagicMock()
        mock_manifest1.components.select.return_value = [MagicMock()]
        mock_manifest1.build.version = "3.2.0"
        mock_manifest1.build.name = "OpenSearch"
        mock_manifest1.build.qualifier = None

        mock_manifest2 = MagicMock()
        mock_manifest2.components.select.return_value = [MagicMock()]
        mock_manifest2.build.version = "3.2.0"
        mock_manifest2.build.name = "OpenSearch Dashboards"
        mock_manifest2.build.qualifier = None

        mock_from_file.side_effect = [mock_manifest1, mock_manifest2]

        mock_release_notes = MagicMock()
        mock_release_notes_class.return_value = mock_release_notes

        main()

        # Verify the interactions
        self.assertEqual(mock_from_file.call_count, 2)
        mock_release_notes_class.assert_called_once_with([mock_manifest1, mock_manifest2], datetime.date(2025, 6, 24), "generate")
        self.assertEqual(mock_release_notes.generate.call_count, 2)
