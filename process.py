#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Process commit data for release notes generation."""

import os
import logging
import subprocess
import datetime
import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional

class Processor:
    """Process commit data for release notes generation."""
    
    def __init__(self, version: str, baseline_date: str = None):
        self.version = version
        self.baseline_date = baseline_date
    
    def process(self, content: str, component_name: str) -> Dict[str, Any]:
        """Process content for release notes generation."""
        # If content is from git log, process it
        if content.strip() and ":" in content:
            return self._process_content(content, component_name, is_commit_history=True)
        # If content is from CHANGELOG.md, process it
        elif "# Changelog" in content or "## Unreleased" in content:
            return self._process_content(content, component_name)
        # Otherwise, try to fetch commits using git commands
        else:
            content = self._fetch_commits_using_git(component_name)
            return self._process_content(content, component_name, is_commit_history=True)
    
    def _process_content(self, content: str, component_name: str, is_commit_history: bool = False) -> Dict[str, Any]:
        """Process content for release notes generation."""
        # If content is empty and it's commit history, try to fetch commits using git commands
        if is_commit_history and not content.strip():
            content = self._fetch_commits_using_git(component_name)
        
        # Format the content for AI processing
        formatted_content = content
        
        return {
            'component_name': component_name,
            'formatted_content': formatted_content,
            'raw_content': content
        }
    
    
    def _make_github_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make a GET request to GitHub API"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "OpenSearch-Release-Notes/1.0"
        }
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"Error making request to {url}: {e}")
            return None
    
    def _make_paginated_github_request(self, url: str, params: Dict = None) -> Optional[List[Dict]]:
        """Make a GET request to GitHub API with pagination support"""
        all_data = []
        page = 1
        
        while True:
            current_params = params.copy() if params else {}
            current_params.update({"page": page, "per_page": 100})
            
            data = self._make_github_request(url, current_params)
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
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"
        
        # Use a special accept header to get PR associations
        headers = {
            "Accept": "application/vnd.github.groot-preview+json",
            "User-Agent": "OpenSearch-Release-Notes/1.0"
        }
        
        # Add GitHub token if available
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            prs = response.json()
            
            if prs and len(prs) > 0:
                return prs[0]  # Return the first (usually only) PR
        except requests.exceptions.RequestException:
            pass
        
        return None
    
    def _fetch_commits_using_git(self, component_name: str) -> str:
        """Fetch commits using GitHub API."""
        try:
            # Extract owner and repo from component name
            owner = "opensearch-project"
            repo = component_name
            
            # GitHub API endpoint for commits
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            
            # Set parameters for the API request
            after_date = self.baseline_date or "2025-01-01"
            params = {
                "since": after_date
            }
            
            logging.info(f"Fetching commits for {component_name} since {after_date} using GitHub API...")
            
            # Make the paginated request to GitHub API
            commits = self._make_paginated_github_request(url, params)
            
            if not commits:
                logging.warning(f"No commits found for {component_name} since {after_date}")
                return ""
            
            logging.info(f"Found {len(commits)} commits for {component_name}")
            
            # Process commits to get formatted output similar to git log
            result = []
            
            # Cache for PR data to avoid duplicate API calls
            pr_cache = {}
            
            # Use threading for faster API calls, but be mindful of rate limits
            max_workers = 5  # Conservative to avoid hitting rate limits
            
            def get_pr_details(pr_number):
                """Get detailed PR information including labels"""
                if pr_number in pr_cache:
                    return pr_cache[pr_number]
                
                url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
                pr_data = self._make_github_request(url)
                
                if pr_data:
                    pr_cache[pr_number] = pr_data
                
                return pr_data
            
            def process_commit(commit):
                commit_hash = commit["sha"][:7]  # Short hash
                commit_date = commit["commit"]["author"]["date"].split("T")[0]  # YYYY-MM-DD
                commit_message = commit["commit"]["message"].replace('\n', ' ').replace('\r', ' ').strip()
                
                # Try to get PR information
                pr_number = self._extract_pr_number_from_commit(commit)
                pr_labels = []
                pr_title = ""
                
                if not pr_number:
                    pr_data = self._get_pr_from_commit_api(owner, repo, commit["sha"])
                    if pr_data:
                        pr_number = pr_data["number"]
                
                # If we have a PR number, get the PR details including labels
                if pr_number:
                    pr_details = get_pr_details(pr_number)
                    if pr_details:
                        pr_labels = [label["name"] for label in pr_details.get("labels", [])]
                        pr_title = pr_details.get("title", "").strip()
                
                # Format the commit line
                if pr_number:
                    label_str = f" [labels: {', '.join(pr_labels)}]" if pr_labels else ""
                    return f"{commit_hash} {commit_date} {commit_message} (#{pr_number}){label_str}"
                else:
                    return f"{commit_hash} {commit_date} {commit_message}"
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_commit = {
                    executor.submit(process_commit, commit): commit
                    for commit in commits
                }
                
                for future in as_completed(future_to_commit):
                    commit_line = future.result()
                    result.append(commit_line)
                    
                    # Small delay to be nice to the API
                    time.sleep(0.1)
            
            # Join the results into a string
            return "\n".join(result)
            
        except Exception as e:
            logging.error(f"Failed to fetch commits using GitHub API: {e}")
            
            # Fall back to git commands if GitHub API fails
            logging.info(f"Falling back to git commands for {component_name}")
            try:
                # Create a temporary directory
                temp_dir = os.path.join("/tmp", f"git-{component_name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
                os.makedirs(temp_dir, exist_ok=True)

                # Clone the repository
                repo_url = f"https://github.com/opensearch-project/{component_name}.git"
                subprocess.run(["git", "clone", "--depth=1000", repo_url, temp_dir], check=True, capture_output=True)

                # Fetch more history if needed
                subprocess.run(["git", "fetch", "--unshallow"], cwd=temp_dir, check=False, capture_output=True)

                # Get commits after the baseline date
                after_date = self.baseline_date or "2025-01-01"
                cmd = ["git", "log", "--date=short", f"--after={after_date}", "--pretty=format:%h %ad %s"]
                result = subprocess.run(cmd, cwd=temp_dir, check=True, capture_output=True, text=True)

                # Clean up
                subprocess.run(["rm", "-rf", temp_dir], check=True, capture_output=True)

                return result.stdout
            except Exception as e:
                logging.error(f"Failed to fetch commits using git commands: {e}")
                return ""
            
    def fetch_changelog_from_github(self, component) -> str:
        """Fetch CHANGELOG.md directly from GitHub."""
        # Extract repository name from URL
        repo_name = component.repository.split('/')[-1].replace('.git', '')
        repo_owner = component.repository.split('/')[-2]
        
        # Construct the raw GitHub URL for CHANGELOG.md
        changelog_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{component.ref}/CHANGELOG.md"
        
        try:
            logging.info(f"Trying to fetch CHANGELOG.md from {changelog_url}")
            
            # Use standard requests here since we're fetching raw content, not JSON
            headers = {
                "User-Agent": "OpenSearch-Release-Notes/1.0"
            }
            
            # Add GitHub token if available
            github_token = os.environ.get("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"
            
            response = requests.get(changelog_url, headers=headers)
            
            if response.status_code == 200:
                logging.info(f"Found CHANGELOG.md for {component.name} at {changelog_url}")
                return response.text
            else:
                logging.info(f"Failed to fetch CHANGELOG.md from {changelog_url}, status code: {response.status_code}")
                return None
        except Exception as e:
            logging.warning(f"Error fetching CHANGELOG.md from GitHub: {e}")
            return None
            
    def get_commit_history_content(self, repo, baseline_date: str, component_name: str) -> str:
        """Get commit history content from the repository."""
        logging.info(f"Fetching commit history for {component_name} after {baseline_date}")
        content = self._fetch_commits_using_git(component_name)
        if content.strip():
            logging.info(f"Successfully fetched commits for {component_name}")
            return content
        else:
            logging.warning(f"No commits found for {component_name} after {baseline_date}")
            return None
            
    def get_last_tag_date(self, build_repo=None, provided_date: str = None) -> str:
        """Get the date of the last tag in the opensearch-build repository using GitHub API."""
        try:
            # GitHub API endpoint for releases
            api_url = "https://api.github.com/repos/opensearch-project/opensearch-build/releases"
            
            # Make the paginated request to GitHub API
            releases = self._make_paginated_github_request(api_url)
            
            # Check if there are any releases
            if releases:
                # Sort releases by published_at date (newest first)
                sorted_releases = sorted(releases, key=lambda x: x.get('published_at', ''), reverse=True)
                
                # Get the date of the newest release
                newest_release = sorted_releases[0]
                last_tag_date = newest_release.get('published_at', '').split('T')[0]  # Format: YYYY-MM-DD
                
                logging.info(f"Found newest release: {newest_release.get('tag_name')} published on {last_tag_date}")
                
                # Use the more recent date between the provided date and the last tag date
                if provided_date:
                    # Convert both dates to strings for comparison
                    date_str = str(provided_date)
                    last_tag_date_str = str(last_tag_date)
                    if date_str > last_tag_date_str:
                        logging.info(f"Using provided date {date_str} as it's more recent than the last tag date")
                        return provided_date
                    else:
                        logging.info(f"Using last tag date from GitHub API: {last_tag_date}")
                        return last_tag_date
                else:
                    logging.info(f"Using last tag date from GitHub API: {last_tag_date}")
                    return last_tag_date
            else:
                logging.warning("No releases found in the GitHub API response, using provided date")
                return provided_date
        except Exception as e:
            logging.warning(f"Failed to get last tag date from GitHub API: {e}, using provided date")
            return provided_date
