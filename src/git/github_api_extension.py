#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Extension to GitRepository for GitHub API integration."""

import logging
import time
from typing import Dict, List, Optional

import requests

from git.git_repository import GitRepository


class GitRepositoryWithGitHubAPI(GitRepository):
    """Extends GitRepository with GitHub API capabilities."""
    
    def __init__(self, url: str, ref: str, directory: str = None, working_subdirectory: str = None, github_token: str = None):
        super().__init__(url, ref, directory, working_subdirectory)
        
        self.github_token = github_token
        self.headers = {"Authorization": f"token {github_token}"} if github_token else {}
        self.session = requests.Session()
        if github_token:
            self.session.headers.update(self.headers)
        
        # Extract repo name from URL
        self.repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
    
    def get_changelog_from_github(self) -> Optional[str]:
        """Get CHANGELOG.md content from GitHub API."""
        if not self.github_token:
            logging.warning("No GitHub token provided, cannot fetch changelog via API")
            return None
            
        changelog_url = f"https://api.github.com/repos/opensearch-project/{self.repo_name}/contents/CHANGELOG.md"
        
        response = self._make_github_request(changelog_url)
        if response and response.status_code == 200:
            import base64
            content = base64.b64decode(response.json()["content"]).decode("utf-8")
            logging.info(f"Found CHANGELOG.md for {self.repo_name} via GitHub API")
            return content
        
        logging.info(f"No CHANGELOG.md found for {self.repo_name} via GitHub API")
        return None
    
    def get_commits_since_date_from_github(self, since_date: str, until_date: str = None) -> List[Dict]:
        """Get commits since specified date via GitHub API."""
        if not self.github_token:
            logging.warning("No GitHub token provided, cannot fetch commits via API")
            return []
            
        commits_url = f"https://api.github.com/repos/opensearch-project/{self.repo_name}/commits"
        
        params = {
            "since": since_date,
            "per_page": 100
        }
        
        if until_date:
            params["until"] = until_date
            
        all_commits = []
        page = 1
        
        while True:
            params["page"] = page
            response = self._make_github_request(commits_url, params)
            
            if not response or response.status_code != 200:
                logging.warning(f"Failed to get commits for {self.repo_name}: {response.status_code if response else 'No response'}")
                break
                
            commits = response.json()
            if not commits:
                break
                
            # Enrich commits with PR information
            for commit in commits:
                commit['pull_request'] = self._get_pull_request_for_commit(commit['sha'])
                
            all_commits.extend(commits)
            page += 1
            
            # Rate limiting
            time.sleep(0.1)
            
            # Break if we got fewer than 100 commits (last page)
            if len(commits) < 100:
                break
        
        logging.info(f"Found {len(all_commits)} commits for {self.repo_name} since {since_date} via GitHub API")
        return all_commits
    
    def _get_pull_request_for_commit(self, commit_sha: str) -> Optional[Dict]:
        """Get pull request associated with a commit."""
        pr_url = f"https://api.github.com/repos/opensearch-project/{self.repo_name}/commits/{commit_sha}/pulls"
        
        response = self._make_github_request(pr_url)
        if response and response.status_code == 200:
            pulls = response.json()
            if pulls:
                # Get labels for the PR
                pr = pulls[0]
                pr['labels'] = self._get_pull_request_labels(pr['number'])
                return pr
        
        return None
    
    def _get_pull_request_labels(self, pr_number: int) -> List[str]:
        """Get labels from a pull request."""
        pr_url = f"https://api.github.com/repos/opensearch-project/{self.repo_name}/pulls/{pr_number}"
        
        response = self._make_github_request(pr_url)
        if response and response.status_code == 200:
            pr_data = response.json()
            labels = pr_data.get("labels", [])
            return [label["name"] for label in labels]
        
        return []
    
    def _make_github_request(self, url: str, params: dict = None) -> Optional[requests.Response]:
        """Make GitHub API request with error handling and rate limiting."""
        if not self.github_token:
            return None
            
        try:
            response = self.session.get(url, params=params)
            
            # Handle rate limiting
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                current_time = int(time.time())
                sleep_time = max(reset_time - current_time, 60)  # At least 1 minute
                
                logging.warning(f"Rate limited. Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
                
                # Retry the request
                response = self.session.get(url, params=params)
            
            return response
            
        except Exception as e:
            logging.error(f"GitHub API request failed for {url}: {e}")
            return None
