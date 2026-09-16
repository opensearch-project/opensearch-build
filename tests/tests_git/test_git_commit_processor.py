# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
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
            "labels": [{"name": "bug"}, {"name": "critical"}],
            "body": "This fixes a critical bug"
        }

        commit = {"sha": "abc123", "commit": {"message": "Fix bug (#123)"}}
        labels, pr_subject, pr_body = self.processor.get_commit_pr_info("owner", "repo", commit)

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
        labels, pr_subject, pr_body = self.processor.get_commit_pr_info("owner", "repo", commit)

        self.assertEqual(labels, ["enhancement"])
        self.assertEqual(pr_subject, "Add feature (#456)")
        mock_get_pr_api.assert_called_once_with("owner", "repo", "def456")

    @patch('git.git_commit_processor.GitHubCommitsProcessor._extract_pr_number_from_commit')
    def test_get_commit_pr_info_no_pr_found(self, mock_extract_pr: MagicMock) -> None:
        """Test commit PR info retrieval when no PR is found."""
        mock_extract_pr.return_value = None

        with patch.object(self.processor, '_get_pr_from_commit_api', return_value=None):
            commit = {"sha": "xyz789", "commit": {"message": "Direct commit"}}
            labels, pr_subject, pr_body = self.processor.get_commit_pr_info("owner", "repo", commit)

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

    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_commits_from_local_git')
    def test_get_commit_details_prefers_local_git_when_base_ref_set(self, mock_local_git: MagicMock) -> None:
        """When base_ref is provided, get_commit_details should use local-git patch-id selection.

        A version base ref (X.Y.Z) resolves to the 'major.minor' release branch.
        """
        processor = GitHubCommitsProcessor(self.after_date, self.component, self.token, base_ref="3.4.0")
        mock_commits = [
            {"Message": "New feature", "Labels": ["enhancement"], "PullRequestSubject": "New feature (#1)", "PullRequestBody": ""}
        ]
        mock_local_git.return_value = mock_commits

        result = processor.get_commit_details()

        self.assertEqual(result, mock_commits)
        mock_local_git.assert_called_once_with(
            "opensearch-project",
            "test-component",
            "3.4",
            "main"
        )

    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_commits_from_local_git')
    def test_get_commit_details_local_git_no_commits(self, mock_local_git: MagicMock) -> None:
        """Local-git selection returning no commits yields an empty list."""
        processor = GitHubCommitsProcessor(self.after_date, self.component, self.token, base_ref="3.4.0")
        mock_local_git.return_value = []

        result = processor.get_commit_details()

        self.assertEqual(result, [])

    @patch('git.git_commit_processor.GitHubCommitsProcessor.get_commits_from_local_git')
    def test_get_commit_details_strips_tags_prefix_on_head(self, mock_local_git: MagicMock) -> None:
        """A 'tags/' prefix on the component head ref is stripped before selection."""
        component = InputComponentFromSource({
            "name": "OpenSearch",
            "repository": "https://github.com/opensearch-project/OpenSearch.git",
            "ref": "tags/3.9.0"
        })
        processor = GitHubCommitsProcessor(None, component, self.token, base_ref="3.8.0")
        mock_local_git.return_value = []

        processor.get_commit_details()

        mock_local_git.assert_called_once_with("opensearch-project", "OpenSearch", "3.8", "3.9.0")

    def test_parse_git_log_parses_records(self) -> None:
        """_parse_git_log should split RS-separated records into {sha, commit:{message}} dicts."""
        output = (
            "abc123\x1fFix bug (#1)\n\nbody line\x1e"
            "def456\x1fAdd feature (#2)\x1e"
        )
        commits = GitHubCommitsProcessor._parse_git_log(output)

        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]["sha"], "abc123")
        self.assertIn("Fix bug (#1)", commits[0]["commit"]["message"])
        self.assertEqual(commits[1]["sha"], "def456")
        self.assertEqual(commits[1]["commit"]["message"], "Add feature (#2)")

    def test_parse_git_log_empty(self) -> None:
        """_parse_git_log returns an empty list for empty output."""
        self.assertEqual(GitHubCommitsProcessor._parse_git_log(""), [])

    @patch('git.git_commit_processor.GitHubCommitsProcessor._enrich_commits')
    @patch('git.git_commit_processor.GitHubCommitsProcessor._rev')
    @patch('git.git_commit_processor.GitHubCommitsProcessor._git')
    @patch('tempfile.TemporaryDirectory')
    def test_get_commits_from_local_git_runs_cherry_pick(self, mock_tmp: MagicMock, mock_git: MagicMock,
                                                         mock_rev: MagicMock, mock_enrich: MagicMock) -> None:
        """get_commits_from_local_git clones, runs the cherry-pick-aware log, and enriches results."""
        mock_tmp.return_value.__enter__.return_value = os.path.join("tmp", "rn")
        # clone, fetch base, fetch head, then the log call returns the RS/US formatted output
        log_output = "sha1\x1fFix codecoverage upload action (#2229)\x1esha2\x1fApply input validation (#2225)\x1e"
        mock_git.side_effect = ["", "", "", log_output]
        mock_rev.side_effect = ["basesha", "headsha"]
        enriched = [{"Message": "x", "Labels": [], "PullRequestSubject": "x (#2229)", "PullRequestBody": ""}]
        mock_enrich.return_value = enriched

        result = self.processor.get_commits_from_local_git("opensearch-project", "alerting", "3.8", "main")

        self.assertEqual(result, enriched)
        # The final git call must be the cherry-pick-aware log with the resolved SHAs.
        log_call = mock_git.call_args_list[-1][0][0]
        self.assertIn("log", log_call)
        self.assertIn("--cherry-pick", log_call)
        self.assertIn("--right-only", log_call)
        self.assertIn("--no-merges", log_call)
        self.assertIn("basesha...headsha", log_call)
        mock_enrich.assert_called_once()

    @patch('git.git_commit_processor.GitHubCommitsProcessor._rev')
    @patch('git.git_commit_processor.GitHubCommitsProcessor._git')
    @patch('tempfile.TemporaryDirectory')
    def test_get_commits_from_local_git_unresolved_ref(self, mock_tmp: MagicMock, mock_git: MagicMock, mock_rev: MagicMock) -> None:
        """If a ref cannot be resolved, selection returns an empty list."""
        mock_tmp.return_value.__enter__.return_value = os.path.join("tmp", "rn")
        mock_git.return_value = ""
        mock_rev.side_effect = [None, "headsha"]  # base unresolved

        result = self.processor.get_commits_from_local_git("opensearch-project", "alerting", "9.9", "main")

        self.assertEqual(result, [])

    def test_init_with_base_ref(self) -> None:
        """base_ref is stored on the processor."""
        processor = GitHubCommitsProcessor(self.after_date, self.component, self.token, base_ref="3.4.0")
        self.assertEqual(processor.base_ref, "3.4.0")

    def test_init_default_base_ref_is_none(self) -> None:
        """base_ref defaults to None (legacy date-based selection)."""
        self.assertIsNone(self.processor.base_ref)

    def test_resolve_base_ref_version_to_branch(self) -> None:
        """A 3-part version base ref resolves to the major.minor release branch."""
        self.assertEqual(self.processor._resolve_base_ref("3.8.0"), "3.8")

    def test_resolve_base_ref_four_part_version_to_branch(self) -> None:
        """A 4-part plugin version base ref also resolves to the major.minor release branch."""
        self.assertEqual(self.processor._resolve_base_ref("3.8.0.0"), "3.8")

    def test_resolve_base_ref_strips_tags_prefix(self) -> None:
        """A 'tags/' prefix is stripped, then the version resolves to the branch."""
        self.assertEqual(self.processor._resolve_base_ref("tags/3.8.0.0"), "3.8")

    def test_resolve_base_ref_branch_unchanged(self) -> None:
        """A non-version ref (branch) is used unchanged."""
        self.assertEqual(self.processor._resolve_base_ref("2.x"), "2.x")

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
            (["bug"], "Fix bug (#123)", "Bug fix description"),
            (["enhancement"], "Add feature (#456)", "Feature description"),
            (["documentation"], "123 Numeric prefix (#789)", "Doc description"),
            ([], "Empty message (#012)", "")
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
