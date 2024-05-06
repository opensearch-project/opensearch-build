# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, call, patch

from system.process import Process
from validation_workflow.zip.validation_zip import ValidateZip


class TestValidateZip(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_args = MagicMock()
        self.tmp_dir = MagicMock()
        self.mock_args.projects = ["opensearch", "opensearch-dashboards"]
        self.mock_args.version = "2.11.0"
        self.mock_args.arch = "x64"
        self.mock_args.platform = "windows"
        self.mock_args.force_https_check = True
        self.mock_args.allow_http = True
        self.call_methods = ValidateZip(self.mock_args, self.tmp_dir)

    @patch("validation_workflow.zip.validation_zip.ZipFile")
    @patch('os.path.basename')
    def test_installation(self, mock_basename: Mock, mock_zip_file: MagicMock) -> None:
        mock_zip_file_instance = mock_zip_file.return_value.__enter__()
        mock_extractall = MagicMock()
        mock_zip_file_instance.extractall = mock_extractall
        mock_basename.side_effect = lambda path: "mocked_filename"

        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        result = validate_zip.installation()
        self.assertTrue(result)

        expected_calls = [call((validate_zip.tmp_dir.path))] * len(self.mock_args.projects)
        mock_extractall.assert_has_calls(expected_calls)

    @patch("validation_workflow.zip.validation_zip.ZipFile")
    @patch('os.path.basename')
    def test_installation_exception(self, mock_basename: Mock, mock_zip_file: MagicMock) -> None:
        self.mock_args.projects = None
        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        mock_basename.side_effect = lambda path: "mocked_filename"
        with self.assertRaises(Exception) as context:
            validate_zip.installation()
        self.assertEqual(str(context.exception), "Failed to install OpenSearch/OpenSearch-Dashboards")

    @patch.object(Process, "start")
    @patch('validation_workflow.zip.validation_zip.get_password')
    def test_start_cluster(self, mock_password: Mock, mock_start: Mock) -> None:

        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        mock_password.return_value = "admin"
        result = validate_zip.start_cluster()
        self.assertTrue(result)
        mock_password.assert_called_once()

    @patch.object(Process, "start")
    def test_start_cluster_exception(self, mock_start: Mock) -> None:
        mock_start.side_effect = Exception("an exception")
        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        with self.assertRaises(Exception) as context:
            validate_zip.start_cluster()
        self.assertEqual(str(context.exception), "Failed to Start Cluster")

    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    @patch("validation_workflow.zip.validation_zip.ApiTestCases")
    def test_validation(self, mock_test_apis: MagicMock, mock_check_cluster: Mock) -> None:
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (True, 3)
        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        result = validate_zip.validation()

        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_test_apis.assert_called_once()

    @patch('validation_workflow.zip.validation_zip.ValidationArgs')
    @patch('validation_workflow.zip.validation_zip.ApiTestCases')
    @patch('os.path.basename')
    @patch('system.execute.execute')
    @patch('validation_workflow.validation.Validation.check_for_security_plugin')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_validation_with_allow_http(self, mock_check_cluster: Mock, mock_security: Mock, mock_system: Mock, mock_basename: Mock, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.allow_http = True
        validate_zip = ValidateZip(mock_validation_args.return_value, self.tmp_dir)
        mock_check_cluster.return_value = True
        mock_basename.side_effect = lambda path: "mocked_filename"
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        mock_security.return_value = True
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 4)

        result = validate_zip.validation()
        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_security.assert_called_once()

    @patch('validation_workflow.zip.validation_zip.ValidationArgs')
    @patch('validation_workflow.zip.validation_zip.ValidateZip.cleanup')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_cluster_not_ready(self, mock_check_cluster: Mock, mock_cleanup: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        validate_zip = ValidateZip(mock_validation_args.return_value, self.tmp_dir)
        mock_check_cluster.return_value = False
        mock_cleanup.return_value = True

        with self.assertRaises(Exception) as context:
            validate_zip.validation()
        self.assertEqual(str(context.exception), 'Cluster is not ready for API test')
        mock_check_cluster.assert_called_once()

    @patch('validation_workflow.zip.validation_zip.ApiTestCases')
    @patch('validation_workflow.zip.validation_zip.ValidateZip.cleanup')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_failed_testcases(self, mock_check_cluster: Mock, mock_cleanup: Mock, mock_test_apis: Mock) -> None:
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (False, 1)
        mock_cleanup.return_value = True

        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        with self.assertRaises(Exception) as context:
            validate_zip.validation()

        self.assertEqual(str(context.exception), 'Not all tests Pass : 1')
        mock_test_apis.assert_called_once()

    @patch.object(Process, "terminate")
    def test_cleanup(self, mock_process_terminate: MagicMock) -> None:
        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        result = validate_zip.cleanup()
        self.assertTrue(result)
        mock_process_terminate.assert_called()

    @patch.object(Process, "terminate")
    def test_cleanup_exception(self, mock_process_terminate: MagicMock) -> None:
        mock_process_terminate.side_effect = Exception("any exception")
        validate_zip = ValidateZip(self.mock_args, self.tmp_dir)
        with self.assertRaises(Exception) as context:
            validate_zip.cleanup()
        self.assertEqual(
            str(context.exception),
            "Failed to terminate the processes that started OpenSearch and OpenSearch-Dashboards",
        )
