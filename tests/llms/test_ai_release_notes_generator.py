#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Tests for AI release notes generator."""

import os
import unittest
import sys
import json
from unittest.mock import patch, MagicMock, mock_open

# We'll use patch instead of sys.modules to mock boto3 and botocore

from llms.ai_release_notes_generator import AIReleaseNotesGenerator


class TestAIReleaseNotesGenerator(unittest.TestCase):
    """Test AI release notes generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.version = "3.2.0"
        self.date = "2025-06-24"
        self.test_mode = True
        
        # Create a mock bedrock client
        self.mock_bedrock_client = MagicMock()
        self.mock_bedrock_response = {
            'body': MagicMock(),
        }
        self.mock_bedrock_response['body'].read.return_value = '{"content": [{"text": "## Test Release Notes\\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))"}]}'
        self.mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response

    @patch('boto3.client')
    def test_create_bedrock_client(self, mock_boto3_client):
        """Test creating Bedrock client."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=self.test_mode
        )
        
        self.assertIsNotNone(generator.bedrock_client)
        mock_boto3_client.assert_called_once_with('bedrock-runtime', region_name='us-east-1')

    @patch('boto3.client')
    @patch('botocore.config.Config')
    def test_generate_ai_release_notes(self, mock_config, mock_boto3_client):
        """Test generating AI release notes."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=self.test_mode
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        repo_name = 'test-component'
        formatted_content = 'Test content'
        
        result = generator._generate_ai_release_notes(repo_name, formatted_content)
        
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    @patch('botocore.config.Config')
    def test_generate_ai_release_notes_with_changelog(self, mock_config, mock_boto3_client):
        """Test generating AI release notes with changelog content."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=self.test_mode
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        repo_name = 'test-component'
        # Create a realistic changelog content
        formatted_content = '''# CHANGELOG
All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased 3.x]
### Added
- Add support for new feature ([#123](https://github.com/opensearch-project/test-component/pull/123))
- Add another feature ([#124](https://github.com/opensearch-project/test-component/pull/124))

### Changed
- Update existing functionality ([#125](https://github.com/opensearch-project/test-component/pull/125))

### Fixed
- Fix bug in component ([#126](https://github.com/opensearch-project/test-component/pull/126))
'''
        
        result = generator._generate_ai_release_notes(repo_name, formatted_content)
        
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    @patch('botocore.config.Config')
    def test_process_success(self, mock_config, mock_boto3_client):
        """Test process method with successful AI generation."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=False  # Not test mode to avoid file saving
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        component_name = 'test-component'
        content = 'Test commit content'
        
        result = generator.process(content, component_name)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['component_name'], component_name)
        self.assertEqual(result['ai_result'], "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        
    @patch('boto3.client')
    @patch('botocore.config.Config')
    def test_generate_ai_release_notes_with_commit_history(self, mock_config, mock_boto3_client):
        """Test generating AI release notes with commit history."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=self.test_mode
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        repo_name = 'test-component'
        # Create a realistic commit history content
        formatted_content = '''abc1234 2025-07-10 Add new feature for component (#123)
def5678 2025-07-09 Fix bug in error handling (#124)
ghi9012 2025-07-08 Update documentation for API (#125)
jkl3456 2025-07-07 Refactor code for better performance (#126)
mno7890 2025-07-06 Add unit tests for new functionality (#127)
pqr1234 2025-07-05 Implement requested changes from review (#128)
stu5678 2025-07-04 Initial implementation of feature (#129)'''
        
        result = generator._generate_ai_release_notes(repo_name, formatted_content)
        
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    @patch('llms.ai_release_notes_generator.AIReleaseNotesGenerator._generate_ai_release_notes')
    def test_process_failure(self, mock_generate, mock_boto3_client):
        """Test process method with AI generation failure."""
        # Set up the mock to return an error message
        mock_generate.return_value = "AI analysis failed after 3 attempts: Test error"
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=False
        )
        
        component_name = 'test-component'
        content = 'Test commit content'
        
        result = generator.process(content, component_name)
        
        self.assertTrue(result['success'])  # The process method will still return success=True
        self.assertEqual(result['component_name'], component_name)
        self.assertIn('AI analysis failed', result['ai_result'])  # But the AI result will contain an error message

    @patch('boto3.client')
    @patch('botocore.config.Config')
    @patch('os.path.abspath')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_file(self, mock_file, mock_makedirs, mock_abspath, mock_config, mock_boto3_client):
        """Test _save_to_file method."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        mock_abspath.return_value = "/mock/project/root"
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=True
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        component_name = 'test-component'
        content = "## Test Release Notes\n* Test item"
        
        generator._save_to_file(component_name, content)
        
        mock_makedirs.assert_called_once_with("/mock/project/root/release-notes", exist_ok=True)
        mock_file.assert_called_once_with("/mock/project/root/release-notes/opensearch-test-component.release-notes-3.2.0.md", 'w')
        mock_file().write.assert_any_call("opensearch-test-component 3.2.0 Release Notes\n\n")
        mock_file().write.assert_any_call(content)

    @patch('boto3.client')
    @patch('botocore.config.Config')
    @patch('os.path.abspath')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_file_opensearch(self, mock_file, mock_makedirs, mock_abspath, mock_config, mock_boto3_client):
        """Test _save_to_file method with OpenSearch component."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        mock_abspath.return_value = "/mock/project/root"
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            test_mode=True
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        component_name = 'OpenSearch'
        content = "## Test Release Notes\n* Test item"
        
        generator._save_to_file(component_name, content)
        
        mock_makedirs.assert_called_once_with("/mock/project/root/release-notes", exist_ok=True)
        mock_file.assert_called_once_with("/mock/project/root/release-notes/opensearch.release-notes-3.2.0.md", 'w')


if __name__ == '__main__':
    unittest.main()
