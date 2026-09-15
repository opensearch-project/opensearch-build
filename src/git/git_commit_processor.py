# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

"""
GitHub Commits Fetcher with PR Labels

This module fetches commits from a GitHub repository and returns a list of JSON entries
with Message, Labels, PullRequestSubject, and PullRequestBody fields.

Commit selection supports two modes:
  - Ref-based (preferred): uses local git with patch-id comparison
    (git log --cherry-pick --right-only --no-merges base...head) to select the commits new to
    the head ref, correctly excluding cherry-picked backports that carry a different SHA.
  - Date-based (legacy): uses the list-commits API with a since date.
"""

import logging
import os
import re
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import requests

from manifests.input_manifest import InputComponent

logger = logging.getLogger(__name__)


class GitHubCommitsProcessor:
    def __init__(self, after_date: Optional[str], component: InputComponent, token: Optional[str] = None, base_ref: Optional[str] = None):
        """
        Initialize the GitHub Commits Fetcher

        Args:
            after_date: ISO 8601 date string for date-based commit selection (legacy).
                Only used when base_ref is not provided.
            component: The input manifest component. component.ref is used as the head ref.
            token: GitHub personal access token (optional but recommended)
            base_ref: Baseline git ref (previous release tag or branch, e.g. "2.19.0" or
                "tags/3.4.0"). When provided, commits are selected via the GitHub Compare API
                (base_ref...component.ref) instead of a since-date. This is ancestry-based and
                avoids missing pre-date commits or duplicating already-shipped/backported commits.
                See https://github.com/opensearch-project/opensearch-build/issues/6056
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
        self.base_ref = base_ref

    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make a GET request to GitHub API"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
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

    def _git(self, args: List[str], cwd: str) -> str:
        """Run a git command in cwd and return stripped stdout. Raises on non-zero exit."""
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()

    def get_commits_from_local_git(self, owner: str, repo: str, base_ref: str, head_ref: str) -> List[Dict]:
        """
        Select commits new to head_ref relative to base_ref using local git with patch-id
        equivalence (git log --cherry-pick --right-only --no-merges base...head), then enrich
        them with PR labels/subjects/bodies.

        Unlike the GitHub Compare API (SHA-based), this correctly excludes cherry-picked
        backports: a commit backported to the release branch has a different SHA but the same
        patch-id, so --cherry-pick drops it. See
        https://github.com/opensearch-project/opensearch-build/issues/6056

        Args:
            owner: Repository owner
            repo: Repository name
            base_ref: Baseline ref already reachable/shipping (e.g. release branch tip '3.8')
            head_ref: Head ref for the new release (e.g. 'main' or '3.x')

        Returns:
            List of dictionaries with 'Message', 'Labels', 'PullRequestSubject', and
            'PullRequestBody' fields.
        """
        clone_url = f"https://github.com/{owner}/{repo}.git"

        with tempfile.TemporaryDirectory(prefix="release-notes-") as tmp:
            work = os.path.join(tmp, repo)
            logger.info(f"Cloning {clone_url} to compute {base_ref}...{head_ref} with patch-id equivalence...")

            # A blobless clone keeps history (needed for patch-id / merge-base) while avoiding
            # the cost of downloading file contents.
            self._git(["clone", "--filter=blob:none", "--no-checkout", "--quiet", clone_url, work], cwd=tmp)

            # Ensure both refs are present locally (branch, tag, or SHA).
            for ref in {base_ref, head_ref}:
                try:
                    self._git(["fetch", "--quiet", "origin", ref], cwd=work)
                except subprocess.CalledProcessError:
                    # SHA or already-present ref; fetch by ref may fail harmlessly.
                    logger.info(f"Could not fetch ref '{ref}' explicitly; relying on cloned refs.")

            base = self._rev(work, base_ref)
            head = self._rev(work, head_ref)
            if base is None or head is None:
                logger.warning(
                    f"Could not resolve base '{base_ref}' or head '{head_ref}' in {owner}/{repo}; "
                    f"no commits selected."
                )
                return []

            output = self._git(
                ["log", "--no-merges", "--cherry-pick", "--right-only",
                 "--pretty=format:%H%x1f%B%x1e", f"{base}...{head}"],
                cwd=work,
            )

        raw_commits = self._parse_git_log(output)
        if not raw_commits:
            logger.info(f"No commits found in {head_ref} that are not already in {base_ref} (patch-id aware).")
            return []

        logger.info(f"Found {len(raw_commits)} commits new to {head_ref}. Fetching PR labels...")
        return self._enrich_commits(owner, repo, raw_commits)

    def _rev(self, work: str, ref: str) -> Optional[str]:
        """Resolve a ref to a commit SHA, trying local, origin/<ref>, and FETCH_HEAD forms."""
        for candidate in (ref, f"origin/{ref}", "FETCH_HEAD"):
            try:
                return self._git(["rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}"], cwd=work)
            except subprocess.CalledProcessError:
                continue
        return None

    @staticmethod
    def _parse_git_log(output: str) -> List[Dict]:
        """
        Parse `git log --pretty=format:%H%x1f%B%x1e` output into commit dicts shaped like the
        GitHub API commits (so they can flow through the existing enrichment path).

        Records are separated by the RS (0x1e) byte; within a record the SHA and full body are
        separated by the US (0x1f) byte.
        """
        commits: List[Dict] = []
        for record in output.split("\x1e"):
            record = record.strip("\n")
            if not record:
                continue
            sha, _, message = record.partition("\x1f")
            sha = sha.strip()
            if not sha:
                continue
            commits.append({"sha": sha, "commit": {"message": message.strip()}})
        return commits

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
            prs = response.json()  # type: ignore[no-any-return]

            if prs and len(prs) > 0:
                return prs[0]  # type: ignore[no-any-return]
        except requests.exceptions.RequestException:
            pass

        return None

    def get_pr_details(self, owner: str, repo: str, pr_number: int) -> Optional[Dict]:
        """Get detailed PR information including labels"""
        if pr_number in self.pr_cache:
            return self.pr_cache[pr_number]  # type: ignore[no-any-return]

        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        pr_data = self._make_request(url)

        if pr_data:
            self.pr_cache[pr_number] = pr_data

        return pr_data

    def get_commit_pr_info(self, owner: str, repo: str, commit: Dict) -> tuple[List[str], str, str]:
        """
        Get labels, PR subject, and PR body for a commit from its associated PR

        Returns:
            Tuple of (labels, pr_subject, pr_body) where pr_subject is formatted as "Title (#PR_NUMBER)" or empty string
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
                pr_body = pr_details.get("body", "") or ""
                return labels, pr_subject, pr_body

        return [], "", ""

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

        return self._enrich_commits(owner, repo, commits)

    def _enrich_commits(self, owner: str, repo: str, commits: List[Dict]) -> List[Dict]:
        """
        Enrich raw GitHub commit objects with PR labels, subjects, and bodies.

        Args:
            owner: Repository owner
            repo: Repository name
            commits: Raw commit objects from the GitHub commits/compare API

        Returns:
            List of dictionaries with 'Message', 'Labels', 'PullRequestSubject', and
            'PullRequestBody' fields, sorted by message.
        """
        # Process commits to get message and labels
        result = []

        # Use threading for faster API calls, but be mindful of rate limits
        max_workers = 5  # Conservative to avoid hitting rate limits

        def process_commit(commit: Dict) -> Dict:
            message = commit["commit"]["message"].replace('\n', ' ').replace('\r', ' ').strip()
            labels, pr_subject, pr_body = self.get_commit_pr_info(owner, repo, commit)
            return {
                "Message": message,
                "Labels": labels,
                "PullRequestSubject": pr_subject,
                "PullRequestBody": pr_body
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
        result.sort(key=lambda x: x["Message"])

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

    def _resolve_base_ref(self, base_ref: str) -> str:
        """
        Resolve the baseline ref used for patch-id comparison.

        The most robust baseline for "what already shipped / is shipping in the previous line"
        is the release BRANCH tip (e.g. '3.8'), because the branch keeps receiving backports
        after the tag is cut. Comparing against the branch (rather than the frozen X.Y.Z /
        X.Y.Z.0 tag) maximizes detection of cherry-picked backports.

        When base_ref is a version (X.Y.Z or X.Y.Z.0), it is reduced to the 'major.minor'
        branch name. Any other form (an explicit branch such as '2.x', a commit SHA, or a
        'tags/...' ref) is used unchanged (with a leading 'tags/' stripped).
        """
        base_ref = base_ref.removeprefix("tags/")

        # X.Y.Z or X.Y.Z.0 -> major.minor release branch (e.g. 3.8.0 / 3.8.0.0 -> 3.8)
        version_match = re.fullmatch(r"(\d+)\.(\d+)(?:\.\d+){1,2}", base_ref)
        if version_match:
            branch = f"{version_match.group(1)}.{version_match.group(2)}"
            logger.info(f"Resolved base version '{base_ref}' to release branch '{branch}' for patch-id comparison")
            return branch

        return base_ref

    def get_commit_details(self) -> List[Dict]:
        url = self.component.repository.rstrip('/').removesuffix('.git')  # type: ignore[attr-defined]
        # Split by '/' and get the last two parts
        parts = url.split('/')
        owner = parts[-2]
        repo = parts[-1]
        head_ref = self.component.ref.removeprefix("tags/")  # type: ignore[attr-defined]

        # Prefer ref-based selection via local git with patch-id equivalence when a base ref is
        # provided. This detects cherry-picked backports (different SHA, same change) that the
        # date-based and Compare-API approaches miss.
        # https://github.com/opensearch-project/opensearch-build/issues/6056
        if self.base_ref:
            base_ref = self._resolve_base_ref(self.base_ref)
            return self.get_commits_from_local_git(owner, repo, base_ref, head_ref)

        # Legacy date-based selection (kept for backward compatibility).
        iso_since_date = self.after_date
        iso_until_date = None

        # Get all commits with labels
        commits = self.get_commits_with_labels(owner, repo, iso_since_date, iso_until_date, head_ref)

        if not commits:
            logger.info("No commits found since the specified date.")
            return []
        return commits
