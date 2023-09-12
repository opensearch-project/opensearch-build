# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from validation_workflow.yum.validation_yum import ValidateYum


class TestValidationYum(unittest.TestCase):

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=True)
    @patch("validation_workflow.validation.Validation.check_url", return_value=True)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_download_artifacts(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock, mock_check_url: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]
        mock_validation_args.return_value.artifact_type.return_value = 'staging'

        validate_yum = ValidateYum(mock_validation_args)

        result = validate_yum.download_artifacts()

        self.assertEqual(result, True)

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=False)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    @patch("validation_workflow.validation.Validation.check_url", return_value=False)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_download_artifacts_error(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock, mock_check_url: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.11.0'
        url = "https://opensearch.org/release/2.11.0/opensearch-2.11.0-linux-x64.repo"

        validate_yum = ValidateYum(mock_validation_args)

        self.assertRaises(Exception, validate_yum.check_url(url))

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=False)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    @patch("validation_workflow.validation.Validation.check_url", return_value=False)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_local_artifacts_(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock, mock_check_url: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.1.0'
        mock_validation_args.return_value.artifact_type.return_value = 'staging'

        url = "home/dev/opensearch-2.1.0-linux-x64.repo"

        validate_yum = ValidateYum(mock_validation_args)

        self.assertRaises(Exception, validate_yum.check_url(url))

    @patch("validation_workflow.yum.validation_yum.execute", return_value=True)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_installation(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.arch.return_value = 'x64'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_yum = ValidateYum(mock_validation_args.return_value)

        result = validate_yum.installation()
        self.assertTrue(result)

    @patch("validation_workflow.yum.validation_yum.execute", return_value=True)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    @patch('time.sleep')
    def test_start_cluster(self, mock_validation_args: Mock, mock_execute: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_yum = ValidateYum(mock_validation_args.return_value)

        result = validate_yum.start_cluster()
        self.assertTrue(result)

    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    @patch('validation_workflow.yum.validation_yum.ApiTestCases')
    def test_validation(self, mock_test_cases: Mock, mock_validation_args: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_cases_instance = mock_test_cases.return_value
        mock_test_cases_instance.test_cases.return_value = (True, 4)

        # Create instance of ValidateYum class
        validate_yum = ValidateYum(mock_validation_args.return_value)

        # Call validation method and assert the result
        result = validate_yum.validation()
        self.assertTrue(result)

        # Assert that the mock methods are called as expected
        mock_test_cases.assert_called_once()

    @patch("validation_workflow.yum.validation_yum.execute", return_value=True)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_cleanup(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_yum = ValidateYum(mock_validation_args.return_value)

        result = validate_yum.cleanup()
        self.assertTrue(result)
