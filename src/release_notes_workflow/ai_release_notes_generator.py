#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""AI-powered release notes generator extending existing workflow."""

import logging
import os
from typing import Any, Dict, List

import boto3

from git.git_repository import GitRepository
from git.github_api_extension import GitRepositoryWithGitHubAPI
from manifests.input_manifest import InputComponentFromSource
from release_notes_workflow.data_processor import DataProcessor
from release_notes_workflow.release_notes_component import ReleaseNotesComponents


class ReleaseNotesGenerator:
    """Base release notes generator (following existing pattern)."""
    
    def __init__(self, version: str, work_dir: str):
        self.version = version
        self.work_dir = work_dir
        self.processed_components = []
        self.failed_components = []


class AIReleaseNotesGenerator(ReleaseNotesGenerator):
    """AI-powered release notes generator using AWS Bedrock."""
    
    def __init__(self, github_token: str, version: str, baseline_date: str = None, work_dir: str = None):
        super().__init__(version, work_dir)
        
        self.github_token = github_token
        self.baseline_date = baseline_date
        
        # Initialize clients
        self.bedrock_client = self._create_bedrock_client()
        self.data_processor = DataProcessor()
        
        # Set baseline date
        if not self.baseline_date:
            self.baseline_date = "2024-01-01"  # Default baseline
        self.baseline_tag = "custom"
    
    def _create_bedrock_client(self):
        """Create AWS Bedrock client."""
        try:
            return boto3.client('bedrock-runtime', region_name='us-east-1')
        except Exception as e:
            logging.warning(f"Failed to create Bedrock client: {e}")
            return None
    
    def _get_baseline_date(self) -> tuple:
        """Get baseline date from previous version tag."""
        # Calculate previous version (3.0.0 for 3.1.0)
        version_parts = self.version.split('.')
        if len(version_parts) >= 2:
            major, minor = int(version_parts[0]), int(version_parts[1])
            if minor > 0:
                baseline_version = f"{major}.{minor-1}.0"
            else:
                baseline_version = f"{major-1}.0.0" if major > 0 else "2.0.0"
        else:
            baseline_version = "3.0.0"
        
        return self.github_client.get_baseline_tag_date(baseline_version)
    
    def generate_release_notes(self, repositories: List[str]) -> Dict[str, Any]:
        """Generate AI-powered release notes for multiple repositories."""
        results = {}
        
        for repo_name in repositories:
            logging.info(f"Generating release notes for {repo_name}")
            result = self.process_repository_by_name(repo_name)
            results[repo_name] = result
        
        return results
    
    def process_repository(self, component: InputComponentFromSource, existing_repo_dir: str = None) -> Dict[str, Any]:
        """Process individual repository and make decision on changelog vs commit."""
        repo_name = component.repository.rstrip('/').split('/')[-1].replace('.git', '')
        
        logging.info(f"Processing component: {component.name} (repo: {repo_name})")
        
        try:
            # Step 1: Use existing repository directory if provided, otherwise create new one
            if existing_repo_dir:
                # Create a mock repo object that points to existing directory
                repo = type('MockRepo', (), {
                    'dir': existing_repo_dir,
                    'working_directory': existing_repo_dir
                })()
                
                # Process without context manager since we're reusing existing repo
                return self._process_repository_content(repo, component, repo_name)
            else:
                # Step 1: Checkout repository using existing GitRepository
                with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(self.work_dir, repo_name),
                    component.working_directory
                ) as repo:
                    return self._process_repository_content(repo, component, repo_name)
                    
        except Exception as e:
            logging.error(f"Failed to process {component.name}: {e}")
            self.failed_components.append(component.name)
            return {
                'success': False,
                'error': str(e),
                'repo_name': repo_name
            }
    
    def _process_repository_content(self, repo, component: InputComponentFromSource, repo_name: str) -> Dict[str, Any]:
        """Process repository content for AI analysis."""
        try:
                
                # Step 2: Check for existing release notes or CHANGELOG files
                release_notes = ReleaseNotesComponents.from_component(
                    component, self.version, None, repo.dir
                )
                
                changelog_content = None
                changelog_source = None
                
                # First check for existing release notes
                if release_notes.exists():
                    logging.info(f"✅ Found existing release notes for {component.name}")
                    with open(release_notes.full_path, 'r') as f:
                        changelog_content = f.read()
                    changelog_source = "release-notes"
                else:
                    logging.info(f"🔍 No existing release notes found for {component.name}, checking for CHANGELOG files...")
                    # Check for CHANGELOG file in root directory
                    changelog_files = ['CHANGELOG.md', 'CHANGELOG.rst', 'CHANGELOG.txt', 'CHANGELOG']
                    for changelog_file in changelog_files:
                        changelog_path = os.path.join(repo.dir, changelog_file)
                        logging.debug(f"Checking for CHANGELOG at: {changelog_path}")
                        if os.path.exists(changelog_path):
                            logging.info(f"✅ Found CHANGELOG file for {component.name}: {changelog_file}")
                            with open(changelog_path, 'r') as f:
                                changelog_content = f.read()
                            changelog_source = "changelog"
                            break
                    else:
                        logging.info(f"❌ No CHANGELOG file found for {component.name}")
                
                if changelog_content:
                    # Process existing changelog/release notes
                    processed_data = self.data_processor.process_changelog(repo_name, changelog_content)
                    processed_data['source'] = changelog_source
                    logging.info(f"Using {changelog_source} content for {repo_name}")
                else:
                    # Step 3: Use git commands to get commit data (no GitHub API needed)
                    logging.info(f"Using git-based commit route for {repo_name}")
                    
                    # Get commits since baseline using git log
                    try:
                        # Use the existing repo's git log functionality
                        if hasattr(repo, 'log'):
                            commits = repo.log(self.baseline_date)
                        else:
                            # Fallback: create a temporary GitRepository with full history
                            with GitRepository(
                                component.repository,
                                component.ref,
                                directory=None,  # Use temporary directory
                                fetch_depth=0   # Fetch full history
                            ) as temp_repo:
                                commits = temp_repo.log(self.baseline_date)
                        
                        if not commits:
                            logging.warning(f"No commits found for {repo_name} since {self.baseline_date}")
                            return {
                                'success': False,
                                'error': f'No commits found since {self.baseline_date}',
                                'repo_name': repo_name
                            }
                        
                        # Use simple approach like original script - no complex data processing
                        logging.info(f"Found {len(commits)} commits for {repo_name} since {self.baseline_date}")
                        
                        # Create simple processed data for AI
                        processed_data = {
                            'type': 'commits',
                            'repo_name': repo_name,
                            'commit_count': len(commits),
                            'commits': commits,  # Use raw git commits
                            'formatted_content': self._format_commits_simple(repo_name, commits)
                        }
                        
                    except Exception as e:
                        logging.error(f"Failed to get commits for {repo_name}: {e}")
                        return {
                            'success': False,
                            'error': f'Failed to get commits: {e}',
                            'repo_name': repo_name
                        }
                
                # Step 4: Generate AI-powered release notes
                if self.bedrock_client:
                    ai_result = self._generate_ai_release_notes(processed_data)
                    
                    # Check if AI analysis actually succeeded
                    if ai_result and not ai_result.startswith("AI analysis failed"):
                        # START OF TEST CODE - DISABLE FILE WRITING
                        logging.info(f"🧪 TEST MODE: Skipping file writing for {repo_name}")
                        # END OF TEST CODE
                        
                        # START OF CODE TO COMMENT OUT DURING TEST
                        # # Step 5: Write release notes to repository
                        # self._write_release_notes_to_repo(repo, component.name, ai_result)
                        # 
                        # # Step 6: Commit changes (if not in test mode)
                        # self._commit_release_notes(repo, component.name)
                        # END OF CODE TO COMMENT OUT DURING TEST
                        
                        self.processed_components.append(component.name)
                        
                        return {
                            'success': True,
                            'repo_name': repo_name,
                            'component_name': component.name,
                            'data_type': processed_data['type'],
                            'entry_count': processed_data.get('entry_count', processed_data.get('commit_count', 0)),
                            'ai_result': ai_result
                        }
                    else:
                        # AI analysis failed
                        logging.warning(f"❌ AI analysis failed for {repo_name}: {ai_result}")
                        return {
                            'success': False,
                            'error': f'AI analysis failed: {ai_result}',
                            'repo_name': repo_name
                        }
                else:
                    logging.warning(f"No Bedrock client available, skipping AI analysis for {repo_name}")
                    return {
                        'success': False,
                        'error': 'No Bedrock client available',
                        'repo_name': repo_name
                    }
        
        except Exception as e:
            logging.error(f"Failed to process {component.name}: {e}")
            self.failed_components.append(component.name)
            return {
                'success': False,
                'error': str(e),
                'repo_name': repo_name
            }
    
    def process_repository_by_name(self, repo_name: str) -> Dict[str, Any]:
        """Process repository by name (for standalone usage)."""
        # Create mock component for compatibility
        mock_component = type('MockComponent', (), {
            'name': repo_name,
            'repository': f'https://github.com/opensearch-project/{repo_name}.git',
            'ref': 'main',
            'working_directory': None
        })()
        
        return self.process_repository(mock_component)
    
    def _generate_ai_release_notes(self, processed_data: Dict[str, Any]) -> str:
        """Generate release notes using AI."""
        if not self.bedrock_client:
            return "AI analysis not available"
        
        prompt = self._create_ai_prompt(processed_data)
        
        try:
            import json
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 8000,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            }
            
            response = self.bedrock_client.invoke_model(
                modelId='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
                body=json.dumps(body),
                contentType='application/json'
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
            
        except Exception as e:
            logging.error(f"AI analysis failed: {e}")
            return f"AI analysis failed: {e}"
    
    def _format_commits_simple(self, repo_name: str, commits: List) -> str:
        """Format commits for AI analysis using simple approach like original script."""
        formatted_lines = [f"## {repo_name}", "", f"### Commits since {self.baseline_date}"]
        
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
        
        formatted_lines.extend([
            "",
            "### Processing Instructions",
            "These are git commits since the last release. Please analyze and categorize them according to the standard release notes format.",
            "**IMPORTANT: Use the GitHub PR Labels provided in [Labels: ...] to determine the correct category:**",
            "- 'bug', 'bugfix' labels → Bug Fixes",
            "- 'enhancement', 'improve' labels → Enhancements", 
            "- 'feature', 'new-feature' labels → Features",
            "- 'breaking-change', 'breaking' labels → Breaking Changes",
            "- 'documentation', 'docs' labels → Documentation",
            "- 'infrastructure', 'ci', 'build' labels → Infrastructure",
            "- 'maintenance', 'chore' labels → Maintenance",
            "- 'refactor', 'refactoring' labels → Refactoring",
            "**If PR labels are available, prioritize them over commit message analysis.**",
            "If no labels are available, fall back to commit message content analysis.",
            "Extract PR numbers from commit messages (e.g., '#3833' from '(#3833)').",
            "Format entries as: Description ([#PR_NUMBER](https://github.com/opensearch-project/REPO_NAME/pull/PR_NUMBER))",
            "If no PR number is found, use the commit hash instead."
        ])
        
        return '\n'.join(formatted_lines)
    
    def _get_pr_labels_from_commit(self, commit_message: str, repo_name: str) -> list:
        """Extract PR number from commit message and scrape PR labels from GitHub."""
        import re
        
        # Extract PR number from commit message
        pr_match = re.search(r'\(#(\d+)\)', commit_message)
        if not pr_match:
            return []
        
        pr_number = pr_match.group(1)
        
        # Scrape PR labels from GitHub page
        try:
            import requests
            from bs4 import BeautifulSoup
            
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
    
    def _create_ai_prompt(self, processed_data: Dict[str, Any]) -> str:
        """Create AI prompt adapted for single-component modular workflow."""
        repo_name = processed_data['repo_name']
        repository_url = f"https://github.com/opensearch-project/{repo_name}"
        
        prompt = f"""Generate OpenSearch plugin release notes for a single component from commit data.

**Component Information:**
- Component: {repo_name}
- Version: {self.version}
- Repository: {repository_url}

**Commit Data:**
{processed_data['formatted_content']}

**Instructions:**
1. **Label-based Categorization Logic:**
   - First, check if any labels match these categories (case-insensitive, partial matches allowed):
     * "breaking change" or "breaking" → Breaking Changes
     * "feature" or "feat" → Features  
     * "enhancement" or "improve" → Enhancements
     * "bug" or "fix" or "bugfix" → Bug Fixes
     * "infrastructure" or "ci" or "test" → Infrastructure
     * "documentation" or "docs" → Documentation
     * "maintenance" or "version" or "support" → Maintenance
     * "refactor" or "refactoring" → Refactoring
   - If a commit has multiple labels that match different categories above, place it in the "Other" category
   - If a commit has no labels or labels that don't match any of the above categories, proceed to fallback analysis

2. **Fallback Message Analysis:**
   - If no labels match, analyze the Message content to determine the appropriate category following below guidelines:
    * Features: A change that introduce a net new unit of functionality of a software system that satisfies a requirement, 
    represents a design decision, and provides a potential configuration option. As for improvement on existing features, 
    use the Enhancement category. As for fixes on existing features, use the Bug Fixes category. Example: "Add start/stop batch actions on detector list page"
    * Enhancements: A change that improves the performance, usability, or reliability of an existing feature without changing its core functionality. Example: "Improve detector list page performance"
    * Bug Fixes: A change that resolves an issue or defect in the software. Example: "Fix issue with detector creation form validation"
    * Infrastructure: A change that modifies the underlying architecture, build process, or deployment of the software Example: "Update CI/CD pipeline for better reliability"
    * Documentation: A change that updates or adds documentation, such as README files, user guides, or API docs. Example: "Update README with new installation instructions"
    * Maintenance: A change that involves routine upkeep, such as version updates, dependency management, or minor tweaks that do not fit other categories. Example: "Update dependencies to latest versions"
    * Refactoring: A change that improves the internal structure of the code without changing its external behavior. Example: "Refactor detector service for better readability or Make ClusterDetailsEventProcessor and all its access methods non-static"
    * Other: If the commit cannot be clearly categorized into any of the above categories through message analysis, place it in "Other"
   - Do not lose any commit information, even if it doesn't match any category

3. **Entry Format:**
   - Use commit message as the main content for each entry
   - Extract PR number from commit message (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - **IMPORTANT**: Capitalize the first letter of every entry description (after the asterisk and space)

4. **Output Requirements:**
   - Generate markdown with ## headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Infrastructure, Documentation, Maintenance, Refactoring, Other
   - Each entry should be a single line with proper PR link formatting

5. **PR Link Format:**
   - Extract PR number from commit message
   - Format as: `([#<number>]({repository_url}/pull/<number>))`
   - Example: `([#456]({repository_url}/pull/456))`
   
6. **Important Notes:**
   - Every commit should be categorized into exactly one category
   - If you cannot determine the appropriate category from labels OR content analysis, place the entry in an "Other" category
   - Do not skip any commits - every entry must appear somewhere in the release notes
   - Prioritize GitHub PR labels over commit message analysis when available

Generate the release notes in category-first format like this example:
## Features
* Feature description ([#123]({repository_url}/pull/123))
* Another feature description ([#124]({repository_url}/pull/124))

## Enhancements
* Enhancement description ([#125]({repository_url}/pull/125))
* Another enhancement description ([#126]({repository_url}/pull/126))

## Bug Fixes
* Bug fix description ([#127]({repository_url}/pull/127))"""
        
        return prompt
    
    def _write_release_notes_to_repo(self, repo: GitRepository, component_name: str, content: str):
        """Write release notes to repository's release-notes directory."""
        release_notes_dir = os.path.join(repo.dir, "release-notes")
        os.makedirs(release_notes_dir, exist_ok=True)
        
        filename = f"{component_name.lower()}.release-notes-{self.version}.md"
        filepath = os.path.join(release_notes_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"# {component_name} {self.version} Release Notes\n\n")
            f.write(content)
        
        logging.info(f"Wrote release notes to {filename}")
    
    def _commit_release_notes(self, repo: GitRepository, component_name: str):
        """Commit release notes changes."""
        try:
            # Create release branch
            branch_name = f"{self.version}-release-notes"
            repo.execute(f"git checkout -b {branch_name}")
            
            # Add and commit
            repo.execute("git add release-notes/")
            repo.execute(f'git commit -m "Add {self.version} release notes for {component_name}"')
            
            logging.info(f"Committed release notes on branch {branch_name}")
            
        except Exception as e:
            logging.warning(f"Failed to commit release notes: {e}")
    
    def generate_summary(self) -> str:
        """Generate workflow summary."""
        total = len(self.processed_components) + len(self.failed_components)
        success_rate = len(self.processed_components) / total * 100 if total > 0 else 0
        
        summary = f"Processed {total} components: {len(self.processed_components)} successful, {len(self.failed_components)} failed ({success_rate:.1f}% success rate)"
        
        if self.failed_components:
            summary += f". Failed: {', '.join(self.failed_components)}"
        
        return summary
