# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os.path
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, mock_open, patch

import requests
from openapi_core.exceptions import OpenAPIError
from requests.models import Response

from test_workflow.smoke_test.smoke_test_runner_opensearch import SmokeTestRunnerOpenSearch


class TestSmokeTestRunnerOpenSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.args = MagicMock()
        self.test_manifest = MagicMock()
        mock_components = MagicMock()
        mock_component = MagicMock()
        mock_component.name = "opensearch"
        mock_component.smoke_test = True
        mock_components.select.return_value = [mock_component]
        self.test_manifest.components = mock_components

    @patch("test_workflow.smoke_test.smoke_test_runner.SmokeTestRunner.extract_paths_from_yaml")
    @patch("test_workflow.smoke_test.smoke_test_runner_opensearch.SmokeTestRunnerOpenSearch.validate_response_swagger")
    @patch("test_workflow.smoke_test.smoke_test_runner_opensearch.Spec.from_file_path")
    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("requests.get")
    @patch("os.path.exists")
    @patch("os.path.dirname")
    def test_smoke_test_runner_opensearch_start_test(self, mock_dirname: Mock, mock_path_exist: Mock, mock_get: Mock,
                                                     mock_recorder: Mock, mock_spec: Mock, mock_validate: Mock,
                                                     mock_extract_spec: Mock) -> None:
        mock_dirname.return_value = "dummy/path"
        mock_path_exist.return_value = True
        mock_spec.return_value = MagicMock()
        mock_extract_spec.return_value = {"/": {"GET": {}}, "/_cat/plugins": {"GET": {}}}

        runner = SmokeTestRunnerOpenSearch(self.args, self.test_manifest)
        runner.version = "2.19.0"

        # Mock a successful API response
        response = Response()
        response.status_code = 200
        response._content = b'{"status": "OK"}'
        response.request = requests.Request("GET", "https://localhost:9200/").prepare()
        mock_get.return_value = response

        results = runner.start_test(work_dir=Path("/temp/path"))
        self.assertTrue(results)
        mock_extract_spec.assert_called_with("opensearch", "2.19.0")
        self.test_manifest.components.select.assert_called()
        mock_get.assert_has_calls(
            [call('https://localhost:9200/', verify=False, auth=('admin', 'myStrongPassword123!'),
                  headers={'Content-Type': 'application/json'}, data=''),
             call('https://localhost:9200/_cat/plugins', verify=False, auth=('admin', 'myStrongPassword123!'),
                  headers={'Content-Type': 'application/json'}, data='')])
        mock_validate.assert_called_with(response)

    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("requests.get")
    def test_smoke_test_validate_response_swagger(self, mock_get: Mock, mock_test_recorder: Mock) -> None:
        runner = SmokeTestRunnerOpenSearch(self.args, self.test_manifest)

        # Mock a successful API response
        response = Response()
        response.status_code = 200
        response._content = b'{"status": "OK"}'
        response.request = requests.Request("GET", "https://localhost:9200/").prepare()
        mock_get.return_value = response

        # Validate the response with the mocked OpenAPI validator
        with patch.object(runner, "validate_response_swagger", return_value=None):
            runner.validate_response_swagger(response)

    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("requests.get")
    def test_validate_response_swagger_with_invalid_response(self, mock_get: Mock, mock_test_recorder: Mock) -> None:
        runner = SmokeTestRunnerOpenSearch(self.args, self.test_manifest)

        # Mock an invalid response
        response = Response()
        response.status_code = 404
        response._content = b'{"error": "Not Found"}'
        response.request = requests.Request("GET", "https://localhost:9200/_invalid_endpoint").prepare()
        mock_get.return_value = response

        # Validate that an OpenAPIError is raised for an invalid response
        with self.assertRaises(OpenAPIError):
            runner.validate_response_swagger(response)

    @patch("test_workflow.smoke_test.smoke_test_runner_opensearch.Spec")
    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_spec_success(self, mock_file: Mock, mock_get: Mock, mock_test_recorder: Mock, mock_spec: Mock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = "Mock OpenSearch API Spec Yaml content"
        mock_get.return_value = mock_response

        runner = SmokeTestRunnerOpenSearch(MagicMock(), MagicMock())

        mock_get.assert_called_once_with(
            "https://github.com/opensearch-project/opensearch-api-specification/releases/download/main-latest/opensearch-openapi.yaml",
            timeout=10
        )

        mock_file.assert_any_call(runner.spec_download_path, "wb")
        mock_file().write.assert_called_once_with("Mock OpenSearch API Spec Yaml content")

        self.assertTrue(runner.spec_path.endswith(os.path.join("smoke_tests_spec", "opensearch-openapi.yaml")))

    @patch("test_workflow.smoke_test.smoke_test_runner_opensearch.Spec")
    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_spec_fail_local(self, mock_file: Mock, mock_get: Mock, mock_test_recorder: Mock, mock_spec: Mock) -> None:
        # Mock request failure
        mock_get.side_effect = requests.RequestException

        runner = SmokeTestRunnerOpenSearch(MagicMock(), MagicMock())

        mock_get.assert_called_once()

        mock_file().write.assert_not_called()

        self.assertTrue(runner.spec_path.endswith(os.path.join("smoke_tests_spec", "opensearch-openapi-local.yaml")))

    @patch("test_workflow.smoke_test.smoke_test_runner_opensearch.Spec")
    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_spec_https_fail(self, mock_file: Mock, mock_get: Mock, mock_test_recorder: Mock, mock_spec: Mock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        runner = SmokeTestRunnerOpenSearch(MagicMock(), MagicMock())

        mock_get.assert_called_once()

        mock_file().write.assert_not_called()

        self.assertTrue(runner.spec_path.endswith(os.path.join("smoke_tests_spec", "opensearch-openapi-local.yaml")))
