# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

import requests

from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_request import ApiTest
from validation_workflow.docker.validation_docker import ValidateDocker
from validation_workflow.tar.validation_tar import ValidateTar
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ImplementValidation(Validation):
    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)
        self.tmp_dir = TemporaryDirectory()

    def installation(self) -> None:
        return None

    def start_cluster(self) -> None:
        return None

    def validation(self) -> None:
        return None

    def cleanup(self) -> None:
        return None


class TestValidation(unittest.TestCase):

    @patch('validation_workflow.download_utils.DownloadUtils')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_check_url_valid(self, mock_validation_args: Mock, mock_download_utils: Mock) -> None:
        mock_validation_args.projects.return_value = ["opensearch"]

        mock_validation = ValidateTar(mock_validation_args.return_value)
        mock_download_utils_download = mock_download_utils.return_value
        mock_download_utils_download.download.return_value = True
        mock_download_utils_download.is_url_valid.return_value = True
        url = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.12.staging.repo"

        result = mock_validation.check_url(url)
        self.assertTrue(result)

    @patch('shutil.copy2', return_value=True)
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_copy_artifact(self, mock_validation_args: Mock, mock_copy: Mock) -> None:
        mock_validation_args.projects.return_value = ["opensearch"]
        mock_validation = ValidateTar(mock_validation_args.return_value)

        url = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.12.staging.repo"

        result = mock_validation.copy_artifact(url, "tmp/tthcdhfh/")
        self.assertTrue(result)

    @patch('os.path.exists')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_check_for_security_plugin(self, mock_validation_args: Mock, mock_path_exists: Mock) -> None:
        mock_path_exists.return_value = True

        mock_validation_args.projects.return_value = ["opensearch"]
        mock_validation = ValidateTar(mock_validation_args.return_value)

        result = mock_validation.check_for_security_plugin("/tmp/tmkuiuo/opensearch")

        self.assertTrue(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.Validation.check_http_request')
    @patch('validation_workflow.validation.ValidationArgs')
    def test_check_cluster_readiness_error(self, mock_validation_args: Mock, mock_check_http: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '1.0.0.1000'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_check_http.return_value = False

        validate_docker = ValidateTar(mock_validation_args.return_value)
        result = validate_docker.check_cluster_readiness()

        self.assertFalse(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch.object(ApiTest, "api_get")
    def test_check_http_request(self, mock_api_get: Mock, mock_validation_args: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '1.3.13'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
        mock_api_get.return_value = (200, "text")

        validate_docker = ValidateTar(mock_validation_args.return_value)
        result = validate_docker.check_http_request()

        self.assertTrue(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch.object(ApiTest, "api_get")
    def test_check_http_request_error(self, mock_api_get: Mock, mock_validation_args: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '1.3.14'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_api_get.return_value = (400, "text")

        validate_docker = ValidateTar(mock_validation_args.return_value)
        result = validate_docker.check_http_request()

        self.assertFalse(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch.object(ApiTest, "api_get")
    def test_check_http_request_connection_error(self, mock_api_get: Mock, mock_validation_args: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_api_get.side_effect = requests.exceptions.ConnectionError

        validate_docker = ValidateDocker(mock_validation_args.return_value)

        result = validate_docker.check_http_request()

        self.assertFalse(result)
