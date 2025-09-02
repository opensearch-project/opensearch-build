# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import io
import logging
import os
import re
from logging import Handler
from pathlib import Path
from typing import Any, Tuple

import requests
from openapi_core import Spec, validate_request, validate_response
from openapi_core.contrib.requests import RequestsOpenAPIRequest, RequestsOpenAPIResponse

from manifests.test_manifest import TestManifest
from test_workflow.smoke_test.smoke_test_runner import SmokeTestRunner
from test_workflow.test_args import TestArgs
from test_workflow.test_recorder.test_result_data import TestResultData
from test_workflow.test_result.test_component_results import TestComponentResults
from test_workflow.test_result.test_result import TestResult
from test_workflow.test_result.test_suite_results import TestSuiteResults


class SmokeTestRunnerOpenSearch(SmokeTestRunner):

    def __init__(self, args: TestArgs, test_manifest: TestManifest) -> None:
        super().__init__(args, test_manifest)
        logging.info("Entering Smoke test for OpenSearch Bundle.")

        # Below URL is for the pre-release latest. In the future may consider use formal released spec when available.
        self.spec_url = "https://github.com/opensearch-project/opensearch-api-specification/releases/download/main-latest/opensearch-openapi.yaml"
        self.spec_local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smoke_tests_spec", "opensearch-openapi-local.yaml")
        self.spec_download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smoke_tests_spec", "opensearch-openapi.yaml")
        self.spec_path = self.download_spec(self.spec_url, self.spec_local_path, self.spec_download_path)
        self.spec_ = Spec.from_file_path(self.spec_path)
        self.mimetype = {
            "Content-Type": "application/json"
        }

    def download_spec(self, url: str, local_path: str, download_path: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(download_path, "wb") as file:
                    file.write(response.content)
                    logging.info(f"Downloaded latest spec from {url}")
                    return download_path
            else:
                logging.info(f"Failed to fetch remote API spec, using local file: {local_path}")
                return local_path
        except requests.RequestException:
            logging.info(f"Could not reach {url}, using local file: {local_path}")
            return local_path

    def validate_request_swagger(self, request: Any) -> None:
        request = RequestsOpenAPIRequest(request)
        validate_request(request=request, spec=self.spec_)
        logging.info("Request is validated.")

    def validate_response_swagger(self, response: Any) -> None:
        request = RequestsOpenAPIRequest(response.request)
        response = RequestsOpenAPIResponse(response)
        validate_response(response=response, spec=self.spec_, request=request)
        logging.info("Response is validated.")

    def record_test_result(self, component: str, test_api: str, api_action: str, stdout: str, stderr: str) -> None:
        test_config = f"{api_action}_{re.sub(r'[^a-zA-Z0-9]', '_', test_api)}"
        logging.info(f"Recording test result for {component} component, config {test_config}")
        file_path = self.test_recorder._create_base_folder_structure(component, test_config)
        self.test_recorder._generate_std_files(stdout, stderr, file_path)

    def setup_logging_buffers(self) -> Tuple[io.StringIO, io.StringIO, logging.StreamHandler, logging.StreamHandler]:
        info_buffer = io.StringIO()
        error_buffer = io.StringIO()

        info_handler = logging.StreamHandler(info_buffer)
        error_handler = logging.StreamHandler(error_buffer)

        info_handler.setLevel(logging.INFO)
        error_handler.setLevel(logging.ERROR)

        logging.getLogger().addHandler(info_handler)
        logging.getLogger().addHandler(error_handler)

        return info_buffer, error_buffer, info_handler, error_handler

    def cleanup_logging_handlers(self, info_handler: Handler, error_handler: Handler) -> None:
        logging.getLogger().removeHandler(info_handler)
        logging.getLogger().removeHandler(error_handler)

    def start_test(self, work_dir: Path) -> TestSuiteResults:
        url = "https://localhost:9200"

        all_results = TestSuiteResults()
        for component in self.test_manifest.components.select(self.args.components):
            if component.smoke_test:
                logging.info(f"Running smoke test on {component.name} component.")
                component_spec = self.extract_paths_from_yaml(component.name, component.smoke_test.get("test-spec"), self.version)
                logging.info(f"component spec is {component_spec}")
                test_results = TestComponentResults()
                for api_requests, api_details in component_spec.items():
                    request_url = ''.join([url, api_requests])
                    for method in api_details.keys():  # Iterates over each method, e.g., "GET", "POST"
                        info_buffer, error_buffer, info_handler, error_handler = self.setup_logging_buffers()

                        logging.info(f"Validating api request {api_requests}")
                        logging.info(f"API request URL is {request_url}")
                        requests_method = getattr(requests, method.lower())
                        parameters_data = self.convert_parameter_json(api_details.get(method).get("parameters"))
                        header = api_details.get(method).get("header", self.mimetype)
                        logging.info(f"Parameter is {parameters_data} and type is {type(parameters_data)}")
                        logging.info(f"header is {header}")
                        status = 0
                        try:
                            response = requests_method(request_url, verify=False, auth=("admin", "myStrongPassword123!"), headers=header, data=parameters_data)
                            logging.info(f"Response is \n{response.text}")
                            self.validate_response_swagger(response)
                        except Exception as e:
                            status = 1
                            logging.error(f"Unexpected Error type is {type(e)}")
                            logging.error(e)
                            logging.info("Response is not validated. Please check the response output text above.")
                        finally:
                            self.record_test_result(component.name, api_requests, method, info_buffer.getvalue(), error_buffer.getvalue())
                            test_result = TestResult(component.name, ' '.join([api_requests, method]), status)  # type: ignore
                            test_result_data_local = TestResultData(
                                component.name,
                                f"{method}_{re.sub(r'[^a-zA-Z0-9]', '_', api_requests)}",
                                status,
                                info_buffer.getvalue(),
                                error_buffer.getvalue(),
                                {}
                            )
                            self.test_recorder.test_results_logs.generate_component_yml(test_result_data_local)
                            self.cleanup_logging_handlers(info_handler, error_handler)
                            test_results.append(test_result)

                all_results.append(component.name, test_results)
        return all_results
