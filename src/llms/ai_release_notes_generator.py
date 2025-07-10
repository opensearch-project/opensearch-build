#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""AI-powered release notes generator extending existing workflow."""

import json
import logging
import os
import re
import boto3
import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, List
from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource
from release_notes_workflow.data_processor import DataProcessor
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from llms.prompts import AI_RELEASE_NOTES_PROMPT

class ReleaseNotesGenerator:
    """Base release notes generator (following existing pattern)."""
    
    def __init__(self, version: str, work_dir: str):
        self.version = version
        self.work_dir = work_dir
        self.processed_components = []
        self.failed_components = []

class AIReleaseNotesGenerator(ReleaseNotesGenerator):
    """AI-powered release notes generator using AWS Bedrock."""
    
    def __init__(self, github_token: str, version: str, baseline_date: str = None, work_dir: str = None, test_mode: bool = False):
        super().__init__(version, work_dir)
        
        self.github_token = github_token
        self.baseline_date = baseline_date
        self.test_mode = test_mode
        
        # Initialize clients
        self.bedrock_client = self._create_bedrock_client()
        self.data_processor = DataProcessor()
        
        # Set baseline date
        if not self.baseline_date:
            self.baseline_date = "2025-01-01"  # Default baseline
        self.baseline_tag = "custom"
    
    def _create_bedrock_client(self):
        """Create AWS Bedrock client."""
        try:
            return boto3.client('bedrock-runtime', region_name='us-east-1')
        except Exception as e:
            logging.error(f"Failed to create Bedrock client: {e}")
            raise RuntimeError(f"Failed to create Bedrock client: {e}")
    
    
    def process_repository(self, component: InputComponentFromSource, existing_repo_dir: str = None) -> Dict[str, Any]:
        """Process individual repository and generate release notes."""
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
                using_context_manager = False
            else:
                # Checkout repository using existing GitRepository
                repo = GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(self.work_dir, repo_name),
                    component.working_directory
                )
                using_context_manager = True
                
            # Use context manager if we created the repo
            if using_context_manager:
                with repo as repo_ctx:
                    return self._process_with_repo(repo_ctx, component, repo_name)
            else:
                return self._process_with_repo(repo, component, repo_name)
                
        except Exception as e:
            logging.error(f"Failed to process {component.name}: {e}")
            self.failed_components.append(component.name)
            return {
                'success': False,
                'error': str(e),
                'repo_name': repo_name
            }
    
    def _process_with_repo(self, repo, component: InputComponentFromSource, repo_name: str) -> Dict[str, Any]:
        """Process repository with an active repo object."""
        try:
            # Step 2: Process repository content using DataProcessor
            processed_data = self.data_processor.process_repository_content(repo, repo_name, self.baseline_date)
            
            # Step 3: Generate AI-powered release notes
            if not self.bedrock_client:
                logging.warning(f"No Bedrock client available, skipping AI analysis for {repo_name}")
                return {
                    'success': False,
                    'error': 'No Bedrock client available',
                    'repo_name': repo_name
                }
            
            ai_result = self._generate_ai_release_notes(processed_data)
            
            # Check if AI analysis succeeded
            if not ai_result or ai_result.startswith("AI analysis failed"):
                logging.warning(f"❌ AI analysis failed for {repo_name}: {ai_result}")
                return {
                    'success': False,
                    'error': f'AI analysis failed: {ai_result}',
                    'repo_name': repo_name
                }
            
            # Step 4: Create PR with release notes if not in test mode
            if not self.test_mode:
                # Create PR with the changes
                self._create_release_notes_pr(repo, component.name, ai_result)
            else:
                logging.info(f"🧪 TEST MODE: Skipping file writing for {repo_name}")
                # Save output to local file if in test mode
                manifest_path = getattr(component, 'manifest_path', None)
                self._save_test_output(component, self.version, {'ai_result': ai_result}, manifest_path)
            
            self.processed_components.append(component.name)
            
            return {
                'success': True,
                'repo_name': repo_name,
                'component_name': component.name,
                'data_type': processed_data['type'],
                'entry_count': processed_data.get('entry_count', processed_data.get('commit_count', 0)),
                'ai_result': ai_result
            }
                
        except Exception as e:
            logging.error(f"Failed to process {component.name}: {e}")
            self.failed_components.append(component.name)
            return {
                'success': False,
                'error': str(e),
                'repo_name': repo_name
            }
    
    def _generate_ai_release_notes(self, processed_data: Dict[str, Any]) -> str:
        """Generate release notes using AI."""
        if not self.bedrock_client:
            return "AI analysis not available"
        
        prompt = self._create_ai_prompt(processed_data)
        
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10000,
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
    
    
    def _create_ai_prompt(self, processed_data: Dict[str, Any]) -> str:
        """Create AI prompt adapted for single-component modular workflow."""
        repo_name = processed_data['repo_name']
        repository_url = f"https://github.com/opensearch-project/{repo_name}"
        
        # Use the prompt from prompts.py
        prompt = AI_RELEASE_NOTES_PROMPT.format(
            repo_name=repo_name,
            version=self.version,
            repository_url=repository_url,
            formatted_content=processed_data['formatted_content']
        )
        
        return prompt
    
    def _create_release_notes_pr(self, repo: GitRepository, component_name: str, content: str) -> None:
        """Create a pull request with the release notes."""
        try:
            logging.info(f"Creating PR for {component_name} release notes")
            
            # Step 1: Write release notes to file
            release_notes_dir = os.path.join(repo.dir, "release-notes")
            os.makedirs(release_notes_dir, exist_ok=True)
            
            filename = f"{component_name.lower()}.release-notes-{self.version}.md"
            filepath = os.path.join(release_notes_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"# {component_name} {self.version} Release Notes\n\n")
                f.write(content)
            
            logging.info(f"Wrote release notes to {filename}")
            
            # Step 2: Create branch and commit changes
            branch_name = f"{self.version}-release-notes"
            repo.execute(f"git checkout -b {branch_name}")
            
            # Add and commit
            repo.execute("git add release-notes/")
            repo.execute(f'git commit -m "Add {self.version} release notes for {component_name}"')
            
            logging.info(f"Committed release notes on branch {branch_name}")
            
            # Step 3: Push branch and provide PR URL
            # Extract repository information
            repo_url = repo.url
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            org_name = repo_url.rstrip('/').split('/')[-2]
            
            # Push the branch to remote
            logging.info(f"Pushing branch {branch_name} to remote")
            repo.execute(f"git push -u origin {branch_name}")
            
            # Print instructions for creating PR manually
            pr_url = f"https://github.com/{org_name}/{repo_name}/compare/main...{branch_name}?expand=1"
            logging.info(f"Branch pushed successfully. Create a PR manually at: {pr_url}")
            
        except Exception as e:
            logging.error(f"Failed to create PR: {e}")
    
    def _save_test_output(self, component: InputComponentFromSource, build_version: str, 
                         ai_result: Dict[str, Any], manifest_path: str = None) -> None:
        """Save test output to a local file."""
        # Extract manifest name from path
        manifest_name = "opensearch"  # Default
        if manifest_path:
            manifest_filename = os.path.basename(manifest_path)
            if '-' in manifest_filename:
                parts = manifest_filename.split('-')
                manifest_parts = []
                for part in parts:
                    if not any(char.isdigit() for char in part) or part in ['dashboards']:
                        manifest_parts.append(part)
                    else:
                        break
                manifest_name = '-'.join(manifest_parts) if manifest_parts else "opensearch"
        
        # Generate filename
        repo_name = component.repository.rstrip('/').split('/')[-1].replace('.git', '').lower()
        local_filename = f"{manifest_name}-{repo_name}.release-notes-{build_version}.md"
        
        # Save to the original working directory, not the temporary directory
        original_cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        output_path = os.path.join(original_cwd, local_filename)
        
        # Print current working directory and absolute path
        print(f"Current working directory: {os.getcwd()}")
        print(f"Creating file at absolute path: {output_path}")
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(f"# {component.name} {build_version} Release Notes\n\n")
            f.write(ai_result['ai_result'])
        
        logging.info(f"🧪 TEST MODE: Saved release notes locally to {local_filename}")
