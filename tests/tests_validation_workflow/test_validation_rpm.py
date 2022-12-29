# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from validation_workflow.rpm.validation_rpm import ValidateRpm


class TestValidationRpm(unittest.TestCase):

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=True)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    def test_download_artifacts(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_rpm = ValidateRpm(mock_validation_args)

        result = validate_rpm.download_artifacts()

        self.assertEqual(result, True)

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=False)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    def test_download_artifacts_error(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.11.0'

        validate_rpm = ValidateRpm(mock_validation_args)

        self.assertRaises(Exception, validate_rpm.download_artifacts())

    @patch("validation_workflow.rpm.validation_rpm.execute", return_value=True)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    def test_installation(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.arch.return_value = 'x64'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_rpm = ValidateRpm(mock_validation_args.return_value)

        result = validate_rpm.installation()
        self.assertTrue(result)

    @patch("validation_workflow.rpm.validation_rpm.execute", return_value=True)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('time.sleep')
    def test_start_cluster(self, mock_validation_args: Mock, mock_system: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]

        validate_rpm = ValidateRpm(mock_validation_args.return_value)

        result = validate_rpm.start_cluster()
        self.assertTrue(result)

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('validation_workflow.rpm.validation_rpm.ApiTestCases')
    def test_validation(self, mock_test_cases: Mock, mock_validation_args: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_cases_instance = mock_test_cases.return_value
        mock_test_cases_instance.test_cases.return_value = (True, 4)

        # Create instance of ValidateRpm class
        validate_rpm = ValidateRpm(mock_validation_args.return_value)

        # Call validation method and assert the result
        result = validate_rpm.validation()
        self.assertTrue(result)

        # Assert that the mock methods are called as expected
        mock_test_cases.assert_called_once()

    @patch("validation_workflow.rpm.validation_rpm.execute", return_value=True)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    def test_cleanup(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]
        # Create instance of ValidateRpm class
        validate_rpm = ValidateRpm(mock_validation_args.return_value)

        result = validate_rpm.cleanup()
        self.assertTrue(result)
