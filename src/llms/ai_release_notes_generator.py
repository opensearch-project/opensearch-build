#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""AI-powered release notes generator using AWS Bedrock."""

import json
import logging
import os
import boto3
import sys
import yaml
import subprocess
from typing import Any, Dict
from git.git_repository import GitRepository
from system.temporary_directory import TemporaryDirectory
from llms.prompts import AI_RELEASE_NOTES_PROMPT_CHANGELOG, AI_RELEASE_NOTES_PROMPT_COMMIT
from release_notes_workflow.release_notes_component import ReleaseNotesComponents

class AIReleaseNotesGenerator:
    """AI-powered release notes generator using AWS Bedrock."""
    
    def __init__(self, github_token: str = None, version: str = None, baseline_date: str = None, work_dir: str = None, test_mode: bool = False):
        self.version = version
        self.baseline_date = baseline_date
        self.test_mode = test_mode
        self.bedrock_client = self._create_bedrock_client()
    
    def _create_bedrock_client(self):
        """Create AWS Bedrock client."""
        try:
            return boto3.client('bedrock-runtime', region_name='us-east-1')
        except Exception as e:
            logging.error(f"Failed to create Bedrock client: {e}")
            logging.warning("Continuing without Bedrock client - will use mock responses for testing")
            return None
    
    def process(self, content: str, component_name: str, manifest_path: str = None, repo = None, component = None) -> Dict[str, Any]:
        """Generate AI-powered release notes from processed content."""
        logging.info(f"Generating AI release notes for {component_name}")
        
        try:
            # Generate AI-powered release notes
            ai_result = self._generate_ai_release_notes(component_name, content, component)
            
            # Save to file if test_mode is True
            if self.test_mode:
                self._save_to_file(component_name, ai_result, manifest_path, component)
                return {
                    'success': True,
                    'component_name': component_name,
                    'ai_result': ai_result
                }
            else:
                # Create PR to the component repository
                self._pr_to_repo(component_name, ai_result, repo, component)
                return {
                    'success': True,
                    'component_name': component_name,
                    'ai_result': ai_result
                }
        
        except Exception as e:
            logging.error(f"Failed to generate AI release notes for {component_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'component_name': component_name
            }
    
    def _get_display_name(self, component_name: str, repo = None) -> str:
        """
        Get the display name for the release notes file.
        
        Args:
            component_name: The name of the component
            repo: Optional repository object, used as fallback for getting prefix
            
        Returns:
            The display name to use for the release notes file (e.g., "opensearch-sql")
        """
        manifest_prefix = None
        
        for arg in sys.argv:
            if arg.endswith('.yml') and ('manifest' in arg or (self.version and f'/{self.version}/' in arg)):
                manifest_filename = os.path.basename(arg)
                # Extract the name from the filename (e.g., "opensearch" from "opensearch-3.2.0.yml")
                if manifest_filename.endswith('.yml'):
                    manifest_prefix = manifest_filename.split('-')[0]
                    print(f"DEBUG: manifest_prefix from command line={manifest_prefix}")
                    break
        
        # Use the component name for the display name
        comp_name = component_name.lower()
        
        # Combine the manifest prefix and component name
        if manifest_prefix and manifest_prefix != comp_name:
            display_name = f"{manifest_prefix}-{comp_name}"
        else:
            display_name = comp_name
            
        return display_name
    
    def _save_to_file(self, component_name: str, content: str, manifest_path: str = None, component = None) -> None:
        """Save AI-generated release notes to a file."""
        try:
            project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))
            output_dir = os.path.join(project_root, "release-notes")
            os.makedirs(output_dir, exist_ok=True)
            
            if not component:
                raise ValueError("Component object must be provided")
            
            # Use ReleaseNotesComponents to get the correct filename suffix
            release_notes_component = ReleaseNotesComponents.from_component(component, self.version, None, project_root)
            filename_suffix = release_notes_component.filename.lstrip('.')
            display_name = self._get_display_name(component_name, None)
            filename = f"{display_name}.{filename_suffix}"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"{display_name} {self.version} Release Notes\n\n")
                f.write(content)
            
            logging.info(f"Saved release notes to {filepath}")
            print(f"Saved release notes to {filepath}")
        except Exception as e:
            logging.error(f"Failed to save release notes to file: {e}")
            print(f"ERROR: Failed to save release notes to file: {e}")
    
    def _generate_ai_release_notes(self, repo_name: str, formatted_content: str, component = None) -> str:
        """Generate release notes using AI."""
        if not self.bedrock_client:
            return "AI analysis not available"
        
        # Component must have a repository attribute
        assert component and hasattr(component, 'repository'), "Component must have a repository attribute"
        repository_url = component.repository.rstrip('/').removesuffix('.git')
        
        # Determine which prompt to use based on content type
        if "CHANGELOG" in formatted_content:
            logging.info(f"Using CHANGELOG for {repo_name}, content length: {len(formatted_content)}")
            
            # For CHANGELOG, we need to add the content separately since it's not in the prompt template
            prompt = AI_RELEASE_NOTES_PROMPT_CHANGELOG.format(
                repo_name=repo_name,
                version=self.version,
                repository_url=repository_url
            )
            
            # Add the formatted_content to the prompt
            prompt += f"\n\n**CHANGELOG Content:**\n{formatted_content}"
        else:
            # For commit data, the formatted_content is included in the prompt template
            prompt = AI_RELEASE_NOTES_PROMPT_COMMIT.format(
                repo_name=repo_name,
                version=self.version,
                repository_url=repository_url,
                formatted_content=formatted_content
            )
        
        # Try to use AWS Bedrock with retries
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 10000,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0
                }
                
                # Create a new client with the updated config
                bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
                
                response = bedrock_client.invoke_model(
                    modelId='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
                    body=json.dumps(body),
                    contentType='application/json'
                )
                
                result = json.loads(response['body'].read())
                return result['content'][0]['text']
                
            except Exception as e:
                retry_count += 1
                logging.warning(f"AI analysis attempt {retry_count} failed: {e}")
                if retry_count < max_retries:
                    logging.info(f"Retrying in 10 seconds...")
                    import time
                    time.sleep(10)
                else:
                    logging.error(f"All AI analysis attempts failed: {e}")
                    return f"AI analysis failed after {max_retries} attempts: {e}"
        
        # This should not be reached, but just in case
        return "AI analysis failed due to unexpected error"
    
    def _pr_to_repo(self, component_name: str, content: str, repo = None, component = None) -> None:
        """Makes a PR with AI-generated release notes to the component's repository."""
        try:
            if not component:
                raise ValueError("Component object must be provided")
            
            repository_url = component.repository
            print(f"DEBUG: Using repository URL: {repository_url}")
            
            if not repo:
                raise ValueError("Repository object must be provided")
                
            repo_dir = repo.dir
            current_branch = repo.output("git rev-parse --abbrev-ref HEAD")
            branch_name = f"release-notes-{self.version}"

            try:
                repo.execute(f"git checkout -b {branch_name}", repo_dir)
            except subprocess.CalledProcessError:
                repo.execute(f"git checkout {branch_name}", repo_dir)

            release_notes_component = ReleaseNotesComponents.from_component(component, self.version, None, repo_dir)
            
            if not release_notes_component.path_exists():
                os.makedirs(release_notes_component.path, exist_ok=True)
            
            filename_suffix = release_notes_component.filename.lstrip('.')
            display_name = self._get_display_name(component_name, repo)
            filename = f"{display_name}.{filename_suffix}"
            release_notes_path = os.path.join(release_notes_component.path, filename)

            with open(release_notes_path, 'w') as f:
                f.write(f"{display_name} {self.version} Release Notes\n\n")
                f.write(content)
            
            repo.execute("git add release-notes/", repo_dir)
            repo.execute(f'git commit -m "Add {self.version} release notes for {component_name}"', repo_dir)
            
            # Push the branch
            try:
                repo.execute(f"git push origin {branch_name}", repo_dir)
                
                # Create a PR using the GitHub CLI if available
                try:
                    pr_title = f"Add {self.version} release notes for {component_name}"
                    pr_body = f"Automatically generated release notes for {component_name} {self.version}"
                    
                    # Check if gh CLI is available
                    subprocess.check_call("which gh > /dev/null 2>&1", shell=True)
                    
                    # Create the PR
                    pr_cmd = f'cd {repo_dir} && gh pr create --title "{pr_title}" --body "{pr_body}" --base main --head {branch_name}'
                    pr_output = subprocess.check_output(pr_cmd, shell=True).decode().strip()
                    
                    logging.info(f"Created PR: {pr_output}")
                    print(f"Created PR: {pr_output}")
                except subprocess.CalledProcessError:
                    # GitHub CLI not available or PR creation failed
                    logging.warning("GitHub CLI not available or PR creation failed. Please create the PR manually.")
                    print(f"Branch {branch_name} pushed to {repository_url}. Please create a PR manually.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to push branch: {e}")
                print(f"Failed to push branch: {e}")
            
            try:
                repo.execute(f"git checkout {current_branch}", repo_dir)
            except subprocess.CalledProcessError:
                logging.warning(f"Failed to return to original branch {current_branch}")
            
            logging.info(f"Release notes for {component_name} prepared for PR")
            
        except Exception as e:
            logging.error(f"Failed to create PR for {component_name}: {e}")
            print(f"ERROR: Failed to create PR: {e}")
