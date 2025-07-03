#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Data processing for changelog and commit data."""

import logging
import re
from typing import Any, Dict, List


class DataProcessor:
    """Handles processing of changelog and commit data."""
    
    def __init__(self):
        pass
    
    def process_changelog(self, repo_name: str, data: str) -> Dict[str, Any]:
        """Process changelog data."""
        logging.info(f"Processing CHANGELOG data for {repo_name}")
        
        # Extract version sections from changelog
        sections = self._extract_changelog_sections(data)
        
        # Format for AI processing
        processed_data = {
            'type': 'changelog',
            'repo_name': repo_name,
            'content': data,
            'sections': sections,
            'entry_count': len(sections),
            'formatted_content': self._format_changelog_for_ai(repo_name, data)
        }
        
        return processed_data
    
    def extract_commits(self, repo_name: str, commits: List[Dict], baseline_date: str) -> Dict[str, Any]:
        """Extract and process commits since baseline."""
        logging.info(f"Processing {len(commits)} commits for {repo_name} since {baseline_date}")
        
        processed_commits = []
        
        for commit in commits:
            processed_commit = {
                'sha': commit['sha'],
                'message': commit['commit']['message'].split('\n')[0],  # First line only
                'date': commit['commit']['committer']['date'],
                'author': commit['commit']['author']['name'],
                'url': commit['html_url'],
                'pull_request': None,
                'labels': []
            }
            
            # Add PR information if available
            if commit.get('pull_request'):
                pr = commit['pull_request']
                processed_commit['pull_request'] = {
                    'number': pr['number'],
                    'title': pr['title'],
                    'url': pr['html_url'],
                    'labels': pr.get('labels', [])
                }
                processed_commit['labels'] = pr.get('labels', [])
            
            processed_commits.append(processed_commit)
        
        # Format for AI processing
        processed_data = {
            'type': 'commits',
            'repo_name': repo_name,
            'baseline_date': baseline_date,
            'commits': processed_commits,
            'commit_count': len(processed_commits),
            'formatted_content': self._format_commits_for_ai(repo_name, processed_commits)
        }
        
        return processed_data
    
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
    
    def _format_changelog_for_ai(self, repo_name: str, changelog_content: str) -> str:
        """Format changelog content for AI analysis."""
        return f"""## {repo_name}

### CHANGELOG Content

{changelog_content}

### Processing Instructions
This is a CHANGELOG file. Please extract and categorize the changes according to the standard release notes format.
"""
    
    def _format_commits_for_ai(self, repo_name: str, commits: List[Dict]) -> str:
        """Format commit data for AI analysis."""
        formatted_lines = [f"## {repo_name}", "", "### Commits"]
        
        for commit in commits:
            commit_line = f"- {commit['message']}"
            
            # Add PR information if available
            if commit['pull_request']:
                pr = commit['pull_request']
                commit_line += f" ([#{pr['number']}]({pr['url']}))"
                
                # Add labels if available
                if commit['labels']:
                    labels_str = ", ".join(commit['labels'])
                    commit_line += f" [Labels: {labels_str}]"
            
            formatted_lines.append(commit_line)
        
        formatted_lines.extend([
            "",
            "### Processing Instructions",
            "These are commits since the last release. Please analyze and categorize them according to the standard release notes format.",
            "Use PR labels when available to help with categorization."
        ])
        
        return '\n'.join(formatted_lines)
    
    def merge_data_sources(self, changelog_data: Dict = None, commit_data: Dict = None) -> Dict[str, Any]:
        """Merge changelog and commit data for comprehensive analysis."""
        merged_data = {
            'sources': [],
            'content_parts': [],
            'total_entries': 0
        }
        
        if changelog_data:
            merged_data['sources'].append('changelog')
            merged_data['content_parts'].append(changelog_data['formatted_content'])
            merged_data['total_entries'] += changelog_data['entry_count']
        
        if commit_data:
            merged_data['sources'].append('commits')
            merged_data['content_parts'].append(commit_data['formatted_content'])
            merged_data['total_entries'] += commit_data['commit_count']
        
        # Combine all content for AI processing
        merged_data['combined_content'] = '\n\n'.join(merged_data['content_parts'])
        
        return merged_data
