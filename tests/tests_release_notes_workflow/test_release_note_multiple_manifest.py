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
    MANIFESTS = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
    )

    def setUp(self) -> None:
        OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(TestReleaseNotes.MANIFESTS, "opensearch-test-main.yml"))
        OPENSEARCH_MANIFEST_QUALIFIER = os.path.realpath(os.path.join(TestReleaseNotes.MANIFESTS, "opensearch-test-main-qualifier.yml"))
        DASHBOARDS_MANIFEST = os.path.realpath(
            os.path.join(TestReleaseNotes.MANIFESTS, "opensearch-dashboards-test-main.yml"))
        self.opensearch_manifest = InputManifest.from_file(open(OPENSEARCH_MANIFEST))
        self.opensearch_manifest_qualifier = InputManifest.from_file(open(OPENSEARCH_MANIFEST_QUALIFIER))
        self.dashboards_manifest = InputManifest.from_file(open(DASHBOARDS_MANIFEST))
        self.build_version = self.opensearch_manifest.build.version
        self.build_qualifier = self.opensearch_manifest.build.qualifier
        self.build_with_qualifier_version = self.opensearch_manifest_qualifier.build.version
        self.build_with_qualifier_qualifier = self.opensearch_manifest_qualifier.build.qualifier
        self.release_notes = ReleaseNotes([self.opensearch_manifest, self.dashboards_manifest], "2022-07-26", "compile")
        self.release_notes_qualifier = ReleaseNotes([self.opensearch_manifest_qualifier, self.dashboards_manifest], "2022-07-26", "compile")
        self.opensearch_component = InputComponentFromSource(
            {"name": "OpenSearch-test", "repository": "url", "ref": "ref"})
        self.dashboards_component = InputComponentFromSource(
            {"name": "OpenSearch-Dashboards-test", "repository": "url", "ref": "ref"})

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check(self, *mocks: Any) -> None:
        self.assertEqual(self.release_notes.check(self.opensearch_component, self.build_version, self.build_qualifier),
                         ['OpenSearch-test', '[ref]', None, None, False, None])
        self.assertEqual(self.release_notes.check(self.dashboards_component, self.build_version, self.build_qualifier),
                         ['OpenSearch-Dashboards-test', '[ref]', None, None, False, None])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check_qualifier(self, *mocks: Any) -> None:
        self.assertEqual(self.release_notes_qualifier.check(self.opensearch_component, self.build_version, self.build_with_qualifier_qualifier),
                         ['OpenSearch-test', '[ref]', None, None, False, None])
        self.assertEqual(self.release_notes_qualifier.check(self.dashboards_component, self.build_version, self.build_with_qualifier_qualifier),
                         ['OpenSearch-Dashboards-test', '[ref]', None, None, False, None])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_table(self, *mocks: Any) -> None:
        self.release_notes.check(self.opensearch_component, self.build_version, self.build_qualifier)
        self.release_notes.check(self.dashboards_component, self.build_version, self.build_qualifier)
        self.release_notes.table()

        self.assertEqual(self.release_notes.table()._table_name.strip(),
                         'Core Components CommitID(after 2022-07-26) & Release Notes info')
        self.assertEqual(self.release_notes.table().headers,
                         ['Repo', 'Branch', 'CommitID', 'Commit Date', 'Release Notes Exists', 'URL'])
        self.assertEqual(self.release_notes.table().value_matrix,
                         [['OpenSearch-Dashboards-test', '[main]', None, None, False, None],
                          ['OpenSearch-test', '[main]', None, None, False, None]])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_table_qualifier(self, *mocks: Any) -> None:
        self.release_notes_qualifier.check(self.opensearch_component, self.build_with_qualifier_version, self.build_with_qualifier_qualifier)
        self.release_notes_qualifier.check(self.dashboards_component, self.build_with_qualifier_version, self.build_with_qualifier_qualifier)
        self.release_notes_qualifier.table()

        self.assertEqual(self.release_notes_qualifier.table()._table_name.strip(),
                         'Core Components CommitID(after 2022-07-26) & Release Notes info')
        self.assertEqual(self.release_notes_qualifier.table().headers,
                         ['Repo', 'Branch', 'CommitID', 'Commit Date', 'Release Notes Exists', 'URL'])
        self.assertEqual(self.release_notes_qualifier.table().value_matrix,
                         [['OpenSearch-Dashboards-test', '[main]', None, None, False, None],
                          ['OpenSearch-test', '[main]', None, None, False, None]])
