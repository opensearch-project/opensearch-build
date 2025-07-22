# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import patch, MagicMock, mock_open

from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes import ReleaseNotes
from git.git_commit_processor import GitHubCommitProcessor
from llms.ai_release_notes_generator import AIReleaseNotesGenerator


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
    @patch('release_notes_workflow.release_notes.GitHubCommitProcessor')
    @patch('os.path.isfile')
    def test_generate_with_content_sources(self, mock_isfile, mock_commit_processor_class, mock_ai_generator_class, mock_git_repo_class):
        """Test generate method with different content sources (changelog and commits)."""
        # Setup common mocks
        mock_repo = MagicMock()
        mock_git_repo_class.return_value.__enter__.return_value = mock_repo
        mock_repo.dir = "/mock/repo/dir"
        
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
            release_notes.generate(self.component, self.build_version)
        
        # Verify changelog interactions
        mock_git_repo_class.assert_called_once()
        mock_isfile.assert_called_once_with('/mock/repo/dir/CHANGELOG.md')
        mock_ai_generator_class.assert_called_once_with(version=self.build_version, baseline_date="2025-06-24")
        mock_ai_generator.process.assert_called_once_with(
            mock_file_content, 
            self.component.name, 
            None, 
            mock_repo, 
            self.component
        )
        
        # Reset mocks for commit history test
        mock_git_repo_class.reset_mock()
        mock_isfile.reset_mock()
        mock_ai_generator_class.reset_mock()
        mock_ai_generator.process.reset_mock()
        
        # Test with commit history
        mock_isfile.return_value = False
        mock_commit_processor = MagicMock()
        mock_commit_processor_class.return_value = mock_commit_processor
        mock_commits = [
            {"sha": "abc123", "commit": {"message": "Fix bug (#123)"}, "Labels": ["bug"], "PullRequestSubject": "Fix bug (#123)"},
            {"sha": "def456", "commit": {"message": "Add feature (#456)"}, "Labels": ["feature"], "PullRequestSubject": "Add feature (#456)"}
        ]
        mock_commit_processor.get_commit_details.return_value = mock_commits
        
        release_notes.generate(self.component, self.build_version)
        
        # Verify commit history interactions
        mock_git_repo_class.assert_called_once()
        mock_isfile.assert_called_once_with('/mock/repo/dir/CHANGELOG.md')
        mock_commit_processor_class.assert_called_once()
        mock_ai_generator_class.assert_called_once_with(version=self.build_version, baseline_date="2025-06-24")
        mock_ai_generator.process.assert_called_once()
        # Check that the commits were passed to the AI generator as JSON
        args, _ = mock_ai_generator.process.call_args
        self.assertIsInstance(args[0], str)
        self.assertIn("abc123", args[0])
        self.assertIn("def456", args[0])

    @patch('release_notes_workflow.release_notes.GitRepository')
    @patch('release_notes_workflow.release_notes.AIReleaseNotesGenerator')
    @patch('release_notes_workflow.release_notes.GitHubCommitProcessor')
    @patch('os.path.isfile')
    def test_generate_no_commits(self, mock_isfile, mock_commit_processor_class, mock_ai_generator_class, mock_git_repo_class):
        """Test generate method when no commits are found."""
        mock_isfile.return_value = False
        mock_repo = MagicMock()
        mock_git_repo_class.return_value.__enter__.return_value = mock_repo
        mock_repo.dir = "/mock/repo/dir"
        
        mock_ai_generator = MagicMock()
        mock_ai_generator_class.return_value = mock_ai_generator
        
        mock_commit_processor = MagicMock()
        mock_commit_processor_class.return_value = mock_commit_processor
        mock_commit_processor.get_commit_details.return_value = None
        release_notes = ReleaseNotes([self.manifest_file], "2025-06-24", "generate")
        
        release_notes.generate(self.component, self.build_version)
        
        # Verify the interactions
        mock_git_repo_class.assert_called_once()
        mock_isfile.assert_called_once_with('/mock/repo/dir/CHANGELOG.md')
        mock_commit_processor_class.assert_called_once()
        mock_ai_generator.process.assert_not_called()

    @patch('release_notes_workflow.release_notes.requests.get')
    @patch('release_notes_workflow.release_notes.GitRepository')
    @patch('release_notes_workflow.release_notes.AIReleaseNotesGenerator')
    @patch('os.path.isfile')
    def test_generate_with_github_api(self, mock_isfile, mock_ai_generator_class, mock_git_repo_class, mock_requests_get):
        """Test generate method with GitHub API date retrieval (success and error cases)."""
        mock_isfile.return_value = True
        mock_repo = MagicMock()
        mock_git_repo_class.return_value.__enter__.return_value = mock_repo
        mock_repo.dir = "/mock/repo/dir"
        
        mock_ai_generator = MagicMock()
        mock_ai_generator_class.return_value = mock_ai_generator
        mock_ai_generator.process.return_value = {"success": True}
        
        # Create a mock file content
        mock_file_content = "# CHANGELOG\nTest changelog content"
        mock_open_func = mock_open(read_data=mock_file_content)
        
        # Test successful GitHub API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"published_at": "2025-05-15T00:00:00Z"}
        mock_requests_get.return_value = mock_response
        
        # Create ReleaseNotes instance with no date
        release_notes = ReleaseNotes([self.manifest_file], None, "generate")
        
        # Call the generate method
        with patch('builtins.open', mock_open_func):
            release_notes.generate(self.component, self.build_version)
        
        # Verify the interactions
        mock_git_repo_class.assert_called_once()
        mock_requests_get.assert_called_once()
        mock_ai_generator_class.assert_called_once_with(version=self.build_version, baseline_date="2025-05-15T00:00:00Z")
        mock_ai_generator.process.assert_called_once()
        
        # Reset mocks for API error test
        mock_git_repo_class.reset_mock()
        mock_requests_get.reset_mock()
        mock_ai_generator_class.reset_mock()
        mock_ai_generator.process.reset_mock()
        
        # Test GitHub API error
        mock_requests_get.side_effect = Exception("API Error")
        
        # Call the generate method
        with patch('builtins.open', mock_open_func):
            # Should not raise an exception
            release_notes.generate(self.component, self.build_version)
        
        # Verify the interactions
        mock_git_repo_class.assert_called_once()
        mock_requests_get.assert_called_once()
        # Should still create AI generator with None date
        mock_ai_generator_class.assert_called_once()
        mock_ai_generator.process.assert_called_once()
