# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, patch

import requests

from git.git_commit_processor import GitHubCommitsProcessor
from manifests.input_manifest import InputComponentFromSource


class TestGitHubCommitsProcessor(unittest.TestCase):
    """Minimal tests for GitHubCommitsProcessor covering essential functionalities."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.after_date = "2022-06-24"
        self.component = InputComponentFromSource({
            "name": "test-component",
            "repository": "https://github.com/opensearch-project/test-component.git",
            "ref": "main"
        })
        self.token = "test-token"
        self.processor = GitHubCommitsProcessor(self.after_date, self.component, self.token)

    def test_init_with_token(self) -> None:
        """Test initialization with GitHub token."""
        processor = GitHubCommitsProcessor(self.after_date, self.component, "test-token")

        self.assertEqual(processor.after_date, self.after_date)
        self.assertEqual(processor.component, self.component)
        self.assertIn("Authorization", processor.headers)
        self.assertEqual(processor.headers["Authorization"], "token test-token")

    def test_init_without_token(self) -> None:
        """Test initialization without GitHub token."""
        processor = GitHubCommitsProcessor(self.after_date, self.component, None)

        self.assertEqual(processor.after_date, self.after_date)
        self.assertEqual(processor.component, self.component)
        self.assertNotIn("Authorization", processor.headers)

    @patch('requests.get')
    def test_make_request_success(self, mock_get: MagicMock) -> None:
        """Test successful API request."""
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.processor._make_request("https://api.github.com/test")

        self.assertEqual(result, {"test": "data"})
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_make_request_failure(self, mock_get: MagicMock) -> None:
        """Test API request failure."""
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        result = self.processor._make_request("https://api.github.com/test")

        self.assertIsNone(result)

    def test_extract_pr_number_merge_commit(self) -> None:
        """Test PR number extraction from merge commit."""
        commit = {
            "commit": {
                "message": "Merge pull request #123 from opensearch-project/feature-branch"
            }
        }

        result = self.processor._extract_pr_number_from_commit(commit)

        self.assertEqual(result, 123)

    def test_extract_pr_number_parentheses(self) -> None:
        """Test PR number extraction from commit with PR in parentheses."""
        commit = {
            "commit": {
                "message": "Fix critical bug (#456)"
            }
        }

        result = self.processor._extract_pr_number_from_commit(commit)

        self.assertEqual(result, 456)

    def test_extract_pr_number_no_match(self) -> None:
        """Test PR number extraction when no PR number exists."""
        commit = {
            "commit": {
                "message": "Update documentation without PR reference"
            }
        }

        result = self.processor._extract_pr_number_from_commit(commit)

        self.assertIsNone(result)

    @patch('git.git_commit_processor.GitHubCommitsProcessor._make_request')
    def test_get_pr_details_with_caching(self, mock_make_request: MagicMock) -> None:
        """Test PR details retrieval with caching."""
        mock_pr_data = {
            "number": 123,
            "title": "Test PR",
            "labels": [{"name": "bug"}, {"name": "enhancement"}]
        }
        mock_make_request.return_value = mock_pr_data

        # First call
        result1 = self.processor.get_pr_details("owner", "repo", 123)
        # Second call (should use cache)
        result2 = self.processor.get_pr_details("owner", "repo", 123)

        self.assertEqual(result1, mock_pr_data)
        self.assertEqual(result2, mock_pr_data)
        # Should only make one API call due to caching
        mock_make_request.assert_called_once()

    @patch('git.git_commit_processor.GitHubCommitsProcessor._extract_pr_number_from_commit')
    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_pr_details')
    def test_get_commit_pr_info_success(self, mock_get_pr_details: MagicMock, mock_extract_pr: MagicMock) -> None:
        """Test successful commit PR info retrieval."""
        mock_extract_pr.return_value = 123
        mock_get_pr_details.return_value = {
            "title": "Fix bug",
            "labels": [{"name": "bug"}, {"name": "critical"}]
        }

        commit = {"sha": "abc123", "commit": {"message": "Fix bug (#123)"}}
        labels, pr_subject = self.processor.get_commit_pr_info("owner", "repo", commit)

        self.assertEqual(labels, ["bug", "critical"])
        self.assertEqual(pr_subject, "Fix bug (#123)")

    @patch('git.git_commit_processor.GitHubCommitsProcessor._extract_pr_number_from_commit')
    @patch('git.git_commit_processor.GitHubCommitsProcessor._get_pr_from_commit_api')
    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_pr_details')
    def test_get_commit_pr_info_fallback_to_api(self, mock_get_pr_details: MagicMock, mock_get_pr_api: MagicMock, mock_extract_pr: MagicMock) -> None:
        """Test commit PR info retrieval when falling back to API."""
        mock_extract_pr.return_value = None  # No PR in commit message
        mock_get_pr_api.return_value = {"number": 456}
        mock_get_pr_details.return_value = {
            "title": "Add feature",
            "labels": [{"name": "enhancement"}]
        }

        commit = {"sha": "def456", "commit": {"message": "Add new feature"}}
        labels, pr_subject = self.processor.get_commit_pr_info("owner", "repo", commit)

        self.assertEqual(labels, ["enhancement"])
        self.assertEqual(pr_subject, "Add feature (#456)")
        mock_get_pr_api.assert_called_once_with("owner", "repo", "def456")

    @patch('git.git_commit_processor.GitHubCommitsProcessor._extract_pr_number_from_commit')
    def test_get_commit_pr_info_no_pr_found(self, mock_extract_pr: MagicMock) -> None:
        """Test commit PR info retrieval when no PR is found."""
        mock_extract_pr.return_value = None

        with patch.object(self.processor, '_get_pr_from_commit_api', return_value=None):
            commit = {"sha": "xyz789", "commit": {"message": "Direct commit"}}
            labels, pr_subject = self.processor.get_commit_pr_info("owner", "repo", commit)

            self.assertEqual(labels, [])
            self.assertEqual(pr_subject, "")

    def test_filter_commits_by_labels(self) -> None:
        """Test filtering commits by labels."""
        commits = [
            {"Message": "Fix bug", "Labels": ["bug", "critical"], "PullRequestSubject": "Fix bug (#1)"},
            {"Message": "Add feature", "Labels": ["enhancement"], "PullRequestSubject": "Add feature (#2)"},
            {"Message": "Update docs", "Labels": ["documentation"], "PullRequestSubject": "Update docs (#3)"},
            {"Message": "Another bug fix", "Labels": ["bug"], "PullRequestSubject": "Another bug fix (#4)"}
        ]

        result = self.processor.filter_commits_by_labels(commits, ["bug", "enhancement"])

        self.assertEqual(len(result), 3)  # Should include commits with bug or enhancement labels
        messages = [commit["Message"] for commit in result]
        self.assertIn("Fix bug", messages)
        self.assertIn("Add feature", messages)
        self.assertIn("Another bug fix", messages)
        self.assertNotIn("Update docs", messages)

    def test_group_commits_by_labels(self) -> None:
        """Test grouping commits by labels."""
        commits = [
            {"Message": "Fix bug", "Labels": ["bug"], "PullRequestSubject": "Fix bug (#1)"},
            {"Message": "Add feature", "Labels": ["enhancement"], "PullRequestSubject": "Add feature (#2)"},
            {"Message": "Update docs", "Labels": ["documentation"], "PullRequestSubject": "Update docs (#3)"},
            {"Message": "No labels", "Labels": [], "PullRequestSubject": "No labels (#4)"}
        ]

        result = self.processor.group_commits_by_labels(commits, ["bug", "enhancement"])

        self.assertEqual(len(result["bug"]), 1)
        self.assertEqual(len(result["enhancement"]), 1)
        self.assertEqual(len(result["unlabeled"]), 2)  # documentation and no labels commits
        self.assertEqual(result["bug"][0]["Message"], "Fix bug")
        self.assertEqual(result["enhancement"][0]["Message"], "Add feature")

    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_commits_with_labels')
    def test_get_commit_details_success(self, mock_get_commits: MagicMock) -> None:
        """Test successful commit details retrieval."""
        mock_commits = [
            {"Message": "Fix bug", "Labels": ["bug"], "PullRequestSubject": "Fix bug (#123)"},
            {"Message": "Add feature", "Labels": ["enhancement"], "PullRequestSubject": "Add feature (#456)"}
        ]
        mock_get_commits.return_value = mock_commits

        result = self.processor.get_commit_details()

        self.assertEqual(result, mock_commits)
        mock_get_commits.assert_called_once_with(
            "opensearch-project",
            "test-component",
            self.after_date,
            None,
            "main"
        )

    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_commits_with_labels')
    def test_get_commit_details_no_commits(self, mock_get_commits: MagicMock) -> None:
        """Test commit details retrieval when no commits are found."""
        mock_get_commits.return_value = []

        result = self.processor.get_commit_details()

        self.assertEqual(result, [])

    @patch('git.git_commit_processor.GitHubCommitsProcessor._make_paginated_request')
    def test_get_commits_with_labels_empty_response(self, mock_paginated_request: MagicMock) -> None:
        """Test get_commits_with_labels with empty response."""
        mock_paginated_request.return_value = None

        result = self.processor.get_commits_with_labels("owner", "repo", "2022-01-01")

        self.assertEqual(result, [])

    @patch('git.git_commit_processor.GitHubCommitsProcessor._make_paginated_request')
    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_commit_pr_info')
    @patch('time.sleep')  # Mock sleep to speed up test
    def test_get_commits_with_labels_sorting(self, mock_sleep: MagicMock, mock_get_pr_info: MagicMock, mock_paginated_request: MagicMock) -> None:
        """Test sorting functionality in get_commits_with_labels method."""
        mock_paginated_request.return_value = [
            {"sha": "abc123", "commit": {"message": "Fix bug"}},
            {"sha": "def456", "commit": {"message": "Add feature"}},
            {"sha": "ghi789", "commit": {"message": "123 Numeric prefix"}},
            {"sha": "jkl012", "commit": {"message": ""}}
        ]
# Mock the PR info retrieval
        mock_get_pr_info.side_effect = [
            (["bug"], "Fix bug (#123)"),
            (["enhancement"], "Add feature (#456)"),
            (["documentation"], "123 Numeric prefix (#789)"),
            ([], "Empty message (#012)")
        ]
        test_data = [
            {"Message": "Fix bug", "Labels": ["bug"]},
            {"Message": "Add feature", "Labels": ["enhancement"]},
            {"Message": "123 Numeric prefix", "Labels": ["documentation"]},
            {"Message": "", "Labels": []}
        ]
        # Manually sort using str() to match the implementation
        expected_order = sorted(test_data, key=lambda x: str(x["Message"]))
        expected_messages = [item["Message"] for item in expected_order]
        # Now test the actual method
        result = self.processor.get_commits_with_labels("owner", "repo", "2022-01-01")
        # Verify the result is sorted by message (as strings)
        actual_messages = [commit["Message"] for commit in result]
        self.assertEqual(actual_messages, expected_messages)

    @patch('requests.get')
    def test_get_pr_from_commit_api_success(self, mock_get: MagicMock) -> None:
        """Test successful PR retrieval from commit API."""
        mock_response = Mock()
        mock_response.json.return_value = [{"number": 123, "title": "Test PR"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.processor._get_pr_from_commit_api("owner", "repo", "abc123")

        self.assertEqual(result, {"number": 123, "title": "Test PR"})
        mock_get.assert_called_once()
        # Verify special header is used
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]["headers"]["Accept"], "application/vnd.github.groot-preview+json")

    @patch('requests.get')
    def test_get_pr_from_commit_api_failure(self, mock_get: MagicMock) -> None:
        """Test PR retrieval from commit API failure."""
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        result = self.processor._get_pr_from_commit_api("owner", "repo", "abc123")

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
