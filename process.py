#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Process commit data for release notes generation."""

import os
import logging
import subprocess
import datetime
from typing import Dict, Any, List

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
    
    
    def _fetch_commits_using_git(self, component_name: str) -> str:
        """Fetch commits using git commands."""
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
        import requests
        
        # Extract repository name from URL
        repo_name = component.repository.split('/')[-1].replace('.git', '')
        repo_owner = component.repository.split('/')[-2]
        
        # Construct the raw GitHub URL for CHANGELOG.md
        changelog_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{component.ref}/CHANGELOG.md"
        
        try:
            logging.info(f"Trying to fetch CHANGELOG.md from {changelog_url}")
            response = requests.get(changelog_url)
            
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
            
    def get_last_tag_date(self, build_repo, provided_date: str = None) -> str:
        """Get the date of the last tag in the opensearch-build repository."""
        try:
            last_tag_date = build_repo.get_last_tag_date()
            if last_tag_date:
                logging.info(f"Found last tag date from opensearch-build: {last_tag_date}")
                # Use the more recent date between the provided date and the last tag date
                if provided_date:
                    # Convert both dates to strings for comparison
                    date_str = str(provided_date)
                    last_tag_date_str = str(last_tag_date)
                    if date_str > last_tag_date_str:
                        logging.info(f"Using provided date {date_str} as it's more recent than the last tag date")
                        return provided_date
                    else:
                        logging.info(f"Using last tag date from opensearch-build: {last_tag_date}")
                        return last_tag_date
                else:
                    logging.info(f"Using last tag date from opensearch-build: {last_tag_date}")
                    return last_tag_date
            else:
                logging.warning("Failed to get last tag date from opensearch-build, using provided date")
                return provided_date
        except Exception as e:
            logging.warning(f"Failed to get last tag date from opensearch-build: {e}")
            return provided_date
