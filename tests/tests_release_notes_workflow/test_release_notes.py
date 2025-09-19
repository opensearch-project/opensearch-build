# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, mock_open, patch

from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes import ReleaseNotes
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs


class TestReleaseNotes(unittest.TestCase):

    def setUp(self) -> None:
        MANIFESTS = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
        )

        OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(MANIFESTS, "opensearch-test-main.yml"))
        OPENSEARCH_MANIFEST_QUALIFIER = os.path.realpath(os.path.join(MANIFESTS, "opensearch-test-main-qualifier.yml"))
        self.manifest_file = InputManifest.from_file(open(OPENSEARCH_MANIFEST))
        self.manifest_file_qualifier = InputManifest.from_file(open(OPENSEARCH_MANIFEST_QUALIFIER))
        self.build_version = self.manifest_file.build.version
        self.build_qualifier = self.manifest_file.build.qualifier
        self.build_with_qualifier_version = self.manifest_file_qualifier.build.version
        self.build_with_qualifier_qualifier = self.manifest_file_qualifier.build.qualifier
        self.release_notes = ReleaseNotes([self.manifest_file], "2022-07-26", "compile")
        self.release_notes_qualifier = ReleaseNotes([self.manifest_file_qualifier], "2022-07-26", "compile")
        self.component = InputComponentFromSource({"name": "OpenSearch-test", "repository": "url", "ref": "ref"})

        self.mock_args = Mock(spec=ReleaseNotesCheckArgs)
        self.mock_args.model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        self.mock_args.max_tokens = 2000

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check(self, *mocks: Any) -> None:
        self.assertEqual(self.release_notes.check(self.component, self.build_version, self.build_qualifier), ['OpenSearch-test', '[ref]', None, None, False, None])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check_qualifier(self, *mocks: Any) -> None:
        self.assertEqual(self.release_notes.check(self.component, self.build_with_qualifier_version, self.build_with_qualifier_qualifier), ['OpenSearch-test', '[ref]', None, None, False, None])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check_with_manifest(self, *mocks: Any) -> None:
        component = next(self.manifest_file.components.select())
        if type(component) is InputComponentFromSource:
            self.assertIsInstance(component, InputComponentFromSource)
            self.assertEqual(self.release_notes.check(component, self.build_version, self.build_qualifier), ['OpenSearch-test', '[main]', None, None, False, None])

    @patch("subprocess.check_output", return_value=''.encode())
    @patch("subprocess.check_call")
    def test_check_with_manifest_qualifier(self, *mocks: Any) -> None:
        component = next(self.manifest_file.components.select())
        if type(component) is InputComponentFromSource:
            self.assertIsInstance(component, InputComponentFromSource)
            self.assertEqual(self.release_notes.check(component, self.build_with_qualifier_version, self.build_with_qualifier_qualifier), ['OpenSearch-test', '[main]', None, None, False, None])

    @patch('release_notes_workflow.release_notes.ReleaseNotes.check', return_value=['OpenSearch-test', '[main]', 'ee26e01', '2022-08-18', False, None])
    def test_table(self, *mocks: Any) -> None:
        table_output = self.release_notes.table()
        self.assertEqual(table_output._table_name.strip(), 'Core Components CommitID(after 2022-07-26) & Release Notes info')
        self.assertEqual(table_output.headers, ['Repo', 'Branch', 'CommitID', 'Commit Date', 'Release Notes Exists', 'URL'])
        self.assertEqual(table_output.value_matrix, [['OpenSearch-test', '[main]', 'ee26e01', '2022-08-18', False, None]])

    @patch('release_notes_workflow.release_notes.GitRepository')
    @patch('release_notes_workflow.release_notes.AIReleaseNotesGenerator')
    @patch('release_notes_workflow.release_notes.GitHubCommitsProcessor')
    @patch('os.path.isfile')
    def test_generate_with_content_sources(self, mock_isfile: MagicMock, mock_commit_processor_class: MagicMock, mock_ai_generator_class: MagicMock,
                                           mock_git_repo_class: MagicMock) -> None:
        """Test generate method with different content sources (changelog and commits)."""
        # Setup common mocks
        mock_repo = MagicMock()
        mock_git_repo_class.return_value.__enter__.return_value = mock_repo
        mock_repo.dir = os.path.join("mock", "repo", "dir")

        mock_ai_generator = MagicMock()
        mock_ai_generator_class.return_value = mock_ai_generator
        mock_ai_generator.process.return_value = {"success": True}

        # Create ReleaseNotes instance
        release_notes = ReleaseNotes([self.manifest_file], "2025-06-24", "generate")

        # Test with CHANGELOG.md
        mock_isfile.return_value = True
        mock_file_content = "# CHANGELOG\nTest changelog content"
        mock_open_func = mock_open(read_data=mock_file_content)

        with patch('builtins.open', mock_open_func):
            release_notes.generate(self.mock_args, self.component, self.build_version, '', 'opensearch')

        # Verify changelog interactions
        mock_git_repo_class.assert_called_once()
        mock_isfile.assert_called_once_with(os.path.join("mock", "repo", "dir", "CHANGELOG.md"))
        mock_ai_generator_class.assert_called_once_with(args=self.mock_args)

        mock_ai_generator.generate_release_notes.assert_called_once()
        call_args = mock_ai_generator.generate_release_notes.call_args[0][0]
        self.assertIn("OpenSearch-test", call_args)
        self.assertIn("1.0", call_args)
        self.assertIn(mock_file_content, call_args)

    @patch('release_notes_workflow.release_notes.TemporaryDirectory')
    @patch('release_notes_workflow.release_notes.GitRepository')
    @patch('release_notes_workflow.release_notes.ReleaseNotesComponents')
    @patch('release_notes_workflow.release_notes.AIReleaseNotesGenerator')
    @patch('release_notes_workflow.release_notes.GitHubCommitsProcessor')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.getcwd')
    def test_generate_without_changelog_with_commits(self, mock_getcwd: MagicMock, mock_file_open: MagicMock, mock_isfile: MagicMock,
                                                     mock_github_commits_class: MagicMock, mock_ai_generator_class: MagicMock,
                                                     mock_release_notes_components: MagicMock, mock_git_repo: MagicMock, mock_temp_dir: MagicMock) -> None:
        """Test generate method when CHANGELOG.md doesn't exist but commits are available."""
        # Setup mocks
        mock_getcwd.return_value = os.path.join("test", "dir")
        mock_temp_dir_instance = Mock()
        mock_temp_dir_instance.name = os.path.join("tmp", "test")
        mock_temp_dir.return_value.__enter__.return_value = mock_temp_dir_instance

        mock_repo = Mock()
        mock_repo.dir = os.path.join("tmp", "test", "test-component")
        mock_git_repo.return_value.__enter__.return_value = mock_repo

        mock_release_notes = Mock()
        mock_release_notes.filename = ".release-notes-2.0.0.md"
        mock_release_notes_components.from_component.return_value = mock_release_notes

        mock_ai_generator = Mock()
        mock_ai_generator.generate_release_notes.return_value = "Generated release notes from commits"
        mock_ai_generator_class.return_value = mock_ai_generator

        # Mock no changelog file
        mock_isfile.return_value = False

        # Mock GitHub commits
        mock_commits_processor = Mock()
        mock_commits = [
            {
                "Message": "Fix critical bug in search",
                "Labels": ["bug", "critical"],
                "PullRequestSubject": "Fix search functionality"
            },
            {
                "Message": "Add new feature X",
                "Labels": ["enhancement"],
                "PullRequestSubject": "Implement feature X"
            },
            {
                "Message": "Flaky test fix",
                "Labels": ["flaky-test"],  # This should be filtered out
                "PullRequestSubject": "Fix flaky test"
            }
        ]
        mock_commits_processor.get_commit_details.return_value = mock_commits
        mock_github_commits_class.return_value = mock_commits_processor

        # Execute
        self.release_notes.generate(self.mock_args, self.component, self.build_version, self.build_qualifier, 'opensearch')

        # Verify
        mock_ai_generator_class.assert_called_once_with(args=self.mock_args)
        mock_isfile.assert_called_once_with(os.path.join("tmp", "test", "test-component", "CHANGELOG.md"))
        mock_github_commits_class.assert_called_once_with("2022-07-26", self.component, None)

        # Verify AI generator was called with commits prompt
        mock_ai_generator.generate_release_notes.assert_called_once()
        call_args = mock_ai_generator.generate_release_notes.call_args[0][0]
        self.assertIn("OpenSearch-test", call_args)
        self.assertIn("1.0", call_args)
        self.assertIn("Fix search functionality", call_args)
        self.assertIn("Implement feature X", call_args)
        # Verify flaky-test commit was filtered out
        self.assertNotIn("Fix flaky test", call_args)

    @patch('release_notes_workflow.release_notes.TemporaryDirectory')
    @patch('release_notes_workflow.release_notes.GitRepository')
    @patch('release_notes_workflow.release_notes.ReleaseNotesComponents')
    @patch('release_notes_workflow.release_notes.AIReleaseNotesGenerator')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.getcwd')
    def test_filename_generation(self, mock_getcwd: MagicMock, mock_file_open: MagicMock, mock_isfile: MagicMock,
                                 mock_ai_generator_class: MagicMock, mock_release_notes_components: MagicMock,
                                 mock_git_repo: MagicMock, mock_temp_dir: MagicMock) -> None:
        """Test the filename generation logic for release notes, specifically the updated repo name extraction."""
        # Setup mocks
        mock_getcwd.return_value = os.path.join("test", "dir")
        mock_temp_dir_instance = Mock()
        mock_temp_dir_instance.name = os.path.join("tmp", "test")
        mock_temp_dir.return_value.__enter__.return_value = mock_temp_dir_instance

        mock_repo = Mock()
        mock_repo.dir = os.path.join("tmp", "test", "test-component")
        mock_git_repo.return_value.__enter__.return_value = mock_repo

        mock_release_notes = Mock()
        mock_release_notes.filename = ".release-notes-2.0.0.md"
        mock_release_notes_components.from_component.return_value = mock_release_notes

        mock_ai_generator = Mock()
        mock_ai_generator.generate_release_notes.return_value = "Generated release notes"
        mock_ai_generator_class.return_value = mock_ai_generator

        mock_isfile.return_value = True

        # Create test components with different repository URLs
        # Normal component (not OpenSearch or OpenSearch-Dashboards)
        component_normal = InputComponentFromSource({
            "name": "common-utils",
            "repository": "https://github.com/opensearch-project/common-utils.git",
            "ref": "main"
        })

        # OpenSearch core component
        component_core = InputComponentFromSource({
            "name": "OpenSearch",
            "repository": "https://github.com/opensearch-project/OpenSearch.git",
            "ref": "main"
        })

        # Test with normal component
        self.release_notes.generate(self.mock_args, component_normal, "2.0.0", "", "opensearch")

        # Check that the file was opened with the correct filename
        # Should use repo name format: opensearch-common-utils.release-notes-2.0.0.md
        mock_file_open.assert_called_with(os.path.join("test", "dir", "release-notes", "opensearch-common-utils.release-notes-2.0.0.md"), "w")

        # Reset mocks for next test
        mock_file_open.reset_mock()

        # Test with OpenSearch core component
        self.release_notes.generate(self.mock_args, component_core, "2.0.0", "", "opensearch")

        # Check that the file was opened with the correct filename format for core components
        # Should use format: opensearch.release-notes-2.0.0.md
        mock_file_open.assert_called_with(os.path.join("test", "dir", "release-notes", "opensearch.release-notes-2.0.0.md"), "w")
