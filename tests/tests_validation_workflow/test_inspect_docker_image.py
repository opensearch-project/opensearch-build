# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import json
import subprocess
import unittest
from unittest.mock import MagicMock, Mock, call, patch

import requests

from validation_workflow.docker.inspect_docker_image import InspectDockerImage
from validation_workflow.validation_args import ValidationArgs


class TestInspectDockerImage(unittest.TestCase):
    def setUp(self) -> None:
        self.image_id = "12345"
        self.image_name = "opensearchproject/opensearch"
        self.prod_image_tag = "1.2.3"
        self.os_build_number = "1000"
        self.osd_build_number = "2000"
        self.version = "2.4.0"
        with patch("validation_workflow.docker.inspect_docker_image.ValidationArgs", MagicMock()) as mock_args:
            mock_args.stg_tag.return_value = "stg_tag"
            self.inspector = InspectDockerImage(self.image_id, self.image_name, self.prod_image_tag)

    def test_validation_args_stg_arg(self) -> None:
        result = ValidationArgs.stg_tag(self, 'opensearch_dashboards').replace(" ", "")  # type: ignore
        self.assertEqual(result, "2.4.0.2000")
        result = ValidationArgs.stg_tag(self, 'opensearch').replace(" ", "")  # type: ignore
        self.assertEqual(result, "2.4.0.1000")

    @patch('validation_workflow.docker.inspect_docker_image.ValidationArgs')
    @patch('validation_workflow.docker.inspect_docker_image.requests.get')
    @patch('validation_workflow.docker.inspect_docker_image.subprocess.run')
    def test_inspect_digest(self, mock_subprocess_run: Mock, mock_requests_get: Mock, mock_validation_args: Mock) -> None:
        mock_validation_args.return_value.stg_tag.return_value = '1.0.0.1000'

        auth_response = requests.Response()
        auth_response._content = json.dumps({'token': 'access_token'}).encode()
        mock_requests_get.return_value = auth_response

        manifest_response = requests.Response()
        manifest_response.headers['etag'] = '1234567890'

        # manifest_response._content = json.dumps({'config': {'digest': '1234567890'}}).encode()
        manifest_response._content = json.dumps({'RepoDigests': '@1234567890'}).encode()
        mock_requests_get.side_effect = [auth_response, manifest_response]

        subprocess_result = subprocess.CompletedProcess(args='', returncode=0, stdout=json.dumps({'RepoDigests': '@1234567890'}), stderr='')
        mock_subprocess_run.return_value = subprocess_result

        # Instantiate class and run method
        inspect_docker_image = InspectDockerImage(self.image_id, self.image_name, self.prod_image_tag)
        inspect_docker_image.inspect_digest()

        # Assert that the manifest value matches with the value from API mocked
        self.assertEqual(json.loads(subprocess_result.stdout), {'RepoDigests': '@' + manifest_response.headers['etag']})
        mock_requests_get.assert_has_calls(
            [
                call(
                    "https://auth.docker.io/token?service=registry.docker.io&scope=repository:opensearchstaging/opensearch:pull"
                ),
                call(
                    "https://index.docker.io/v2/opensearchstaging/opensearch/manifests/1.0.0.1000",
                    headers={
                        "Authorization": "Bearer access_token",
                        "Accept": "application/vnd.docker.distribution.manifest.list.v2+json",
                        "Content-Type": "application/json;charset=UTF-8",
                    },
                ),
            ]
        )
        mock_subprocess_run.assert_has_calls(
            [
                call(
                    "docker image inspect --format '{{json .}}' 12345 | jq -r '. | {RepoDigests: .RepoDigests}'",
                    shell=True,
                    stdout=-1,
                    stderr=-1,
                    universal_newlines=True,
                )
            ]
        )


if __name__ == '__main__':
    unittest.main()
