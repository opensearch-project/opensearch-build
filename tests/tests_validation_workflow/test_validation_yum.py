# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, patch

from validation_workflow.yum.validation_yum import ValidateYum


class TestValidationYum(unittest.TestCase):

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=True)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_download_artifacts(self, mock_validation_args: Mock, mock_download: Mock, mock_is_url_valid: Mock) -> None:
        mock_validation_args.return_value.file_path = {"opensearch": "https://opensearch.org/release/2.11.0/opensearch-2.11.0-linux-x64.repo"}
        mock_check_url = MagicMock()
        mock_check_url.return_value = True
        validate_yum = ValidateYum(mock_validation_args.return_value)

        result = validate_yum.download_artifacts()

        self.assertEqual(result, True)

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=False)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    @patch("validation_workflow.validation.Validation.check_url", return_value=False)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_download_artifacts_error(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock, mock_check_url: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.11.0'

        validate_yum = ValidateYum(mock_validation_args.return_value)
        self.assertRaises(Exception, validate_yum.download_artifacts())

    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    @patch('validation_workflow.validation.Validation.check_url')
    def test_copy_artifacts(self, mock_validation_args: Mock, mock_isFilePathEmpty: Mock) -> None:
        mock_isFilePathEmpty.return_value = True
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_validation_args.return_value.file_path = {"opensearch": "/src/files/opensearch.staging.repo"}
        validate_yum = ValidateYum(mock_validation_args.return_value)

        # Call cleanup method
        with patch.object(validate_yum, 'copy_artifact') as mock_copy_artifact:
            mock_copy_artifact.return_value = True
            result = validate_yum.download_artifacts()
            self.assertTrue(result)

    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_exceptions(self, mock_validation_args: Mock) -> None:
        with self.assertRaises(Exception) as e1:
            mock_validation_args.return_value.projects = ["opensearch"]
            mock_validation_args.return_value.file_path = {"opensearch": "/src/files/opensearch.staging.reop"}
            validate_yum = ValidateYum(mock_validation_args.return_value)
            validate_yum.installation()
        self.assertEqual(str(e1.exception), "Failed to Install Opensearch")

        with self.assertRaises(Exception) as e2:
            mock_validation_args.return_value.projects = ["opensearch"]
            validate_yum = ValidateYum(mock_validation_args.return_value)
            validate_yum.start_cluster()
        self.assertEqual(str(e2.exception), "Failed to Start Cluster")

        with self.assertRaises(Exception) as e3:
            mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
            validate_yum = ValidateYum(mock_validation_args.return_value)
            validate_yum.cleanup()
        self.assertIn("Exception occurred either while attempting to stop cluster or removing OpenSearch/OpenSearch-Dashboards.", str(e3.exception))  # noqa: E501

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
    def test_validation(self, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 4)

        # Create instance of ValidateYum class
        validate_yum = ValidateYum(mock_validation_args.return_value)

        # Call validation method and assert the result
        result = validate_yum.validation()
        self.assertTrue(result)

        # Assert that the mock methods are called as expected
        mock_test_apis.assert_called_once()

    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    @patch('validation_workflow.yum.validation_yum.ApiTestCases')
    def test_failed_testcases(self, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 1)

        # Create instance of ValidateRpm class
        validate_yum = ValidateYum(mock_validation_args.return_value)

        # Call validation method and assert the result
        validate_yum.validation()
        self.assertRaises(Exception, "Not all tests Pass : 1")

        # Assert that the mock methods are called as expected
        mock_test_apis.assert_called_once()

    @patch("validation_workflow.yum.validation_yum.execute", return_value=True)
    @patch('validation_workflow.yum.validation_yum.ValidationArgs')
    def test_cleanup(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_yum = ValidateYum(mock_validation_args.return_value)

        result = validate_yum.cleanup()
        self.assertTrue(result)
