# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, patch

from manifests.input_manifest import InputComponentFromSource
from release_notes_workflow.release_notes_component import ReleaseNotesComponent, ReleaseNotesComponents, ReleaseNotesOpenSearch, ReleaseNotesOpenSearchPlugin


class TestReleaseNotesComponent(unittest.TestCase):

    class MyReleaseNotesComponent(ReleaseNotesComponent):

        @property
        def filename(self) -> str:
            return "release-notes-2.0.0.md"

    def setUp(self) -> None:
        self.release_notes_component = self.MyReleaseNotesComponent(MagicMock(), "2.2.0", "path")

    def test_path(self) -> None:
        self.assertEqual(self.release_notes_component.path, os.path.join("path", "release-notes"))

    @patch("os.path.exists", return_value=True)
    def test_path_exists(self, mock_path_exists: Mock) -> None:
        self.assertTrue(self.release_notes_component.path_exists())
        mock_path_exists.assert_called_with(os.path.join("path", "release-notes"))

    @patch("os.path.exists", return_value=True)
    @patch("os.listdir", return_value=['release-notes-2.0.0.md'])
    def test_exists(self, *mocks: Any) -> None:
        self.assertTrue(self.release_notes_component.exists())

    @patch("os.path.exists", return_value=False)
    @patch("os.listdir", return_value=['release-notes-2.0.0.md'])
    def test_does_not_exist(self, *mocks: Any) -> None:
        self.assertFalse(self.release_notes_component.exists())

    @patch("os.path.exists", return_value=True)
    @patch("os.listdir", return_value=['release-notes-1.0.0.md'])
    def test_does_not_exist_1x(self, *mocks: Any) -> None:
        self.assertFalse(self.release_notes_component.exists())


class TestReleaseNotesOpenSearch(unittest.TestCase):

    def setUp(self) -> None:
        self.release_notes_component = ReleaseNotesOpenSearch(MagicMock(), "2.2.0", "path")

    def test_filename(self) -> None:
        self.assertEqual(self.release_notes_component.filename, ".release-notes-2.2.0.md")


class TestReleaseNotesOpenSearchPlugin(unittest.TestCase):

    def setUp(self) -> None:
        self.release_notes_component = ReleaseNotesOpenSearchPlugin(MagicMock(), "2.2.0", "path")

    def test_filename(self) -> None:
        self.assertEqual(self.release_notes_component.filename, ".release-notes-2.2.0.0.md")


class TestComponentsReleaseNotes(unittest.TestCase):

    def test_from_component(self) -> None:
        self.assertIsInstance(ReleaseNotesComponents.from_component(MagicMock(), "2.2.0", "path"), ReleaseNotesComponent)

    def test_from_component_open_search(self) -> None:
        test_component_opensearch = InputComponentFromSource({"name": "OpenSearch", "repository": "url", "ref": "ref"})
        self.assertIsInstance(ReleaseNotesComponents.from_component(test_component_opensearch, "2.2.0", "path"), ReleaseNotesOpenSearch)

    def test_from_component_open_search_plugin(self) -> None:
        test_component_plugin = InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref"})
        self.assertIsInstance(ReleaseNotesComponents.from_component(test_component_plugin, "2.2.0", "path"), ReleaseNotesOpenSearchPlugin)
