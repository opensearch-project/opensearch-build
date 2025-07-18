#!/usr/bin/env python3
"""
GitHub Commits Since Date with PR Labels
 
This script fetches commits from a GitHub repository since a specified date,
and returns a list of JSON entries with Message and Labels fields.
"""
 
import requests
import re
import json
import os
import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from manifests.input_manifest import InputComponent
 
class GitHubCommitProcessor:
    def __init__(self, after_date: str, component: InputComponent, token: Optional[str] = None):
        """
        Initialize the GitHub Commits Fetcher
 
        Args:
            token: GitHub personal access token (optional but recommended)
                  If not provided, will check for GITHUB_TOKEN or GH_TOKEN environment variables
        """
        
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Commits-Fetcher/1.0"
        }
 
        # Use provided token, or check environment variables
        if token:
            self.headers["Authorization"] = f"token {token}"
        else:
            env_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
            if env_token:
                print("Using GitHub token from environment variables")
                self.headers["Authorization"] = f"token {env_token}"
 
        # Cache for PR data to avoid duplicate API calls
        self.pr_cache = {}
        self.after_date = after_date
        self.component = component
 
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make a GET request to GitHub API"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None
 
    def _make_paginated_request(self, url: str, params: Dict = None) -> Optional[List[Dict]]:
        """Make a GET request to GitHub API with pagination support"""
        all_data = []
        page = 1
 
        while True:
            current_params = params.copy() if params else {}
            current_params.update({"page": page, "per_page": 100})
 
            data = self._make_request(url, current_params)
            if not data:
                break
 
            all_data.extend(data)

            if len(data) < 100:
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
            prs = response.json()
 
            if prs and len(prs) > 0:
                return prs[0]  # Return the first (usually only) PR
        except requests.exceptions.RequestException:
            pass
 
        return None
 
    def get_pr_details(self, owner: str, repo: str, pr_number: int) -> Optional[Dict]:
        """Get detailed PR information including labels"""
        if pr_number in self.pr_cache:
            return self.pr_cache[pr_number]
 
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
 
        print(f"Fetching commits since {since_date}" + (f" until {until_date}" if until_date else "") + "...")
        commits = self._make_paginated_request(url, params)
 
        if not commits:
            return []
 
        print(f"Found {len(commits)} commits. Fetching PR labels...")
 
        # Process commits to get message and labels
        result = []
 
        # Use threading for faster API calls, but be mindful of rate limits
        max_workers = 5  # Conservative to avoid hitting rate limits
 
        def process_commit(commit):
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
                    print(f"Processed {i + 1}/{len(commits)} commits...")
 
                # Small delay to be nice to the API
                time.sleep(1)
 
        # Sort by commit message for consistent output
        result.sort(key=lambda x: x["Message"])
 
        return result

    def get_commit_details(self):
        # Use the provided date (which should be the last tag date from release_notes.py)
        iso_since_date = self.after_date
        print(f"Using baseline date: {iso_since_date}")
 
        iso_until_date = None
        url = self.component.repository.rstrip('/').removesuffix('.git')
        # Split by '/' and get the last two parts
        parts = url.split('/')
        owner = parts[-2]
        repo = parts[-1]
        #if args.until:
        #    try:
        #        iso_until_date = parse_date_input(args.until)
        #    except ValueError as e:
        #       print(f"Error parsing until date: {e}")
        #       sys.exit(1)
 
        # Get all commits with labels
        commits = self.get_commits_with_labels(owner, repo, iso_since_date, iso_until_date, self.component.ref)
 
        if not commits:
            print("No commits found since the specified date.")
            return
 
        # Apply filtering if requested
        # if self.release_notes_args.filter_labels:
        #    commits = self.filter_commits_by_labels(commits, self.release_notes_args.filter_labels)
        #    print(f"Filtered to {len(commits)} commits with labels: {', '.join(self.release_notes_args.filter_labels)}")
 
        # Group by labels if requested
        # if args.group_by_labels:
        #    grouped_commits = fetcher.group_commits_by_labels(commits, args.group_by_labels)
 
        #    result = {}
        #    for label, label_commits in grouped_commits.items():
        #        if label_commits:
        #            result[label] = label_commits
 
        #    output_data = result
        #else:
        # Output the list of commits
        #    output_data = commits
 
        # Convert to JSON string
        json_output = json.dumps(commits, indent=2)
 
        # Debug logging to see what the commit data looks like
        print(f"DEBUG: Found {len(commits)} commits with labels")
        for i, commit in enumerate(commits[:5]):  # Print first 5 commits for debugging
            print(f"DEBUG: Commit {i+1}:")
            print(f"  Message: {commit['Message'][:100]}...")
            print(f"  Labels: {commit['Labels']}")
            print(f"  PullRequestSubject: {commit['PullRequestSubject'][:100]}...")
        
        # Write to file or print to console
        #print(json_output)
        return commits
