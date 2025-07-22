#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Tests for AI release notes generator."""

import os
import unittest
import sys
import json
import importlib
import requests
from packaging import version
from unittest.mock import patch, MagicMock, mock_open, call

from llms.ai_release_notes_generator import AIReleaseNotesGenerator
from release_notes_workflow.release_notes_component import ReleaseNotesComponents


class TestAIReleaseNotesGenerator(unittest.TestCase):
    """Test AI release notes generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.version = "3.2.0"
        self.date = "2025-06-24"
        
        # Create a mock bedrock client
        self.mock_bedrock_client = MagicMock()
        self.mock_bedrock_response = {
            'body': MagicMock(),
        }
        self.mock_bedrock_response['body'].read.return_value = '{"content": [{"text": "## Test Release Notes\\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))"}]}'
        self.mock_bedrock_client.invoke_model.return_value = self.mock_bedrock_response
        
        # Create a mock component
        self.mock_component = MagicMock()
        self.mock_component.name = "test-component"
        self.mock_component.repository = "https://github.com/opensearch-project/test-component"

    @patch('boto3.client')
    def test_create_bedrock_client(self, mock_boto3_client):
        """Test creating Bedrock client."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        self.assertIsNotNone(generator.bedrock_client)
        mock_boto3_client.assert_called_once_with('bedrock-runtime', region_name='us-east-1')

    @patch('boto3.client')
    @patch('botocore.config.Config')
    def test_generate_ai_release_notes_with_different_content(self, mock_config, mock_boto3_client):
        """Test generating AI release notes with different types of content."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        generator.bedrock_client = self.mock_bedrock_client
        
        repo_name = 'test-component'
        
        formatted_content = 'Test content'
        result = generator._generate_ai_release_notes(repo_name, formatted_content, self.mock_component)
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()
        
        # Reset mock for next test
        self.mock_bedrock_client.invoke_model.reset_mock()
        
        changelog_content = '''# CHANGELOG
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
        result = generator._generate_ai_release_notes(repo_name, changelog_content, self.mock_component)
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()
        
        # Reset mock for next test
        self.mock_bedrock_client.invoke_model.reset_mock()
        
        commit_history_content = '''abc1234 2025-07-10 Add new feature for component (#123)
def5678 2025-07-09 Fix bug in error handling (#124)
ghi9012 2025-07-08 Update documentation for API (#125)
jkl3456 2025-07-07 Refactor code for better performance (#126)
mno7890 2025-07-06 Add unit tests for new functionality (#127)
pqr1234 2025-07-05 Implement requested changes from review (#128)
stu5678 2025-07-04 Initial implementation of feature (#129)'''
        
        result = generator._generate_ai_release_notes(repo_name, commit_history_content, self.mock_component)
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    @patch('botocore.config.Config')
    @patch('llms.ai_release_notes_generator.AIReleaseNotesGenerator._save_to_file')
    def test_process_success(self, mock_save_to_file, mock_config, mock_boto3_client):
        """Test process method with successful AI generation."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        generator.bedrock_client = self.mock_bedrock_client
        component_name = 'test-component'
        content = 'Test commit content'
        result = generator.process(content, component_name, None, None, self.mock_component)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['component_name'], component_name)
        self.assertEqual(result['ai_result'], "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        mock_save_to_file.assert_called_once_with(component_name, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))", None, self.mock_component)
        
    @patch('boto3.client')
    @patch('botocore.config.Config')
    def test_generate_ai_release_notes_with_commit_history(self, mock_config, mock_boto3_client):
        """Test generating AI release notes with commit history."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_config.return_value = MagicMock()
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        generator.bedrock_client = self.mock_bedrock_client
        repo_name = 'test-component'
        formatted_content = '''abc1234 2025-07-10 Add new feature for component (#123)
def5678 2025-07-09 Fix bug in error handling (#124)
ghi9012 2025-07-08 Update documentation for API (#125)
jkl3456 2025-07-07 Refactor code for better performance (#126)
mno7890 2025-07-06 Add unit tests for new functionality (#127)
pqr1234 2025-07-05 Implement requested changes from review (#128)
stu5678 2025-07-04 Initial implementation of feature (#129)'''
        result = generator._generate_ai_release_notes(repo_name, formatted_content, self.mock_component)
        
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    @patch('llms.ai_release_notes_generator.AIReleaseNotesGenerator._generate_ai_release_notes')
    def test_process_failure(self, mock_generate, mock_boto3_client):
        """Test process method with AI generation failure."""
        # Set up the mock to return an error message
        mock_generate.side_effect = Exception("Test error")
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        component_name = 'test-component'
        content = 'Test commit content'
        result = generator.process(content, component_name, None, None, self.mock_component)
        
        self.assertFalse(result['success'])  # The process method should return success=False on exception
        self.assertEqual(result['component_name'], component_name)
        self.assertIn('Test error', result['error'])

    @patch('boto3.client')
    @patch('os.path.abspath')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('release_notes_workflow.release_notes_component.ReleaseNotesComponents.from_component')
    @patch('sys.argv', ["script.py", "manifests/3.2.0/opensearch-3.2.0.yml"])
    def test_save_to_file_scenarios(self, mock_from_component, mock_file, mock_makedirs, mock_abspath, mock_boto3_client):
        """Test _save_to_file method with different scenarios."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_abspath.return_value = "/mock/project/root"
        mock_release_notes_component = MagicMock()
        mock_release_notes_component.filename = ".release-notes-3.2.0.md"
        mock_from_component.return_value = mock_release_notes_component
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        # Mock the boto3.client with config
        generator.bedrock_client = self.mock_bedrock_client
        
        component_name = 'test-component'
        content = "## Test Release Notes\n* Test item"
        
        generator._save_to_file(component_name, content, None, self.mock_component)
        
        mock_makedirs.assert_called_once_with("/mock/project/root/release-notes", exist_ok=True)
        mock_from_component.assert_called_once_with(self.mock_component, self.version, None, "/mock/project/root")
        mock_file.assert_called_once()
        mock_file().write.assert_any_call(f"opensearch-{component_name} {self.version} Release Notes\n\n")
        mock_file().write.assert_any_call(content)
        
        # Reset mocks for next test
        mock_makedirs.reset_mock()
        mock_from_component.reset_mock()
        mock_file.reset_mock()
        
        mock_opensearch_component = MagicMock()
        mock_opensearch_component.name = "OpenSearch"
        mock_opensearch_component.repository = "https://github.com/opensearch-project/OpenSearch"
        
        component_name = 'OpenSearch'
        content = "## Test Release Notes\n* Test item"
        
        generator._save_to_file(component_name, content, None, mock_opensearch_component)
        
        mock_makedirs.assert_called_once_with("/mock/project/root/release-notes", exist_ok=True)
        mock_from_component.assert_called_once_with(mock_opensearch_component, self.version, None, "/mock/project/root")
        mock_file.assert_called_once()
        
        # Reset mocks for next test
        mock_makedirs.reset_mock()
        mock_from_component.reset_mock()
        mock_file.reset_mock()
        
        component_name = 'test-component'
        content = "## Test Release Notes\n* Test item"
            
        generator._save_to_file(component_name, content, "manifests/3.2.0/opensearch-3.2.0.yml", self.mock_component)
        
        mock_makedirs.assert_called_once_with("/mock/project/root/release-notes", exist_ok=True)
        mock_from_component.assert_called_once_with(self.mock_component, self.version, None, "/mock/project/root")
        mock_file.assert_called_once()
        mock_file().write.assert_any_call(f"opensearch-{component_name} {self.version} Release Notes\n\n")
        mock_file().write.assert_any_call(content)


    @patch('boto3.client')
    def test_create_bedrock_client_failure(self, mock_boto3_client):
        """Test creating Bedrock client when it fails."""
        mock_boto3_client.side_effect = Exception("Failed to create client")
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        # The client should be None, but the constructor should not fail
        self.assertIsNone(generator.bedrock_client)

    @patch('boto3.client')
    @patch('os.path.abspath')
    @patch('os.makedirs')
    @patch('logging.error')
    def test_save_to_file_no_component(self, mock_logging_error, mock_makedirs, mock_abspath, mock_boto3_client):
        """Test _save_to_file method when component is not provided."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_abspath.return_value = "/mock/project/root"
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        component_name = 'test-component'
        content = "## Test Release Notes\n* Test item"
        
        # Call the method with no component
        generator._save_to_file(component_name, content, None, None)
        mock_logging_error.assert_called_with("Failed to save release notes to file: Component object must be provided")

    @patch('boto3.client')
    def test_generate_ai_release_notes_no_bedrock_client(self, mock_boto3_client):
        """Test generating AI release notes when Bedrock client is not available."""
        # Set up the mock to return None
        mock_boto3_client.return_value = None
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        # Ensure the client is None
        self.assertIsNone(generator.bedrock_client)
        
        repo_name = 'test-component'
        formatted_content = 'Test content'
        
        # The method should return a fallback message
        result = generator._generate_ai_release_notes(repo_name, formatted_content, self.mock_component)
        self.assertEqual(result, "AI analysis not available")

    @patch('boto3.client')
    @patch('time.sleep')
    def test_generate_ai_release_notes_with_retries(self, mock_sleep, mock_boto3_client):
        """Test generating AI release notes with retries."""
        mock_client = MagicMock()
        mock_client.invoke_model.side_effect = [
            Exception("First failure"),
            Exception("Second failure"),
            self.mock_bedrock_response
        ]
        mock_boto3_client.return_value = mock_client
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        repo_name = 'test-component'
        formatted_content = 'Test content'
        
        # The method should succeed on the third try
        result = generator._generate_ai_release_notes(repo_name, formatted_content, self.mock_component)
        
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.assertEqual(mock_client.invoke_model.call_count, 3)
        mock_sleep.assert_called_with(10)

    @patch('boto3.client')
    def test_generate_ai_release_notes_with_git_suffix(self, mock_boto3_client):
        """Test generating AI release notes with repository URL ending in .git."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        mock_component_with_git = MagicMock()
        mock_component_with_git.name = "test-component"
        mock_component_with_git.repository = "https://github.com/opensearch-project/test-component.git"
        repo_name = 'test-component'
        formatted_content = 'Test content'
        result = generator._generate_ai_release_notes(repo_name, formatted_content, mock_component_with_git)
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    @patch('os.path.abspath')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('release_notes_workflow.release_notes_component.ReleaseNotesComponents.from_component')
    @patch('os.path.basename')
    def test_save_to_file_with_manifest_path(self, mock_basename, mock_from_component, mock_file, mock_makedirs, mock_abspath, mock_boto3_client):
        """Test _save_to_file method with manifest path provided."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        mock_abspath.return_value = "/mock/project/root"
        # We need to mock basename to return the correct filename
        mock_basename.return_value = "opensearch-3.2.0.yml"
        original_argv = sys.argv
        
        try:
            sys.argv = ["script.py", "manifests/opensearch-dashboards-3.2.0.yml"]
            
            # Create a mock release notes component
            mock_release_notes_component = MagicMock()
            mock_release_notes_component.filename = ".release-notes-3.2.0.md"
            mock_from_component.return_value = mock_release_notes_component
            
            generator = AIReleaseNotesGenerator(
                version=self.version,
                baseline_date=self.date
            )
            
            component_name = 'test-component'
            content = "## Test Release Notes\n* Test item"
            manifest_path = "manifests/opensearch-dashboards-3.2.0.yml"
            
            # Call the method with the manifest path
            generator._save_to_file(component_name, content, manifest_path, self.mock_component)
            
            mock_makedirs.assert_called_once_with("/mock/project/root/release-notes", exist_ok=True)
            mock_from_component.assert_called_once_with(self.mock_component, self.version, None, "/mock/project/root")
            mock_file.assert_called_once()
            mock_file().write.assert_any_call(f"opensearch-{component_name} {self.version} Release Notes\n\n")
            mock_file().write.assert_any_call(content)
        finally:
            # Restore the original sys.argv
            sys.argv = original_argv


    @patch('boto3.client')
    @patch('time.sleep')
    def test_generate_ai_release_notes_access_denied(self, mock_sleep, mock_boto3_client):
        """Test generating AI release notes when user doesn't have access to the AWS Bedrock model."""
        # Create a mock client that raises an AccessDeniedException
        mock_client = MagicMock()
        access_denied_exception = Exception("AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel")
        # Set up the mock to raise the exception for all 3 retry attempts
        mock_client.invoke_model.side_effect = [
            access_denied_exception,
            access_denied_exception,
            access_denied_exception
        ]
        mock_boto3_client.return_value = mock_client
        
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        repo_name = 'test-component'
        formatted_content = 'Test content'
        
        # The method should handle the access denied exception and return an error message
        result = generator._generate_ai_release_notes(repo_name, formatted_content, self.mock_component)
        
        self.assertIn("AI analysis failed", result)
        self.assertIn("AccessDeniedException", result)
        self.assertEqual(mock_client.invoke_model.call_count, 3)
        mock_sleep.assert_called_with(10)


    def test_boto3_version_for_bedrock(self):
        """Test that boto3 version is sufficient for AWS Bedrock support.
        
        AWS Bedrock requires boto3 version 1.28.57 or higher.
        """
        try:
            boto3 = importlib.import_module('boto3')
            boto3_version = boto3.__version__
            
            # Check if boto3 version is sufficient for AWS Bedrock
            self.assertTrue(
                version.parse(boto3_version) >= version.parse('1.28.57'),
                f"boto3 version {boto3_version} is too old for AWS Bedrock support. Required: boto3>=1.28.57"
            )
            
            print(f"\nboto3 version: {boto3_version} ✅ (sufficient for AWS Bedrock support)")
        except ImportError:
            self.fail("boto3 is not installed")
    
    def test_real_bedrock_access(self):
        """Test that the user has access to AWS Bedrock.
        
        This is an integration test that actually tries to connect to AWS Bedrock
        using the user's credentials. It will be skipped if the SKIP_INTEGRATION_TESTS
        environment variable is set.
        """
        # Skip this test if the SKIP_INTEGRATION_TESTS environment variable is set
        if os.environ.get('SKIP_INTEGRATION_TESTS'):
            self.skipTest("Skipping integration test")
        
        # Create a real AIReleaseNotesGenerator instance
        generator = AIReleaseNotesGenerator(
            version=self.version,
            baseline_date=self.date
        )
        
        # Check if the Bedrock client was created successfully
        self.assertIsNotNone(generator.bedrock_client, "Failed to create Bedrock client. Check your AWS credentials.")
        
        # Try to invoke the model with a simple prompt
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0
            }
            
            response = generator.bedrock_client.invoke_model(
                modelId='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
                body=json.dumps(body),
                contentType='application/json'
            )
            
            # If we get here, the user has access to Bedrock
            self.assertIsNotNone(response)
            self.assertIn('body', response)
            result = json.loads(response['body'].read())
            self.assertIn('content', result)
            
            print("\nAWS Bedrock access test passed. You have access to the Claude model.")
        except Exception as e:
            self.fail(f"Failed to invoke Bedrock model: {e}")


if __name__ == '__main__':
    unittest.main()
