# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

"""
GitHub Commits Since Date with PR Labels

This script fetches commits from a GitHub repository since a specified date,
and returns a list of JSON entries with Message and Labels fields.
"""

import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import requests

from manifests.input_manifest import InputComponent

logger = logging.getLogger(__name__)


class GitHubCommitsProcessor:
    def __init__(self, after_date: str, component: InputComponent, token: Optional[str] = None):
        """
        Initialize the GitHub Commits Fetcher

        Args:
            token: GitHub personal access token (optional but recommended)
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Commits-Fetcher/1.0"
        }

        if token:
            self.headers["Authorization"] = f"token {token}"

        # Cache for PR data to avoid duplicate API calls
        self.pr_cache: Dict = {}
        self.after_date = after_date
        self.component = component

    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make a GET request to GitHub API"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return dict(response.json())  # Explicitly cast to Dict
        except requests.exceptions.RequestException as e:
            logger.info(f"Error making request to {url}: {e}")
            return None

    def _make_paginated_request(self, url: str, params: Dict = None) -> Optional[List[Dict]]:
        """Make a GET request to GitHub API with pagination support"""
        all_data: List[Dict] = []
        page = 1

        while True:
            current_params = params.copy() if params else {}
            current_params.update({"page": page, "per_page": 100})

            data = self._make_request(url, current_params)
            if not data:
                break

            all_data.extend(data)

            # Check if there are more pages
            if len(data) < 100:  # Less than per_page means last page
                break

            page += 1

        return all_data

    def _extract_pr_number_from_commit(self, commit: Dict) -> Optional[int]:
        """
        Extract PR number from commit message or commit data

        Common patterns:
        - "Merge pull request #123 from..."
        - "Fix issue (#123)"
        - "(#123)"
        """
        message = commit["commit"]["message"]

        # Pattern for merge commits
        merge_pattern = r"Merge pull request #(\d+)"
        match = re.search(merge_pattern, message)
        if match:
            return int(match.group(1))

        # Pattern for PR numbers in parentheses
        pr_pattern = r"\(#(\d+)\)"
        match = re.search(pr_pattern, message)
        if match:
            return int(match.group(1))

        # Pattern for general PR references
        general_pattern = r"#(\d+)"
        match = re.search(general_pattern, message)
        if match:
            return int(match.group(1))

        return None

    def _get_pr_from_commit_api(self, owner: str, repo: str, commit_sha: str) -> Optional[Dict]:
        """
        Get PR information using the commit SHA via GitHub API
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/commits/{commit_sha}/pulls"

        # Use a special accept header to get PR associations
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.groot-preview+json"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            prs = list(response.json())  # Convert to List

            if prs and len(prs) > 0:
                return dict(prs[0])  # Convert to Dict
        except requests.exceptions.RequestException:
            pass

        return None

    def get_pr_details(self, owner: str, repo: str, pr_number: int) -> Optional[Dict]:
        """Get detailed PR information including labels"""
        if pr_number in self.pr_cache:
            return dict(self.pr_cache[pr_number])  # Explicitly cast to Dict

        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        pr_data = self._make_request(url)

        if pr_data:
            self.pr_cache[pr_number] = pr_data

        return pr_data

    def get_commit_pr_info(self, owner: str, repo: str, commit: Dict) -> tuple[List[str], str]:
        """
        Get labels and PR subject for a commit from its associated PR

        Returns:
            Tuple of (labels, pr_subject) where pr_subject is formatted as "Title (#PR_NUMBER)" or empty string
        """
        # Try to get PR number from commit message
        pr_number = self._extract_pr_number_from_commit(commit)

        # If no PR number found in message, try API method
        if not pr_number:
            pr_data = self._get_pr_from_commit_api(owner, repo, commit["sha"])
            if pr_data:
                pr_number = pr_data["number"]

        # Get detailed PR information if we have a PR number
        if pr_number:
            pr_details = self.get_pr_details(owner, repo, pr_number)
            if pr_details:
                labels = [label["name"] for label in pr_details.get("labels", [])]
                pr_title = pr_details.get("title", "").strip()
                pr_subject = f"{pr_title} (#{pr_number})" if pr_title else f"(#{pr_number})"
                return labels, pr_subject

        return [], ""

    def get_commits_with_labels(self, owner: str, repo: str, since_date: str,
                                until_date: str = None, branch: str = None) -> List[Dict]:
        """
        Get all commits since a specific date with their associated PR labels and subjects

        Args:
            owner: Repository owner
            repo: Repository name
            since_date: ISO 8601 formatted date string
            until_date: ISO 8601 formatted date string (optional, commits before this date)
            branch: Specific branch to get commits from (optional)

        Returns:
            List of dictionaries with 'Message', 'Labels', and 'PullRequestSubject' fields
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"

        params = {
            "since": since_date
        }

        if until_date:
            params["until"] = until_date

        if branch:
            params["sha"] = branch

        logger.info(f"Fetching commits since {since_date}" + (f" until {until_date}" if until_date else "") + "...")
        commits = self._make_paginated_request(url, params)

        if not commits:
            return []

        logger.info(f"Found {len(commits)} commits. Fetching PR labels...")

        # Process commits to get message and labels
        result = []

        # Use threading for faster API calls, but be mindful of rate limits
        max_workers = 5  # Conservative to avoid hitting rate limits

        def process_commit(commit: Dict) -> Dict:
            message = commit["commit"]["message"].replace('\n', ' ').replace('\r', ' ').strip()
            labels, pr_subject = self.get_commit_pr_info(owner, repo, commit)
            return {
                "Message": message,
                "Labels": labels,
                "PullRequestSubject": pr_subject
            }

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_commit = {
                executor.submit(process_commit, commit): commit
                for commit in commits
            }

            for i, future in enumerate(as_completed(future_to_commit)):
                commit_entry = future.result()
                result.append(commit_entry)

                # Progress indicator
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(commits)} commits...")

                # Small delay to be nice to the API
                time.sleep(0.1)

        # Sort by commit message for consistent output
        result.sort(key=lambda x: str(x["Message"]))

        return result

    def filter_commits_by_labels(self, commits: List[Dict], target_labels: List[str]) -> List[Dict]:
        """
        Filter commits that have any of the specified labels

        Args:
            commits: List of commit dictionaries with Message, Labels, and PullRequestSubject
            target_labels: List of labels to filter by

        Returns:
            Filtered list of commits
        """
        filtered = []
        for commit in commits:
            if any(label in commit["Labels"] for label in target_labels):
                filtered.append(commit)
        return filtered

    def group_commits_by_labels(self, commits: List[Dict], target_labels: List[str]) -> Dict[str, List[Dict]]:
        """
        Group commits by labels

        Args:
            commits: List of commit dictionaries with Message, Labels, and PullRequestSubject
            target_labels: List of labels to group by

        Returns:
            Dictionary with labels as keys and lists of commits as values
        """
        grouped: Dict = {label: [] for label in target_labels}
        grouped["unlabeled"] = []

        for commit in commits:
            if commit["Labels"]:
                # Check if commit has any of the target labels
                found_labels = [label for label in target_labels if label in commit["Labels"]]

                if found_labels:
                    for label in found_labels:
                        grouped[label].append(commit)
                else:
                    grouped["unlabeled"].append(commit)
            else:
                grouped["unlabeled"].append(commit)

        return grouped

    def get_commit_details(self) -> List[Dict]:
        iso_since_date = self.after_date

        iso_until_date = None
        url = self.component.repository.rstrip('/').removesuffix('.git')  # type: ignore[attr-defined]
        # Split by '/' and get the last two parts
        parts = url.split('/')
        owner = parts[-2]
        repo = parts[-1]

        # Get all commits with labels
        commits = self.get_commits_with_labels(owner, repo, iso_since_date, iso_until_date, self.component.ref)  # type: ignore[attr-defined]

        if not commits:
            logger.info("No commits found since the specified date.")
            return []
        return commits
