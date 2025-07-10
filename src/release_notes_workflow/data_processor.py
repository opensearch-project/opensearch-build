#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Data processing for changelog and commit data."""

import logging
import os
import re
import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, List
from git.git_repository import GitRepository

class DataProcessor:
    """Handles processing of changelog and commit data."""
    
    def __init__(self):
        pass
    
    def process_repository_content(self, repo, repo_name: str, baseline_date: str) -> Dict[str, Any]:
        """Process repository content for AI analysis."""
        logging.info(f"Processing repository content for {repo_name}")
        
        # First try to find and process changelog data
        changelog_data = self._find_changelog_data(repo, repo_name)
        if changelog_data:
            return changelog_data
            
        # If no changelog data found, process commits
        return self._process_commits(repo, repo_name, baseline_date)
    
    def _find_changelog_data(self, repo, repo_name: str) -> Dict[str, Any]:
        """Find and process changelog data from release notes or CHANGELOG.md."""
        
        # If no release notes found, check for CHANGELOG.md
        changelog_path = os.path.join(repo.dir, 'CHANGELOG.md')
        if os.path.exists(changelog_path):
            logging.info(f"✅ Found CHANGELOG.md file for {repo_name}")
            with open(changelog_path, 'r') as f:
                content = f.read()
            
            return self._format_changelog_data(repo_name, content, 'changelog')
        
        # No changelog data found
        logging.info(f"❌ No changelog data found for {repo_name}")
        return None
    
    def _format_changelog_data(self, repo_name: str, content: str, source: str) -> Dict[str, Any]:
        """Format changelog data for AI processing."""
        # Extract version sections from changelog
        sections = self._extract_changelog_sections(content)
        
        # Format for AI processing
        return {
            'type': 'changelog',
            'repo_name': repo_name,
            'content': content,
            'sections': sections,
            'entry_count': len(sections),
            'formatted_content': f"## {repo_name} Changelog\n\n{content}",
            'source': source
        }
    
    def _process_commits(self, repo, repo_name: str, baseline_date: str) -> Dict[str, Any]:
        """Process commits for AI analysis."""
        # No need to log here as _find_changelog_data already logged that no changelog was found
        
        try:
            # Get commits since baseline
            if hasattr(repo, 'log'):
                commits = repo.log(baseline_date)
            else:
                # Extract repository URL and ref from repo object if available
                repo_url = getattr(repo, 'url', f"https://github.com/opensearch-project/{repo_name}.git")
                repo_ref = getattr(repo, 'ref', 'main')
                
                logging.info(f"Repository object does not have log method, creating temporary GitRepository")
                with GitRepository(
                    repo_url,
                    repo_ref,
                    directory=None,  # Use temporary directory
                    fetch_depth=0    # Fetch full history
                ) as temp_repo:
                    commits = temp_repo.log(baseline_date)
            
            if not commits:
                logging.warning(f"No commits found for {repo_name} since {baseline_date}")
                return {
                    'success': False,
                    'error': f'No commits found since {baseline_date}',
                    'repo_name': repo_name
                }
            
            # Format for AI processing
            logging.info(f"Found {len(commits)} commits for {repo_name} since {baseline_date}")
            return {
                'type': 'commits',
                'repo_name': repo_name,
                'commits': commits,  # Store raw git commits
                'commit_count': len(commits),
                'formatted_content': self._format_commits_for_ai(repo_name, commits, baseline_date),
                'source': 'commits'
            }
            
        except Exception as e:
            logging.error(f"Failed to get commits for {repo_name}: {e}")
            return {
                'success': False,
                'error': f'Failed to get commits: {e}',
                'repo_name': repo_name
            }
    
    def _extract_changelog_sections(self, changelog_content: str) -> List[Dict]:
        """Extract version sections from changelog."""
        sections = []
        
        # Look for version headers (## [1.2.3] or ## Version 1.2.3, etc.)
        version_pattern = r'^##\s*(?:\[?([^\]]+)\]?|Version\s+([^\s]+))'
        lines = changelog_content.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            version_match = re.match(version_pattern, line, re.IGNORECASE)
            
            if version_match:
                # Save previous section
                if current_section:
                    sections.append({
                        'version': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # Start new section
                current_section = version_match.group(1) or version_match.group(2)
                current_content = [line]
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections.append({
                'version': current_section,
                'content': '\n'.join(current_content).strip()
            })
        
        return sections
    
    def _format_commits_for_ai(self, repo_name: str, commits: List, baseline_date: str) -> str:
        """Format commit data for AI analysis."""
        formatted_lines = [f"## {repo_name}", "", f"### Commits since {baseline_date}"]
        
        for commit in commits:
            if hasattr(commit, 'message') and commit.message:
                # Extract PR number and get labels via web scraping
                pr_labels = self._get_pr_labels_from_commit(commit.message, repo_name)
                if pr_labels:
                    formatted_lines.append(f"- {commit.id} ({commit.date}): {commit.message} [Labels: {', '.join(pr_labels)}]")
                else:
                    formatted_lines.append(f"- {commit.id} ({commit.date}): {commit.message}")
            else:
                formatted_lines.append(f"- {commit.id} ({commit.date})")
        
        return '\n'.join(formatted_lines)
    
    def _get_pr_labels_from_commit(self, commit_message: str, repo_name: str) -> list:
        """Extract PR number from commit message and scrape PR labels from GitHub."""
        
        # Extract PR number from commit message
        pr_match = re.search(r'\(#(\d+)\)', commit_message)
        if not pr_match:
            return []
        
        pr_number = pr_match.group(1)
        
        # Scrape PR labels from GitHub page
        try:
            pr_url = f"https://github.com/opensearch-project/{repo_name}/pull/{pr_number}"
            
            response = requests.get(pr_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for label elements
                labels = []
                label_elements = soup.find_all('a', class_='IssueLabel')
                for label in label_elements:
                    label_text = label.get_text().strip()
                    # Filter out version labels like 'v3.2.0'
                    if not label_text.startswith('v') and '.' not in label_text:
                        labels.append(label_text)
                
                # Remove duplicates and return
                return list(set(labels))
            else:
                logging.debug(f"Failed to fetch PR #{pr_number} page: {response.status_code}")
                return []
                
        except Exception as e:
            logging.debug(f"Error scraping PR #{pr_number} labels: {e}")
            return []
