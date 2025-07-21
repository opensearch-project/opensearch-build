#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""AI-powered release notes generator using AWS Bedrock."""

import json
import logging
import os
import boto3
import sys
from typing import Any, Dict
from llms.prompts import AI_RELEASE_NOTES_PROMPT_CHANGELOG, AI_RELEASE_NOTES_PROMPT_COMMIT
from release_notes_workflow.release_notes_component import ReleaseNotesComponents

class AIReleaseNotesGenerator:
    """AI-powered release notes generator using AWS Bedrock."""
    
    def __init__(self, version: str = None, baseline_date: str = None):
        self.version = version
        self.baseline_date = baseline_date
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
            
            self._save_to_file(component_name, ai_result, manifest_path, component)
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
    
    def _save_to_file(self, component_name: str, content: str, manifest_path: str = None, component = None) -> None:
        """Save AI-generated release notes to a file."""
        try:
            project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))
            output_dir = os.path.join(project_root, "release-notes")
            os.makedirs(output_dir, exist_ok=True)
            
            if not component:
                raise ValueError("Component object must be provided")
            
            release_notes_component = ReleaseNotesComponents.from_component(component, self.version, None, project_root)
            filename_suffix = release_notes_component.filename.lstrip('.')
            
            # Get the display name for the release notes file
            manifest_prefix = None
            
            for arg in sys.argv:
                if arg.endswith('.yml') and ('manifest' in arg or (self.version and f'/{self.version}/' in arg)):
                    manifest_filename = os.path.basename(arg)
                    # Extract the name from the filename (e.g., "opensearch" from "opensearch-3.2.0.yml")
                    if manifest_filename.endswith('.yml'):
                        manifest_prefix = manifest_filename.split('-')[0]
                        logging.debug(f"manifest_prefix from command line={manifest_prefix}")
                        break
            
            comp_name = component_name.lower()
            
            if manifest_prefix and manifest_prefix != comp_name:
                display_name = f"{manifest_prefix}-{comp_name}"
            else:
                display_name = comp_name
            filename = f"{display_name}.{filename_suffix}"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"{display_name} {self.version} Release Notes\n\n")
                f.write(content)
            
            logging.info(f"Saved release notes to {filepath}")
        except Exception as e:
            logging.error(f"Failed to save release notes to file: {e}")
    
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
            
            prompt = AI_RELEASE_NOTES_PROMPT_CHANGELOG.format(
                repo_name=repo_name,
                version=self.version,
                repository_url=repository_url
            )
            
            prompt += f"\n\n**CHANGELOG Content:**\n{formatted_content}"
        else:
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
