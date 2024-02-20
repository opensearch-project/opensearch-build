# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, call, patch

from validation_workflow.deb.validation_deb import ValidateDeb


class TestValidateDeb(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_args = MagicMock()
        self.mock_args.version = "2.3.0"
        self.mock_args.arch = "x64"
        self.mock_args.projects = ["opensearch"]
        self.mock_args.file_path = {"opensearch": "/src/opensearch/opensearch-1.3.12.staging.deb"}
        self.mock_args.platform = "linux"
        self.call_methods = ValidateDeb(self.mock_args)

    @patch("validation_workflow.deb.validation_deb.execute")
    @patch('os.path.basename')
    @patch("validation_workflow.deb.validation_deb.get_password")
    def test_installation(self, mock_get_pwd: Mock, mock_basename: Mock, mock_system: Mock) -> None:
        validate_deb = ValidateDeb(self.mock_args)
        mock_basename.side_effect = lambda path: "mocked_filename"
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        result = validate_deb.installation()
        self.assertTrue(result)
        mock_get_pwd.assert_called_with("2.3.0")

    @patch("validation_workflow.deb.validation_deb.execute")
    @patch("validation_workflow.deb.validation_deb.get_password")
    def test_installation_exception_os(self, mock_get_pwd: Mock, mock_execute: Mock) -> None:
        validate_deb = ValidateDeb(self.mock_args)
        mock_execute.side_effect = Exception("any exception occurred")
        with self.assertRaises(Exception) as context:
            validate_deb.installation()

        mock_get_pwd.assert_called_with("2.3.0")
        self.assertEqual(str(context.exception), "Failed to install OpenSearch/OpenSearch-Dashboards")

    @patch("validation_workflow.deb.validation_deb.execute")
    @patch("validation_workflow.deb.validation_deb.ValidationArgs")
    def test_start_cluster(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        self.mock_args.projects = ["opensearch", "opensearch-dashboards"]

        validate_deb = ValidateDeb(self.mock_args)
        result = validate_deb.start_cluster()
        self.assertTrue(result)
        mock_execute.assert_has_calls(
            [
                call("sudo systemctl enable opensearch", "."),
                call("sudo systemctl start opensearch", "."),
                call("sudo systemctl status opensearch", "."),
                call("sudo systemctl enable opensearch-dashboards", "."),
                call("sudo systemctl start opensearch-dashboards", "."),
                call("sudo systemctl status opensearch-dashboards", "."),
            ]
        )

    @patch("validation_workflow.deb.validation_deb.execute")
    def test_start_cluster_exception_os(self, mock_execute: MagicMock) -> None:
        validate_deb = ValidateDeb(self.mock_args)
        mock_execute.side_effect = Exception("any exception occurred")
        with self.assertRaises(Exception) as context:
            validate_deb.start_cluster()

        self.assertEqual(str(context.exception), "Failed to Start Cluster")

    @patch("validation_workflow.deb.validation_deb.ApiTestCases")
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_validation(self, mock_check_cluster: Mock, mock_test_apis: Mock) -> None:
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (True, 3)

        validate_deb = ValidateDeb(self.mock_args)

        result = validate_deb.validation()
        self.assertTrue(result)

        mock_test_apis.assert_called_once()
        mock_check_cluster.assert_called_once()

    @patch('validation_workflow.deb.validation_deb.ApiTestCases')
    @patch('os.path.basename')
    @patch('validation_workflow.deb.validation_deb.execute')
    @patch('validation_workflow.validation.Validation.check_for_security_plugin')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_validation_with_allow_http(self, mock_validation_args: Mock, mock_check_cluster: Mock, mock_security: Mock, mock_system: Mock, mock_basename: Mock, mock_test_apis: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.allow_http = True
        validate_deb = ValidateDeb(mock_validation_args.return_value)
        mock_check_cluster.return_value = True
        mock_basename.side_effect = lambda path: "mocked_filename"
        mock_system.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        mock_security.return_value = True
        mock_test_apis_instance = mock_test_apis.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 4)

        result = validate_deb.validation()
        self.assertTrue(result)
        mock_check_cluster.assert_called_once()
        mock_security.assert_called_once()

    @patch('validation_workflow.deb.validation_deb.ValidationArgs')
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_cluster_not_ready(self, mock_check_cluster: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        validate_deb = ValidateDeb(mock_validation_args.return_value)
        mock_check_cluster.return_value = False

        with self.assertRaises(Exception) as context:
            validate_deb.validation()
        self.assertEqual(str(context.exception), 'Cluster is not ready for API test')
        mock_check_cluster.assert_called_once()

    @patch("validation_workflow.deb.validation_deb.ApiTestCases")
    @patch('validation_workflow.validation.Validation.check_cluster_readiness')
    def test_failed_testcases(self, mock_check_cluster: Mock, mock_test_apis: Mock) -> None:
        mock_test_apis_instance = mock_test_apis.return_value
        mock_check_cluster.return_value = True
        mock_test_apis_instance.test_apis.return_value = (False, 2)
        validate_deb = ValidateDeb(self.mock_args)

        with self.assertRaises(Exception) as context:
            validate_deb.validation()

        self.assertEqual(str(context.exception), "Not all tests Pass : 2")

        mock_test_apis.assert_called_once()

    @patch("validation_workflow.deb.validation_deb.execute")
    def test_cleanup(self, mock_execute: Mock) -> None:
        self.mock_args.projects = ["opensearch", "opensearch-dashboards"]

        validate_deb = ValidateDeb(self.mock_args)
        result = validate_deb.cleanup()
        self.assertTrue(result)
        mock_execute.assert_has_calls(
            [call("sudo dpkg --purge opensearch", "."), call("sudo dpkg --purge opensearch-dashboards", ".")]
        )

    @patch("validation_workflow.deb.validation_deb.execute")
    def test_cleanup_exception(self, mock_execute: Mock) -> None:
        self.mock_args.projects = ["opensearch", "opensearch-dashboards"]
        mock_execute.side_effect = Exception("an exception occurred")
        validate_deb = ValidateDeb(self.mock_args)
        with self.assertRaises(Exception) as context:
            validate_deb.cleanup()

        self.assertEqual(
            str(context.exception),
            "Exception occurred either while attempting to stop cluster or removing OpenSearch/OpenSearch-Dashboards. an exception occurred",
        )
