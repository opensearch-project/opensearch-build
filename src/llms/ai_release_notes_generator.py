# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import json
import logging
import sys
import time

import boto3
from botocore.exceptions import ClientError, ConnectTimeoutError, NoCredentialsError, ReadTimeoutError

from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs


class AIReleaseNotesGenerator:

    def __init__(self, args: ReleaseNotesCheckArgs, aws_region: str = 'us-east-1'):
        self.aws_region = 'us-east-1'
        self.model_id = args.model_id
        self.max_tokens_override = args.max_tokens
        self.max_retries = 3
        self.base_delay = 1  # Base delay in seconds for exponential backoff

        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=aws_region)
        except NoCredentialsError:
            logging.error("Error: AWS credentials not found. Please configure your AWS credentials.")
            sys.exit(1)

    def _should_retry(self, exception: Exception) -> bool:
        """Determine if the exception warrants a retry"""
        if isinstance(exception, ClientError):
            error_code = exception.response['Error']['Code']
            return error_code in ['ThrottlingException', 'ServiceUnavailable', 'InternalServerError']

        if isinstance(exception, (ReadTimeoutError, ConnectTimeoutError)):
            return True

        return False

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay using exponential backoff with jitter"""
        import random
        delay: float = self.base_delay * (2 ** attempt)
        # Add jitter to avoid thundering herd
        jitter: float = random.uniform(0.1, 0.5)
        return delay + jitter

    def call_bedrock_claude(self, prompt: str) -> str:
        """Call AWS Bedrock Claude Sonnet 3.5 v2 model with retry logic"""

        # Prepare the request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens_override,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        last_exception: Exception = None

        for attempt in range(self.max_retries + 1):
            try:
                # Call Bedrock
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(request_body),
                    contentType="application/json"
                )

                # Parse response
                response_body = json.loads(response['body'].read())
                return str(response_body['content'][0]['text'])

            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                last_exception = e

                if not self._should_retry(e):
                    # Handle non-retryable errors immediately
                    logging.error(f"AWS Bedrock Error ({error_code}): {error_message}")

                    if error_code == "AccessDeniedException":
                        logging.error("Make sure you have proper IAM permissions for Bedrock and the model is enabled in your region.")
                    elif error_code == "ValidationException":
                        logging.error("Check if the Claude Sonnet 3.5 v2 model is available in your region.")

                    sys.exit(1)

                # Handle retryable errors
                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    logging.warning(f"Retryable error ({error_code}): {error_message}. Retrying in {delay:.2f} seconds... (Attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
                else:
                    logging.error(f"Max retries ({self.max_retries}) exceeded for AWS Bedrock Error ({error_code}): {error_message}")

            except (ReadTimeoutError, ConnectTimeoutError) as e:
                last_exception = e

                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    logging.warning(f"Timeout error: {str(e)}. Retrying in {delay:.2f} seconds... (Attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
                else:
                    logging.error(f"Max retries ({self.max_retries}) exceeded for timeout error: {str(e)}")

            except Exception as e:
                # Non-retryable unexpected errors
                logging.error(f"Unexpected error calling Bedrock: {e}")
                sys.exit(1)

        # If we get here, all retries have been exhausted
        logging.error(f"Failed to call Bedrock after {self.max_retries} retries. Last error: {last_exception}")
        sys.exit(1)

    def generate_release_notes(self, prompt: str) -> str:
        # Generate release notes using Claude
        logging.info("Generating release notes using AWS Bedrock Claude Sonnet 3.5 v2...")
        release_notes = self.call_bedrock_claude(prompt)

        return release_notes
