#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Tests for AI release notes generator."""

import json
import unittest
from unittest.mock import MagicMock, call, patch

from botocore.exceptions import ClientError, ConnectTimeoutError, NoCredentialsError, ReadTimeoutError

from llms.ai_release_notes_generator import AIReleaseNotesGenerator
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs


class TestAIReleaseNotesGenerator(unittest.TestCase):
    """Test AI release notes generator."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create a mock args object
        self.mock_args = MagicMock(spec=ReleaseNotesCheckArgs)
        self.mock_args.model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        self.mock_args.max_tokens = 2000

        # Mock bedrock client
        self.mock_bedrock_client = MagicMock()
        self.mock_response = {
            'body': MagicMock()
        }
        self.mock_response['body'].read.return_value = b'{"content": [{"text": "Generated release notes"}]}'
        self.mock_bedrock_client.invoke_model.return_value = self.mock_response

    @patch('boto3.client')
    def test_init_success(self, mock_boto3_client: MagicMock) -> None:
        """Test successful initialization."""
        mock_boto3_client.return_value = self.mock_bedrock_client

        generator = AIReleaseNotesGenerator(self.mock_args)

        self.assertEqual(generator.aws_region, 'us-east-1')
        self.assertEqual(generator.model_id, "us.anthropic.claude-3-7-sonnet-20250219-v1:0")
        self.assertEqual(generator.max_tokens_override, 2000)
        self.assertEqual(generator.max_retries, 3)
        self.assertEqual(generator.base_delay, 1)
        self.assertEqual(generator.bedrock_client, self.mock_bedrock_client)
        mock_boto3_client.assert_called_once_with('bedrock-runtime', region_name='us-east-1')

    @patch('boto3.client')
    def test_init_with_custom_region(self, mock_boto3_client: MagicMock) -> None:
        """Test initialization with custom AWS region."""
        mock_boto3_client.return_value = self.mock_bedrock_client

        AIReleaseNotesGenerator(self.mock_args, aws_region='eu-west-1')

        mock_boto3_client.assert_called_once_with('bedrock-runtime', region_name='eu-west-1')

    @patch('boto3.client')
    @patch('sys.exit')
    @patch('logging.error')
    def test_init_no_credentials(self, mock_logging: MagicMock, mock_sys_exit: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test initialization when AWS credentials are not found."""
        mock_boto3_client.side_effect = NoCredentialsError()

        AIReleaseNotesGenerator(self.mock_args)

        mock_logging.assert_called_once_with("Error: AWS credentials not found. Please configure your AWS credentials.")
        mock_sys_exit.assert_called_once_with(1)

    def test_should_retry_client_error_retryable(self) -> None:
        """Test _should_retry with retryable ClientError."""
        generator = AIReleaseNotesGenerator(self.mock_args)

        # Test retryable error codes
        for error_code in ['ThrottlingException', 'ServiceUnavailable', 'InternalServerError']:
            client_error = ClientError(
                error_response={'Error': {'Code': error_code, 'Message': 'Test error'}},
                operation_name='invoke_model'
            )
            self.assertTrue(generator._should_retry(client_error))

    def test_should_retry_client_error_non_retryable(self) -> None:
        """Test _should_retry with non-retryable ClientError."""
        generator = AIReleaseNotesGenerator(self.mock_args)

        client_error = ClientError(
            error_response={'Error': {'Code': 'AccessDeniedException', 'Message': 'Test error'}},
            operation_name='invoke_model'
        )
        self.assertFalse(generator._should_retry(client_error))

    def test_should_retry_timeout_errors(self) -> None:
        """Test _should_retry with timeout errors."""
        generator = AIReleaseNotesGenerator(self.mock_args)

        self.assertTrue(generator._should_retry(ReadTimeoutError(endpoint_url='test')))
        self.assertTrue(generator._should_retry(ConnectTimeoutError(endpoint_url='test')))

    def test_should_retry_other_exceptions(self) -> None:
        """Test _should_retry with other exceptions."""
        generator = AIReleaseNotesGenerator(self.mock_args)

        self.assertFalse(generator._should_retry(ValueError("Test error")))
        self.assertFalse(generator._should_retry(Exception("Test error")))

    @patch('random.uniform')
    def test_calculate_delay(self, mock_random: MagicMock) -> None:
        """Test _calculate_delay method."""
        mock_random.return_value = 0.3
        generator = AIReleaseNotesGenerator(self.mock_args)

        # Test exponential backoff
        self.assertEqual(generator._calculate_delay(0), 1.3)  # 1 * 2^0 + 0.3
        self.assertEqual(generator._calculate_delay(1), 2.3)  # 1 * 2^1 + 0.3
        self.assertEqual(generator._calculate_delay(2), 4.3)  # 1 * 2^2 + 0.3

        mock_random.assert_has_calls([call(0.1, 0.5)] * 3)

    @patch('boto3.client')
    def test_call_bedrock_claude_success(self, mock_boto3_client: MagicMock) -> None:
        """Test successful call to Bedrock Claude."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        generator = AIReleaseNotesGenerator(self.mock_args)

        result = generator.call_bedrock_claude("Test prompt")

        self.assertEqual(result, "Generated release notes")

        # Verify the request was made correctly
        expected_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": "Test prompt"}]
        }
        self.mock_bedrock_client.invoke_model.assert_called_once_with(
            modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps(expected_body),
            contentType="application/json"
        )

    @patch('boto3.client')
    @patch('time.sleep')
    def test_call_bedrock_claude_retry_success(self, mock_sleep: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test Bedrock call with retry that eventually succeeds."""
        mock_client = MagicMock()

        # First call fails with retryable error, second succeeds
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException', 'Message': 'Rate exceeded'}},
            operation_name='invoke_model'
        )
        mock_client.invoke_model.side_effect = [throttling_error, self.mock_response]
        mock_boto3_client.return_value = mock_client

        generator = AIReleaseNotesGenerator(self.mock_args)

        result = generator.call_bedrock_claude("Test prompt")

        self.assertEqual(result, "Generated release notes")
        self.assertEqual(mock_client.invoke_model.call_count, 2)
        mock_sleep.assert_called_once()

    @patch('boto3.client')
    @patch('time.sleep')
    @patch('sys.exit')
    @patch('logging.error')
    def test_call_bedrock_claude_max_retries_exceeded(self, mock_logging: MagicMock, mock_sys_exit: MagicMock, mock_sleep: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test Bedrock call when max retries are exceeded."""
        mock_client = MagicMock()

        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException', 'Message': 'Rate exceeded'}},
            operation_name='invoke_model'
        )
        mock_client.invoke_model.side_effect = throttling_error
        mock_boto3_client.return_value = mock_client

        # Make sys.exit raise an exception to stop execution
        mock_sys_exit.side_effect = SystemExit(1)

        generator = AIReleaseNotesGenerator(self.mock_args)

        # Should raise SystemExit after max retries
        with self.assertRaises(SystemExit):
            generator.call_bedrock_claude("Test prompt")

        # Should attempt max_retries + 1 times (initial + 3 retries)
        self.assertEqual(mock_client.invoke_model.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 3)
        mock_logging.assert_called()
        mock_sys_exit.assert_called_with(1)

    @patch('boto3.client')
    @patch('sys.exit')
    @patch('logging.error')
    def test_call_bedrock_claude_access_denied(self, mock_logging: MagicMock, mock_sys_exit: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test Bedrock call with AccessDeniedException."""
        mock_client = MagicMock()

        access_denied_error = ClientError(
            error_response={'Error': {'Code': 'AccessDeniedException', 'Message': 'Access denied'}},
            operation_name='invoke_model'
        )
        mock_client.invoke_model.side_effect = access_denied_error
        mock_boto3_client.return_value = mock_client

        # Make sys.exit raise an exception to stop execution
        mock_sys_exit.side_effect = SystemExit(1)

        generator = AIReleaseNotesGenerator(self.mock_args)

        # Should raise SystemExit due to AccessDeniedException
        with self.assertRaises(SystemExit):
            generator.call_bedrock_claude("Test prompt")

        # Should not retry for AccessDeniedException
        self.assertEqual(mock_client.invoke_model.call_count, 1)
        mock_logging.assert_any_call("AWS Bedrock Error (AccessDeniedException): Access denied")
        mock_logging.assert_any_call("Make sure you have proper IAM permissions for Bedrock and the model is enabled in your region.")
        mock_sys_exit.assert_called_with(1)

    @patch('boto3.client')
    @patch('sys.exit')
    @patch('logging.error')
    def test_call_bedrock_claude_validation_exception(self, mock_logging: MagicMock, mock_sys_exit: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test Bedrock call with ValidationException."""
        mock_client = MagicMock()

        validation_error = ClientError(
            error_response={'Error': {'Code': 'ValidationException', 'Message': 'Invalid model'}},
            operation_name='invoke_model'
        )
        mock_client.invoke_model.side_effect = validation_error
        mock_boto3_client.return_value = mock_client

        # Make sys.exit raise an exception to stop execution
        mock_sys_exit.side_effect = SystemExit(1)

        generator = AIReleaseNotesGenerator(self.mock_args)

        # Should raise SystemExit due to ValidationException
        with self.assertRaises(SystemExit):
            generator.call_bedrock_claude("Test prompt")

        # Should not retry for ValidationException
        self.assertEqual(mock_client.invoke_model.call_count, 1)
        mock_logging.assert_any_call("AWS Bedrock Error (ValidationException): Invalid model")
        mock_logging.assert_any_call("Check if the Claude Sonnet 3.5 v2 model is available in your region.")
        mock_sys_exit.assert_called_with(1)

    @patch('boto3.client')
    @patch('time.sleep')
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.warning')
    def test_call_bedrock_claude_timeout_retry(self, mock_warning: MagicMock, mock_error: MagicMock, mock_sys_exit: MagicMock, mock_sleep: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test Bedrock call with timeout errors and retry."""
        mock_client = MagicMock()

        timeout_error = ReadTimeoutError(endpoint_url='test')
        mock_client.invoke_model.side_effect = timeout_error
        mock_boto3_client.return_value = mock_client

        # Make sys.exit raise an exception to stop execution
        mock_sys_exit.side_effect = SystemExit(1)

        generator = AIReleaseNotesGenerator(self.mock_args)

        # Should raise SystemExit after max retries
        with self.assertRaises(SystemExit):
            generator.call_bedrock_claude("Test prompt")

        # Should retry for timeout errors
        self.assertEqual(mock_client.invoke_model.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 3)
        mock_warning.assert_called()
        mock_error.assert_called()
        mock_sys_exit.assert_called_with(1)

    @patch('boto3.client')
    @patch('sys.exit')
    @patch('logging.error')
    def test_call_bedrock_claude_unexpected_error(self, mock_logging: MagicMock, mock_sys_exit: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test Bedrock call with unexpected error."""
        mock_client = MagicMock()

        unexpected_error = ValueError("Unexpected error")
        mock_client.invoke_model.side_effect = unexpected_error
        mock_boto3_client.return_value = mock_client

        # Make sys.exit raise an exception to stop execution
        mock_sys_exit.side_effect = SystemExit(1)

        generator = AIReleaseNotesGenerator(self.mock_args)

        # Should raise SystemExit due to unexpected error
        with self.assertRaises(SystemExit):
            generator.call_bedrock_claude("Test prompt")

        # Should not retry for unexpected errors
        self.assertEqual(mock_client.invoke_model.call_count, 1)
        mock_logging.assert_called_with("Unexpected error calling Bedrock: Unexpected error")
        mock_sys_exit.assert_called_with(1)

    @patch('boto3.client')
    @patch('logging.info')
    def test_generate_release_notes(self, mock_logging: MagicMock, mock_boto3_client: MagicMock) -> None:
        """Test generate_release_notes method."""
        mock_boto3_client.return_value = self.mock_bedrock_client
        generator = AIReleaseNotesGenerator(self.mock_args)

        result = generator.generate_release_notes("Test prompt")

        self.assertEqual(result, "Generated release notes")
        mock_logging.assert_called_once_with("Generating release notes using AWS Bedrock Claude Sonnet 3.5 v2...")

    @patch('boto3.client')
    def test_call_bedrock_claude_json_parsing(self, mock_boto3_client: MagicMock) -> None:
        """Test JSON response parsing in call_bedrock_claude."""
        # Test with different response structures
        test_responses = [
            {'content': [{'text': 'Simple response'}]},
            {'content': [{'text': 'Response with multiple items'}, {'text': 'Second item'}]},
        ]

        for response_data in test_responses:
            with self.subTest(response=response_data):
                mock_response = {'body': MagicMock()}
                mock_response['body'].read.return_value = json.dumps(response_data).encode()

                mock_client = MagicMock()
                mock_client.invoke_model.return_value = mock_response
                mock_boto3_client.return_value = mock_client

                generator = AIReleaseNotesGenerator(self.mock_args)
                result = generator.call_bedrock_claude("Test prompt")

                self.assertEqual(result, response_data['content'][0]['text'])

    def test_initialization_attributes(self) -> None:
        """Test that all required attributes are properly initialized."""
        generator = AIReleaseNotesGenerator(self.mock_args)

        # Test all instance attributes exist
        self.assertTrue(hasattr(generator, 'aws_region'))
        self.assertTrue(hasattr(generator, 'model_id'))
        self.assertTrue(hasattr(generator, 'max_tokens_override'))
        self.assertTrue(hasattr(generator, 'max_retries'))
        self.assertTrue(hasattr(generator, 'base_delay'))
        self.assertTrue(hasattr(generator, 'bedrock_client'))

    @patch('boto3.client')
    def test_custom_args_parameters(self, mock_boto3_client: MagicMock) -> None:
        """Test initialization with custom args parameters."""
        custom_args = MagicMock(spec=ReleaseNotesCheckArgs)
        custom_args.model_id = "custom-model-id"
        custom_args.max_tokens = 5000

        mock_boto3_client.return_value = self.mock_bedrock_client

        generator = AIReleaseNotesGenerator(custom_args)

        self.assertEqual(generator.model_id, "custom-model-id")
        self.assertEqual(generator.max_tokens_override, 5000)


if __name__ == '__main__':
    unittest.main()
