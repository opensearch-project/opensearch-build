#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Tests for GitHubCommitProcessor."""

import unittest
import requests
from unittest.mock import patch, MagicMock

from git.git_commit_processor import GitHubCommitProcessor
from manifests.input_manifest import InputComponent


class TestGitHubCommitProcessor(unittest.TestCase):
    """Test GitHubCommitProcessor."""

    def setUp(self):
        """Set up test fixtures."""
        self.after_date = "2025-06-24T00:00:00Z"
        self.mock_component = MagicMock(spec=InputComponent)
        self.mock_component.name = "test-component"
        self.mock_component.repository = "https://github.com/opensearch-project/test-component"
        self.mock_component.ref = "main"
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-API-Client/1.0"
        }
        
        self.processor = GitHubCommitProcessor(
            after_date=self.after_date,
            component=self.mock_component,
            headers=self.headers
        )

    @patch('requests.get')
    def test_make_request(self, mock_get):
        """Test _make_request method with success and error cases."""
        # Test successful request
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        
        url = "https://api.github.com/repos/opensearch-project/test-component/commits"
        result = self.processor._make_request(url)
        
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with(url, headers=self.headers, params=None)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()
        
        # Reset mock for error test
        mock_get.reset_mock()
        
        # Test request with error
        mock_get.side_effect = requests.exceptions.RequestException("Test error")
        
        result = self.processor._make_request(url)
        
        self.assertIsNone(result)
        mock_get.assert_called_once_with(url, headers=self.headers, params=None)

    @patch('git.git_commit_processor.GitHubCommitProcessor._make_request')
    def test_make_paginated_request(self, mock_make_request):
        """Test _make_paginated_request method with various responses."""
        # Test with successful response
        mock_make_request.side_effect = [
            [{"id": 1}, {"id": 2}],  # First page with 2 items
            []                       # Second page with 0 items (end of pagination)
        ]
        
        url = "https://api.github.com/repos/opensearch-project/test-component/commits"
        params = {"since": self.after_date}
        result = self.processor._make_paginated_request(url, params)
        
        self.assertEqual(result, [{"id": 1}, {"id": 2}])
        mock_make_request.assert_called_once_with(
            url, {'since': self.after_date, 'page': 1, 'per_page': 100}
        )
        
        # Reset mock for empty response test
        mock_make_request.reset_mock()
        mock_make_request.side_effect = None
        mock_make_request.return_value = None
        
        # Test with empty response
        result = self.processor._make_paginated_request(url, params)
        
        self.assertEqual(result, [])
        mock_make_request.assert_called_once_with(url, {'since': self.after_date, 'page': 1, 'per_page': 100})

    def test_extract_pr_number_from_commit(self):
        """Test _extract_pr_number_from_commit method."""
        # Test merge commit message
        merge_commit = {
            "commit": {
                "message": "Merge pull request #123 from opensearch-project/feature-branch"
            }
        }
        self.assertEqual(self.processor._extract_pr_number_from_commit(merge_commit), 123)
        
        # Test PR number in parentheses
        pr_commit = {
            "commit": {
                "message": "Add new feature (#456)"
            }
        }
        self.assertEqual(self.processor._extract_pr_number_from_commit(pr_commit), 456)
        
        # Test general PR reference
        general_commit = {
            "commit": {
                "message": "Fix bug related to #789"
            }
        }
        self.assertEqual(self.processor._extract_pr_number_from_commit(general_commit), 789)
        
        # Test no PR number
        no_pr_commit = {
            "commit": {
                "message": "Update documentation"
            }
        }
        self.assertIsNone(self.processor._extract_pr_number_from_commit(no_pr_commit))

    @patch('requests.get')
    def test_get_pr_from_commit_api(self, mock_get):
        """Test _get_pr_from_commit_api method with success and error cases."""
        # Test successful API call
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{"number": 123, "title": "Test PR"}]
        mock_get.return_value = mock_response
        
        owner = "opensearch-project"
        repo = "test-component"
        commit_sha = "abc123"
        result = self.processor._get_pr_from_commit_api(owner, repo, commit_sha)
        
        self.assertEqual(result, {"number": 123, "title": "Test PR"})
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://api.github.com/repos/opensearch-project/test-component/commits/abc123/pulls")
        self.assertEqual(kwargs["headers"]["Accept"], "application/vnd.github.groot-preview+json")
        
        # Reset mock for error test
        mock_get.reset_mock()
        
        # Test API call with error
        mock_get.side_effect = requests.exceptions.RequestException("Test error")
        
        result = self.processor._get_pr_from_commit_api(owner, repo, commit_sha)
        
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('git.git_commit_processor.GitHubCommitProcessor._make_request')
    def test_get_pr_details(self, mock_make_request):
        """Test get_pr_details method."""
        mock_make_request.return_value = {"number": 123, "title": "Test PR", "labels": [{"name": "bug"}]}
        owner = "opensearch-project"
        repo = "test-component"
        pr_number = 123
        result = self.processor.get_pr_details(owner, repo, pr_number)
        self.assertEqual(result, {"number": 123, "title": "Test PR", "labels": [{"name": "bug"}]})
        mock_make_request.assert_called_once_with("https://api.github.com/repos/opensearch-project/test-component/pulls/123")
        
        # Test caching
        self.processor.get_pr_details(owner, repo, pr_number)
        # Should still be called only once because of caching
        mock_make_request.assert_called_once()

    @patch('git.git_commit_processor.GitHubCommitProcessor._extract_pr_number_from_commit')
    @patch('git.git_commit_processor.GitHubCommitProcessor.get_pr_details')
    def test_get_commit_pr_info(self, mock_get_pr_details, mock_extract_pr_number):
        """Test get_commit_pr_info method."""
        mock_extract_pr_number.return_value = 123
        mock_get_pr_details.return_value = {
            "title": "Test PR",
            "labels": [{"name": "bug"}, {"name": "enhancement"}]
        }
        
        owner = "opensearch-project"
        repo = "test-component"
        commit = {"sha": "abc123", "commit": {"message": "Fix bug (#123)"}}
        labels, pr_subject = self.processor.get_commit_pr_info(owner, repo, commit)
        
        # Verify the result
        self.assertEqual(labels, ["bug", "enhancement"])
        self.assertEqual(pr_subject, "Test PR (#123)")
        mock_extract_pr_number.assert_called_once_with(commit)
        mock_get_pr_details.assert_called_once_with(owner, repo, 123)

    @patch('git.git_commit_processor.GitHubCommitProcessor._extract_pr_number_from_commit')
    @patch('git.git_commit_processor.GitHubCommitProcessor._get_pr_from_commit_api')
    @patch('git.git_commit_processor.GitHubCommitProcessor.get_pr_details')
    def test_get_commit_pr_info_no_pr_in_message(self, mock_get_pr_details, mock_get_pr_from_api, mock_extract_pr_number):
        """Test get_commit_pr_info method when PR number is not in commit message."""
        mock_extract_pr_number.return_value = None
        mock_get_pr_from_api.return_value = {"number": 456}
        mock_get_pr_details.return_value = {
            "title": "Test PR from API",
            "labels": [{"name": "feature"}]
        }
        
        owner = "opensearch-project"
        repo = "test-component"
        commit = {"sha": "def456", "commit": {"message": "Add new feature"}}
        labels, pr_subject = self.processor.get_commit_pr_info(owner, repo, commit)
        
        # Verify the result
        self.assertEqual(labels, ["feature"])
        self.assertEqual(pr_subject, "Test PR from API (#456)")
        mock_extract_pr_number.assert_called_once_with(commit)
        mock_get_pr_from_api.assert_called_once_with(owner, repo, "def456")
        mock_get_pr_details.assert_called_once_with(owner, repo, 456)

    @patch('git.git_commit_processor.GitHubCommitProcessor._make_paginated_request')
    @patch('git.git_commit_processor.GitHubCommitProcessor.get_commit_pr_info')
    @patch('time.sleep')
    def test_get_commits_with_labels(self, mock_sleep, mock_get_commit_pr_info, mock_make_paginated_request):
        """Test get_commits_with_labels method."""
        mock_make_paginated_request.return_value = [
            {"sha": "abc123", "commit": {"message": "Fix bug (#123)"}},
            {"sha": "def456", "commit": {"message": "Add feature (#456)"}}
        ]
        mock_get_commit_pr_info.side_effect = [
            (["bug"], "Fix bug (#123)"),
            (["feature"], "Add feature (#456)")
        ]
        
        owner = "opensearch-project"
        repo = "test-component"
        since_date = "2025-06-24T00:00:00Z"
        result = self.processor.get_commits_with_labels(owner, repo, since_date)
        
        # Verify the result
        self.assertEqual(len(result), 2)
        
        # Check that both expected entries are in the result
        # The order might be different due to sorting in the implementation
        labels_found = [entry["Labels"] for entry in result]
        pr_subjects_found = [entry["PullRequestSubject"] for entry in result]
        
        self.assertIn(["bug"], labels_found)
        self.assertIn(["feature"], labels_found)
        self.assertIn("Fix bug (#123)", pr_subjects_found)
        self.assertIn("Add feature (#456)", pr_subjects_found)
        
        mock_make_paginated_request.assert_called_once()
        self.assertEqual(mock_get_commit_pr_info.call_count, 2)
        mock_sleep.assert_called()

    @patch('git.git_commit_processor.GitHubCommitProcessor.get_commits_with_labels')
    def test_get_commit_details(self, mock_get_commits_with_labels):
        """Test get_commit_details method with and without commits."""
        mock_commits = [
            {"Message": "Fix bug", "Labels": ["bug"], "PullRequestSubject": "Fix bug (#123)"},
            {"Message": "Add feature", "Labels": ["feature"], "PullRequestSubject": "Add feature (#456)"}
        ]
        mock_get_commits_with_labels.return_value = mock_commits
        
        result = self.processor.get_commit_details()
        
        self.assertEqual(result, mock_commits)
        mock_get_commits_with_labels.assert_called_once_with(
            "opensearch-project", 
            "test-component", 
            self.after_date, 
            None, 
            "main"
        )
        
        # Reset mock for no commits test
        mock_get_commits_with_labels.reset_mock()
        mock_get_commits_with_labels.return_value = []
        
        # Test with no commits
        result = self.processor.get_commit_details()
        
        self.assertIsNone(result)
        mock_get_commits_with_labels.assert_called_once()


if __name__ == '__main__':
    unittest.main()
