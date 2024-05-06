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
    def setUp(self) -> None:
        self.args = Mock()
        self.tmp_dir = Mock()
        self.call_methods = ValidateRpm(self.args, self.tmp_dir)

    def test_empty_file_path_and_production_artifact_type(self) -> None:
        self.args.projects = ["opensearch"]
        self.args.version = "2.4.0"
        self.args.distribution = "rpm"
        self.args.file_path = {}
        self.args.artifact_type = "production"

        with patch.object(self.call_methods, 'check_url') as mock_check_url:
            result = self.call_methods.download_artifacts()

        self.assertTrue(result)
        mock_check_url.assert_called_once()

    def test_with_file_path_both_artifact_types(self) -> None:
        self.args.projects = ["opensearch"]
        self.args.file_path = {"opensearch": "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.11.rpm"}

        with patch.object(self.call_methods, 'check_url') as mock_check_url:
            result = self.call_methods.download_artifacts()
        self.assertTrue(result)
        mock_check_url.assert_called_with(self.args.file_path["opensearch"])

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    def test_empty_file_path_and_staging_artifact_type(self, mock_validation_args: Mock) -> None:
        self.args.projects = ["opensearch"]
        self.args.version = "2.4.0"
        self.args.distribution = "rpm"
        self.args.artifact_type = "staging"
        self.args.file_path = {}
        self.args.build_number = {"opensearch": "1.2.3", "opensearch-dashboards": "1.2.3"}

        with patch.object(self.call_methods, 'check_url') as mock_check_url:
            result = self.call_methods.download_artifacts()
        self.assertTrue(result)
        mock_check_url.assert_called_with(self.args.file_path["opensearch"])

    @patch('shutil.copy2', return_value=True)
    def test_local_artifacts(self, mock_copy: Mock) -> None:
        self.args.file_path = {"opensearch": "opensearch.1.3.12.rpm"}
        self.args.projects = ["opensearch"]
        self.args.version = ""
        self.args.arch = "arm64"
        self.args.file_path = {"opensearch": "src/opensearch/opensearch-1.3.12.rpm"}

        with patch.object(self.call_methods, 'copy_artifact') as mock_copy_artifact:
            result = self.call_methods.download_artifacts()
        self.assertTrue(result)
        mock_copy_artifact.assert_called_once()

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_exceptions(self, mock_temporary_directory: Mock, mock_validation_args: Mock) -> None:
        with self.assertRaises(Exception) as e1:
            mock_validation_args.return_value.projects = ["opensearch"]
            mock_validation_args.return_value.file_path = {"opensearch": "/src/files/opensearch.rpm"}
            mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"
            validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)
            validate_rpm.installation()
        self.assertEqual(str(e1.exception), "Failed to install Opensearch")

        with self.assertRaises(Exception) as e2:
            mock_validation_args.return_value.projects = ["opensearch"]
            validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)
            validate_rpm.start_cluster()
        self.assertEqual(str(e2.exception), "Failed to Start Cluster")

        with self.assertRaises(Exception) as e3:
            mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
            validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)
            validate_rpm.cleanup()
        self.assertIn("Exception occurred either while attempting to stop cluster or removing OpenSearch/OpenSearch-Dashboards.",
                      str(e3.exception))

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch("validation_workflow.rpm.validation_rpm.execute")
    def test_installation(self, mock_temporary_directory: Mock, mock_system: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.arch = 'x64'
        mock_validation_args.return_value.platform = 'linux'
        mock_validation_args.return_value.allow_http = True
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"

        validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        result = validate_rpm.installation()
        self.assertTrue(result)

    @patch("validation_workflow.rpm.validation_rpm.execute", return_value=True)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_start_cluster(self, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_system: Mock) -> None:
        mock_validation_args.return_value.projects.return_value = ["opensearch", "opensearch-dashboards"]
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"

        validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)

        result = validate_rpm.start_cluster()
        self.assertTrue(result)

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch('validation_workflow.rpm.validation_rpm.ApiTestCases')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_validation(self, mock_check_cluster: Mock, mock_test_apis: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (True, 3)
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"

        validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)

        result = validate_rpm.validation()
        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_test_apis.assert_called_once()

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch('validation_workflow.rpm.validation_rpm.ApiTestCases')
    @patch('os.path.basename')
    @patch('validation_workflow.rpm.validation_rpm.execute')
    @patch('validation_workflow.validation.Validation.check_for_security_plugin')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_validation_with_allow_http_check(self, mock_check_cluster: Mock, mock_security: Mock, mock_system: Mock,
                                              mock_basename: Mock, mock_test_apis: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.allow_http = True
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"
        validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)
        mock_check_cluster.return_value = True
        mock_basename.side_effect = lambda path: "mocked_filename"
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        mock_security.return_value = True
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 4)

        result = validate_rpm.validation()
        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_security.assert_called_once()

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_cluster_not_ready(self, mock_check_cluster: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"
        validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)
        mock_check_cluster.return_value = False

        with self.assertRaises(Exception) as context:
            validate_rpm.validation()
        self.assertEqual(str(context.exception), 'Cluster is not ready for API test')
        mock_check_cluster.assert_called_once()

    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch('validation_workflow.rpm.validation_rpm.ApiTestCases')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_failed_testcases(self, mock_check_cluster: Mock, mock_test_apis: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (False, 1)
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"

        validate_rpm = ValidateRpm(mock_validation_args, mock_temporary_directory)

        with self.assertRaises(Exception) as context:
            validate_rpm.validation()

        self.assertEqual(str(context.exception), 'Not all tests Pass : 1')

        mock_test_apis.assert_called_once()

    @patch("validation_workflow.rpm.validation_rpm.execute", return_value=True)
    @patch('validation_workflow.rpm.validation_rpm.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_cleanup(self, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"

        validate_rpm = ValidateRpm(mock_validation_args.return_value, mock_temporary_directory.return_value)

        result = validate_rpm.cleanup()
        self.assertTrue(result)
