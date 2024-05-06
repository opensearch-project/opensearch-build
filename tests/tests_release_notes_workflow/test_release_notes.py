# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import patch

from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes import ReleaseNotes


class TestReleaseNotes(unittest.TestCase):

    def setUp(self) -> None:
        MANIFESTS = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
        )
        OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(MANIFESTS, "opensearch-test-main.yml"))
        self.manifest_file = InputManifest.from_file(open(OPENSEARCH_MANIFEST))
        self.build_version = self.manifest_file.build.version
        self.release_notes = ReleaseNotes([self.manifest_file], "2022-07-26", "compile")
        self.component = InputComponentFromSource({"name": "OpenSearch-test", "repository": "url", "ref": "ref"})

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check(self, *mocks: Any) -> None:
        self.assertEqual(self.release_notes.check(self.component, self.build_version), ['OpenSearch-test', '[ref]', None, None, False, None])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check_with_manifest(self, *mocks: Any) -> None:
        component = next(self.manifest_file.components.select())
        if type(component) is InputComponentFromSource:
            self.assertIsInstance(component, InputComponentFromSource)
            self.assertEqual(self.release_notes.check(component, self.build_version), ['OpenSearch-test', '[main]', None, None, False, None])

    @patch('release_notes_workflow.release_notes.ReleaseNotes.check', return_value=['OpenSearch-test', '[main]', 'ee26e01', '2022-08-18', False, None])
    def test_table(self, *mocks: Any) -> None:
        table_output = self.release_notes.table()
        self.assertEqual(table_output._table_name.strip(), 'Core Components CommitID(after 2022-07-26) & Release Notes info')
        self.assertEqual(table_output.headers, ['Repo', 'Branch', 'CommitID', 'Commit Date', 'Release Notes Exists', 'URL'])
        self.assertEqual(table_output.value_matrix, [['OpenSearch-test', '[main]', 'ee26e01', '2022-08-18', False, None]])
