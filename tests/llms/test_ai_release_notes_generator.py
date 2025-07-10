#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Tests for AI release notes generator."""

import os
import unittest
import sys
from unittest.mock import patch, MagicMock

# Mock boto3 module
sys.modules['boto3'] = MagicMock()
sys.modules['boto3'].client = MagicMock()

from llms.ai_release_notes_generator import AIReleaseNotesGenerator
from manifests.input_manifest import InputComponentFromSource


class TestAIReleaseNotesGenerator(unittest.TestCase):
    """Test AI release notes generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.version = "3.2.0"
        self.date = "2025-06-24"
        self.work_dir = "/tmp/test_work_dir"
        self.test_mode = True
        
        # Create a mock component
        self.component = MagicMock(spec=InputComponentFromSource)
        self.component.name = "test-component"
        self.component.repository = "https://github.com/opensearch-project/test-component.git"
        self.component.ref = "main"
        self.component.working_directory = None
        
        # Create a mock repo
        self.repo = MagicMock()
        self.repo.dir = "/tmp/test_repo_dir"
        
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
            work_dir=self.work_dir,
            test_mode=self.test_mode
        )
        
        self.assertIsNotNone(generator.bedrock_client)
        mock_boto3_client.assert_called_once_with('bedrock-runtime', region_name='us-east-1')

    @patch('boto3.client')
    def test_generate_ai_release_notes(self, mock_boto3_client):
        """Test generating AI release notes."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            work_dir=self.work_dir,
            test_mode=self.test_mode
        )
        
        processed_data = {
            'repo_name': 'test-component',
            'formatted_content': 'Test content'
        }
        
        result = generator._generate_ai_release_notes(processed_data)
        
        self.assertEqual(result, "## Test Release Notes\n* Test item ([#123](https://github.com/opensearch-project/test-component/pull/123))")
        self.mock_bedrock_client.invoke_model.assert_called_once()

    @patch('boto3.client')
    def test_process_repository_content_with_changelog(self, mock_boto3_client):
        """Test processing repository content with CHANGELOG."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            work_dir=self.work_dir,
            test_mode=self.test_mode
        )
        
        # Mock the data processor
        generator.data_processor = MagicMock()
        generator.data_processor.process_repository_content.return_value = {
            'type': 'changelog',
            'repo_name': 'test-component',
            'formatted_content': 'Test content'
        }
        
        result = generator._process_with_repo(self.repo, self.component, 'test-component')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['component_name'], 'test-component')
        self.assertEqual(result['data_type'], 'changelog')
        # DataProcessor now handles CHANGELOG.md detection internally
        generator.data_processor.process_repository_content.assert_called_once()

    @patch('boto3.client')
    def test_process_repository_content_with_commits(self, mock_boto3_client):
        """Test processing repository content with commits."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        
        generator = AIReleaseNotesGenerator(
            github_token=None,
            version=self.version,
            baseline_date=self.date,
            work_dir=self.work_dir,
            test_mode=self.test_mode
        )
        
        # Mock the data processor
        generator.data_processor = MagicMock()
        generator.data_processor.process_repository_content.return_value = {
            'type': 'commits',
            'repo_name': 'test-component',
            'formatted_content': 'Formatted commits',
            'entry_count': 1  # Changed from commit_count to entry_count
        }
        
        result = generator._process_with_repo(self.repo, self.component, 'test-component')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['component_name'], 'test-component')
        self.assertEqual(result['data_type'], 'commits')
        self.assertEqual(result['entry_count'], 1)  # Changed from commit_count to entry_count
        # DataProcessor now handles commit processing internally
        generator.data_processor.process_repository_content.assert_called_once()


if __name__ == '__main__':
    unittest.main()
