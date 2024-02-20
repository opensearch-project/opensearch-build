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


class TestValidateTar(unittest.TestCase):
    def setUp(self) -> None:
        self.args = Mock()
        self.call_methods = ValidateTar(self.args)

    def test_empty_file_path_and_production_artifact_type(self) -> None:
        self.args.projects = ["opensearch"]
        self.args.version = "2.4.0"
        self.args.distribution = "tar"
        self.args.file_path = {}
        self.args.artifact_type = "production"

        with patch.object(self.call_methods, 'check_url') as mock_check_url:
            result = self.call_methods.download_artifacts()

        self.assertTrue(result)
        mock_check_url.assert_called_once()

    def test_with_file_path_both_artifact_types(self) -> None:
        self.args.projects = ["opensearch"]
        self.args.file_path = {"opensearch": "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/tar/dist/opensearch/opensearch-1.3.12.tar.gz"}

        with patch.object(self.call_methods, 'check_url') as mock_check_url:
            result = self.call_methods.download_artifacts()
        self.assertTrue(result)
        mock_check_url.assert_called_with(self.args.file_path["opensearch"])

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_empty_file_path_and_staging_artifact_type(self, mock_validation_args: Mock) -> None:
        self.args.projects = ["opensearch"]
        self.args.version = "2.4.0"
        self.args.distribution = "tar"
        self.args.artifact_type = "staging"
        self.args.file_path = {}
        self.args.build_number = {"opensearch": "latest", "opensearch-dashboards": "latest"}

        with patch.object(self.call_methods, 'check_url') as mock_check_url:
            result = self.call_methods.download_artifacts()
        self.assertTrue(result)
        mock_check_url.assert_called_with(self.args.file_path["opensearch"])

    @patch('shutil.copy2', return_value=True)
    def test_local_artifacts(self, mock_copy: Mock) -> None:
        self.args.file_path = {"opensearch": "tar.gz"}
        self.args.projects = ["opensearch"]
        self.args.version = ""
        self.args.arch = "x64"
        self.args.file_path = {"opensearch": "src/opensearch/opensearch-1.3.12.tar.gz"}

        with patch.object(self.call_methods, 'copy_artifact') as mock_copy_artifact:
            result = self.call_methods.download_artifacts()
        self.assertTrue(result)
        mock_copy_artifact.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('os.path.basename')
    @patch('validation_workflow.tar.validation_tar.execute')
    def test_installation(self, mock_system: Mock, mock_basename: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.arch = 'x64'
        mock_validation_args.return_value.platform = 'linux'
        mock_validation_args.return_value.allow_http = True
        mock_validation_args.return_value.projects = ["opensearch"]

        validate_tar = ValidateTar(mock_validation_args.return_value)
        mock_basename.side_effect = lambda path: "mocked_filename"
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        result = validate_tar.installation()
        self.assertTrue(result)

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch.object(Process, 'start')
    @patch('validation_workflow.tar.validation_tar.get_password')
    def test_start_cluster(self, mock_password: Mock, mock_start: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.arch = 'x64'
        mock_validation_args.return_value.platforms = 'linux'
        mock_validation_args.return_value.allow_http = True
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
        mock_password.return_value = "admin"

        validate_tar = ValidateTar(mock_validation_args.return_value)
        result = validate_tar.start_cluster()
        self.assertTrue(result)
        mock_password.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('time.sleep')
    @patch('src.test_workflow.integ_test.utils.get_password')
    def test_start_cluster_exception_os(self, mock_password: Mock, mock_sleep: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_validation_args.return_value.allow_http = True

        validate_tar = ValidateTar(mock_validation_args.return_value)
        validate_tar.os_process.start = MagicMock(side_effect=Exception('Failed to Start Cluster'))  # type: ignore
        with self.assertRaises(Exception) as context:
            validate_tar.start_cluster()

        self.assertEqual(str(context.exception), 'Failed to Start Cluster')

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.tar.validation_tar.ApiTestCases')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_validation(self, mock_check_cluster: Mock, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (True, 3)

        validate_tar = ValidateTar(mock_validation_args.return_value)

        result = validate_tar.validation()
        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_test_apis.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.tar.validation_tar.ApiTestCases')
    @patch('os.path.basename')
    @patch('validation_workflow.tar.validation_tar.execute')
    @patch('validation_workflow.validation.Validation.check_for_security_plugin')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_validation_with_allow_http(self, mock_check_cluster: Mock, mock_security: Mock, mock_system: Mock, mock_basename: Mock, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.allow_http = True
        validate_tar = ValidateTar(mock_validation_args.return_value)
        mock_check_cluster.return_value = True
        mock_basename.side_effect = lambda path: "mocked_filename"
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        mock_security.return_value = True
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 4)

        result = validate_tar.validation()
        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_security.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_cluster_not_ready(self, mock_check_cluster: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        validate_tar = ValidateTar(mock_validation_args.return_value)
        mock_check_cluster.return_value = False

        with self.assertRaises(Exception) as context:
            validate_tar.validation()
        self.assertEqual(str(context.exception), 'Cluster is not ready for API test')
        mock_check_cluster.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('validation_workflow.tar.validation_tar.ApiTestCases')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_failed_testcases(self, mock_check_cluster: Mock, mock_test_apis: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (False, 1)

        validate_tar = ValidateTar(mock_validation_args.return_value)

        with self.assertRaises(Exception) as context:
            validate_tar.validation()

        self.assertEqual(str(context.exception), 'Not all tests Pass : 1')

        mock_test_apis.assert_called_once()

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch.object(Process, 'terminate')
    def test_cleanup(self, mock_terminate: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.arch = 'x64'
        mock_validation_args.return_value.platform = 'linux'
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]

        validate_tar = ValidateTar(mock_validation_args.return_value)
        result = validate_tar.cleanup()
        self.assertTrue(result)

    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_cleanup_exception(self, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
        validate_tar = ValidateTar(mock_validation_args.return_value)
        with self.assertRaises(Exception) as context:
            validate_tar.cleanup()

        self.assertEqual(str(context.exception), 'Failed to terminate the processes that started OpenSearch and OpenSearch-Dashboards')
