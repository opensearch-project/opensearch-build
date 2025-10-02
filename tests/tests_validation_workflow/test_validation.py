# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import unittest
from unittest import mock
from unittest.mock import Mock, call, mock_open, patch

import requests

from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_request import ApiTest
from validation_workflow.docker.validation_docker import ValidateDocker
from validation_workflow.tar.validation_tar import ValidateTar
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ImplementValidation(Validation):
    def __init__(self, args: ValidationArgs, tmp_dir: TemporaryDirectory) -> None:
        super().__init__(args, tmp_dir)

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
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_check_url_valid(self, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_download_utils: Mock) -> None:
        mock_validation_args.projects.return_value = ["opensearch"]
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"
        mock_temporary_directory.return_value.name = "/tmp/trytytyuit/"
        mock_validation = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)

        url = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.12.staging.repo"

        with mock.patch("os.path.join") as mock_join, \
                mock.patch("os.path.basename") as mock_basename, \
                mock.patch("builtins.open") as mock_open:
            mock_join.return_value = "mocked_path"
            mock_basename.return_value = "mocked_filename"
            response_content = "Mocked content"
            mock_open.return_value.write.return_value = len(response_content)

            mock_download_utils_download = mock_download_utils.return_value
            mock_download_utils_download.download.return_value = True
            mock_download_utils_download.is_url_valid.return_value = True

            result = mock_validation.check_url(url)

            self.assertTrue(result)

    @patch('shutil.copy2', return_value=True)
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_copy_artifact(self, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_copy: Mock) -> None:
        mock_validation_args.projects.return_value = ["opensearch"]
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"
        mock_validation = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)

        url = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.12.staging.repo"

        result = mock_validation.copy_artifact(url, mock_temporary_directory.return_value.path)
        self.assertTrue(result)

    @patch('os.path.exists')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_check_for_security_plugin(self, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_path_exists: Mock) -> None:
        mock_path_exists.return_value = True
        mock_validation_args.projects.return_value = ["opensearch"]
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"

        mock_validation = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)

        result = mock_validation.check_for_security_plugin("/tmp/trytytyuit/opensearch")

        self.assertTrue(result)

    @patch("validation_workflow.validation.execute")
    @patch.object(Validation, "get_native_plugin_list")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_install_native_plugin_production(self, mock_temporary_directory: Mock, mock_validation_args: Mock,
                                              mock_plugin_list: Mock, mock_execute: Mock) -> None:
        mock_plugin_list.return_value = ["discovery-ec2", "repository-s3"]
        mock_execute.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")

        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        validate_tar.install_native_plugin(os.path.join("tmp", "trytytyuit", "opensearch"), ["discovery-ec2", "repository-s3"])
        mock_execute.assert_has_calls(
            [
                call(f'.{os.sep}opensearch-plugin install --batch discovery-ec2',
                     os.path.join("tmp", "trytytyuit", "opensearch", "bin")),
                call(f'.{os.sep}opensearch-plugin install --batch repository-s3',
                     os.path.join("tmp", "trytytyuit", "opensearch", "bin"))
            ]
        )

    @patch('pathlib.Path.as_uri')
    @patch('requests.get')
    @patch("validation_workflow.validation.execute")
    @patch.object(Validation, "get_native_plugin_list")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch("builtins.open", new_callable=mock_open)
    def test_install_native_plugin_staging(self, mock_temporary_directory: Mock, mock_file: Mock,
                                           mock_validation_args: Mock, mock_plugin_list: Mock, mock_execute: Mock,
                                           mock_get: Mock, mock_path: Mock) -> None:
        mock_response = Mock()
        mock_validation_args.return_value.version = "3.0.0"
        mock_validation_args.os_build_number.return_value = "1123"
        mock_validation_args.platform.return_value = "linux"
        mock_validation_args.arch.return_value = "x64"
        mock_validation_args.distribution.return_value = "tar"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        mock_plugin_list.return_value = ["analysis-icu", "analysis-nori"]
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")
        mock_validation_args.return_value.artifact_type = "staging"
        mock_execute.side_effect = lambda *args, **kwargs: (0, "stdout_output", "stderr_output")
        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        mock_path.return_value = "file:///tmp/trytytyuit/opensearch/bin/analysis-icu-3.0.0.zip"
        validate_tar.install_native_plugin(os.path.join("tmp", "trytytyuit", "opensearch"),
                                           ["analysis-icu", "analysis-nori"])

        mock_execute.assert_has_calls(
            [
                call(
                    f'.{os.sep}opensearch-plugin install --batch file:///{os.path.join("tmp", "trytytyuit", "opensearch", "bin", "analysis-icu-3.0.0.zip")}',
                    os.path.join("tmp", "trytytyuit", "opensearch", "bin")),
            ]
        )

        mock_path.return_value = "file:///tmp/trytytyuit/opensearch/bin/analysis-nori-3.0.0.zip"
        mock_execute.assert_has_calls(
            [
                call(
                    f'.{os.sep}opensearch-plugin install --batch file:///{os.path.join("tmp", "trytytyuit", "opensearch", "bin", "analysis-icu-3.0.0.zip")}',
                    os.path.join("tmp", "trytytyuit", "opensearch", "bin")),
            ]
        )

    @patch('requests.get')
    @patch("validation_workflow.validation.execute")
    @patch.object(Validation, "get_native_plugin_list")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch("builtins.open", new_callable=mock_open)
    def test_install_native_plugin_exception(self, mock_file: Mock, mock_temporary_directory: Mock,
                                             mock_validation_args: Mock,
                                             mock_plugin_list: Mock, mock_execute: Mock, mock_get: Mock) -> None:
        mock_plugin_list.return_value = ["discovery-ec2", "repository-s3"]
        mock_execute.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=f".{os.sep}opensearch-plugin install --batch discovery-ec2', {os.path.join('tmp', 'trytytyuit', 'bin')}",
            stderr="stdout err"
        )
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")
        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        with self.assertRaises(Exception) as e:
            validate_tar.install_native_plugin(os.path.join("tmp", "trytytyuit", ), ["discovery-ec2"])
        self.assertEqual(str(e.exception),
                         f"Unable to install native plugin: Command '.{os.sep}opensearch-plugin install"
                         f" --batch discovery-ec2', tmp{os.sep}trytytyuit{os.sep}bin' returned non-zero exit status 1.")

    @patch('requests.get')
    @patch('manifests.bundle_manifest.BundleManifest.from_path')
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_get_native_plugin_list(self, mock_temporary_directory: Mock, mock_validation_args: Mock,
                                    mock_manifest_from_path: Mock, mock_get: Mock) -> None:

        mock_response = Mock()
        mock_response.json.return_value = [{'name': 'analysis-icu', 'path': 'plugins/analysis-icu', 'sha': 'adce05e8b5beee96'},
                                           {'name': 'analysis-nori', 'path': 'plugins/analysis-nori', 'sha': 'd3e5d7559hiji96'},
                                           {'name': 'query-insights', 'path': 'plugins/analysis-nori', 'sha': 'd3e5d7559hiji96'},
                                           {'name': 'examples', 'path': 'examples', 'sha': 'hjkd7559hiji96'},
                                           {'name': 'build.gradle', 'path': 'build.gradle', 'sha': 'd3e5d75cdsiji96'},
                                           {'name': 'identity-shiro', 'path': 'plugins/identity-shiro', 'sha': 'd3e5d75cdsiji96'}
                                           ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        mock_temporary_directory.return_value.path = "/tmp/trytytyuit/"
        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        result = validate_tar.get_native_plugin_list(mock_temporary_directory.return_value.path, ["query-insights"])

        self.assertEqual(["analysis-icu", "analysis-nori"], result)

    @patch('requests.get')
    @patch('manifests.bundle_manifest.BundleManifest.from_path')
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_get_native_plugin_list_exception(self, mock_temporary_directory: Mock, mock_validation_args: Mock,
                                              mock_manifest_from_path: Mock, mock_get: Mock) -> None:
        mock_response = Mock()
        mock_response.json.return_value = [
            {'name': 'analysis-icu', 'path': 'plugins/analysis-icu', 'sha': 'adce05e8b5beee96'},
            {'name': 'analysis-nori', 'path': 'plugins/analysis-nori', 'sha': 'd3e5d7559hiji96'},
            {'name': 'query-insights', 'path': 'plugins/analysis-nori', 'sha': 'd3e5d7559hiji96'}
        ]
        mock_response.status_code = 503
        mock_get.return_value = mock_response
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")
        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        with self.assertRaises(Exception) as e1:
            validate_tar.get_native_plugin_list(mock_temporary_directory.return_value.path, ["query-insights", "ml-commons"])

        self.assertEqual(str(e1.exception), "Github Api returned error code while retrieving the list of native plugins")

    @patch("time.sleep")
    @patch('validation_workflow.validation.Validation.check_http_request')
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    def test_check_cluster_readiness_error(self, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_check_http: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '1.0.0.1000'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")
        mock_check_http.return_value = False

        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        result = validate_tar.check_cluster_readiness()

        self.assertFalse(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch.object(ApiTest, "api_get")
    def test_check_http_request(self, mock_api_get: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '1.3.13'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch", "opensearch-dashboards"]
        mock_api_get.return_value = (200, "text")
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")

        validate_tar = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        result = validate_tar.check_http_request()

        self.assertTrue(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch.object(ApiTest, "api_get")
    def test_check_http_request_error(self, mock_api_get: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '1.3.14'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_api_get.return_value = (400, "text")
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")

        validate_docker = ValidateTar(mock_validation_args.return_value, mock_temporary_directory.return_value)
        result = validate_docker.check_http_request()

        self.assertFalse(result)

    @patch("time.sleep")
    @patch('validation_workflow.validation.ValidationArgs')
    @patch('system.temporary_directory.TemporaryDirectory')
    @patch.object(ApiTest, "api_get")
    def test_check_http_request_connection_error(self, mock_api_get: Mock, mock_temporary_directory: Mock, mock_validation_args: Mock, mock_sleep: Mock) -> None:
        mock_validation_args.return_value.version = '2.3.0'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.allow_http = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_temporary_directory.return_value.path = os.path.join("tmp", "trytytyuit")
        mock_api_get.side_effect = requests.exceptions.ConnectionError

        validate_docker = ValidateDocker(mock_validation_args.return_value, mock_temporary_directory.return_value)

        result = validate_docker.check_http_request()

        self.assertFalse(result)
