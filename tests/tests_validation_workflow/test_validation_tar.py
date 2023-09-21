# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, patch

from system.process import Process
from validation_workflow.tar.validation_tar import ValidateTar


class TestValidationTar(unittest.TestCase):

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=True)
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_download_artifacts(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock) -> None:
        mock_validation_args.return_value.projects.return_value = ["opensearch"]
        mock_validation_args.return_value.version.return_value = "2.5.0"
        mock_validation_args.return_value.arch.return_value = "x64"
        mock_check_url = MagicMock()
        mock_check_url.return_value = True
        validate_tar = ValidateTar(mock_validation_args)

        result = validate_tar.download_artifacts()

        self.assertEqual(result, True)

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=False)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    @patch("validation_workflow.validation.Validation.check_url", return_value=False)
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_download_artifacts_error(self, mock_validation_args: Mock, mock_is_url_valid: Mock, mock_download: Mock, mock_check_url: Mock) -> None:
        url = "https://opensearch.org/release/2.11.0/opensearch-2.11.0-linux-arm64.tar.gz"

        validate_tar = ValidateTar(mock_validation_args)
        validate_tar.download_artifacts()
        self.assertRaises(Exception, validate_tar.check_url(url))

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.validation.Validation.check_url')
    def test_copy_artifacts(self, mock_validation_args: Mock, mock_isFilePathEmpty: Mock) -> None:
        mock_isFilePathEmpty.return_value = True
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
        mock_validation_args.return_value.file_path = {"opensearch": "/src/files/opensearch-tar.gz", "opensearch-dashboards": "/src/files/opensearch-dashboards-tar.gz"}
        validate_tar = ValidateTar(mock_validation_args.return_value)

        # Call cleanup method
        with patch.object(validate_tar, 'copy_artifact') as mock_copy_artifact:
            mock_copy_artifact.return_value = True
            result = validate_tar.download_artifacts()
            self.assertTrue(result)

    @patch("validation_workflow.tar.validation_tar.execute", return_value=True)
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_installation(self, mock_validation_args: Mock, mock_system: Mock) -> None:
        mock_validation_args.return_value.version.return_value = '2.3.0'
        mock_validation_args.return_value.arch.return_value = 'x64'
        mock_validation_args.return_value.platform.return_value = 'linux'
        mock_validation_args.return_value.projects.return_value = ["opensearch"]

        validate_tar = ValidateTar(mock_validation_args.return_value)

        result = validate_tar.installation()
        self.assertTrue(result)

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch.object(Process, 'start')
    @patch('time.sleep')
    def test_start_cluster(self, mock_sleep: Mock, mock_start: Mock, mock_validation_args: Mock) -> None:
        validate_tar = ValidateTar(mock_validation_args.return_value)
        result = validate_tar.start_cluster()
        self.assertTrue(result)

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.tar.validation_tar.ApiTestCases')
    def test_validation(self, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 3)

        validate_tar = ValidateTar(mock_validation_args.return_value)

        result = validate_tar.validation()
        self.assertTrue(result)

        mock_test_apis.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.tar.validation_tar.ApiTestCases')
    def test_failed_testcases(self, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 1)

        # Create instance of ValidateRpm class
        validate_tar = ValidateTar(mock_validation_args.return_value)

        # Call validation method and assert the result
        validate_tar.validation()
        self.assertRaises(Exception, "Not all tests Pass : 1")

        # Assert that the mock methods are called as expected
        mock_test_apis.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch.object(Process, 'terminate')
    def test_cleanup(self, mock_terminate: Mock, mock_validation_args: Mock) -> None:
        validation_args = mock_validation_args.return_value
        validate_tar = ValidateTar(validation_args)
        result = validate_tar.cleanup()
        self.assertTrue(result)
