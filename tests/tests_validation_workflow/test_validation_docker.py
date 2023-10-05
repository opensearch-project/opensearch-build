# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest
import urllib.request
from unittest.mock import MagicMock, Mock, call, patch

from validation_workflow.docker.validation_docker import ValidateDocker


class TestValidateDocker(unittest.TestCase):

    @patch('validation_workflow.docker.validation_docker.ValidateDocker.get_image_id')
    @patch('validation_workflow.docker.validation_docker.ValidationArgs')
    @patch('validation_workflow.docker.validation_docker.ValidateDocker.is_container_daemon_running')
    def test_download_artifacts(self, mock_is_container_daemon_running: Mock, mock_validation_args: Mock, mock_get_image_id: Mock) -> None:
        mock_validation_args = Mock()
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_validation_args.return_value.docker_source = 'dockerhub'
        mock_validation_args.return_value.using_staging_artifact_only = True

        # create instance of ValidateDocker
        validate_docker = ValidateDocker(mock_validation_args.return_value)

        # set the desired value for args.docker_source
        validate_docker.args.docker_source = 'dockerhub'

        # call download_artifacts method
        result = validate_docker.download_artifacts()

        # Assert that the mock methods are called as expected
        self.assertEqual(result, True)
        mock_is_container_daemon_running.assert_called_once()

    @patch('validation_workflow.docker.validation_docker.ValidateDocker.check_http_request')
    @patch('validation_workflow.docker.validation_docker.ValidationArgs')
    @patch('validation_workflow.docker.validation_docker.InspectDockerImage')
    @patch('validation_workflow.docker.validation_docker.ApiTestCases')
    @patch('validation_workflow.docker.validation_docker.ValidateDocker.run_container')
    @patch('validation_workflow.docker.validation_docker.InspectDockerImage.inspect_digest')
    @patch('time.sleep', return_value=None)
    def test_staging(self, mock_time_sleep: Mock, mock_digest: Mock, mock_container: Mock, mock_test: Mock, mock_docker_image: Mock, mock_validation_args: Mock, mock_check_http: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.OS_image = 'opensearchstaging/opensearch-os'
        mock_validation_args.return_value.version = '1.0.0.1000'
        mock_validation_args.return_value.validate_digest_only = False
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_docker_image.return_value = MagicMock()
        mock_container.return_value = (True, 'test_file.yml')
        mock_test_apis_instance = mock_test.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 2)
        mock_digest.return_value = True
        mock_check_http.return_value = True

        # Create instance of ValidateDocker class
        validate_docker = ValidateDocker(mock_validation_args.return_value)
        validate_docker.image_ids = {'opensearch': 'images_id_0'}
        validate_docker.replacements = [('opensearchproject/opensearch:1', 'images_id_0')]

        # Call validation method and assert the result
        result = validate_docker.validation()
        self.assertTrue(result)

        # Assert that the mock methods are called as expected
        mock_container.assert_called_once()
        mock_test.assert_called_once()
        mock_test.assert_has_calls([call(), call().test_apis(['opensearch'])])

    @patch('validation_workflow.docker.validation_docker.ValidateDocker.check_http_request')
    @patch('validation_workflow.docker.validation_docker.ValidationArgs')
    @patch('validation_workflow.docker.validation_docker.InspectDockerImage')
    @patch('validation_workflow.docker.validation_docker.ApiTestCases')
    @patch('validation_workflow.docker.validation_docker.ValidateDocker.run_container')
    @patch('validation_workflow.docker.validation_docker.InspectDockerImage.inspect_digest')
    @patch('time.sleep', return_value=None)
    def test_digests(self, mock_time_sleep: Mock, mock_digest: Mock, mock_container: Mock, mock_test: Mock, mock_docker_image: Mock, mock_validation_args: Mock, mock_check_http: Mock) -> None:
        # Set up mock objects
        mock_validation_args.return_value.OS_image = 'opensearchstaging/opensearch-os'
        mock_validation_args.return_value.version = '1.0.0.1000'
        mock_validation_args.return_value.using_staging_artifact_only = False
        mock_validation_args.return_value.validate_digest_only = True
        mock_validation_args.return_value.projects = ["opensearch"]
        mock_docker_image.return_value = MagicMock()
        mock_container.return_value = (True, 'test_file.yml')
        mock_test_apis_instance = mock_test.return_value
        mock_test_apis_instance.test_apis.return_value = (True, 2)
        mock_digest.return_value = True
        mock_check_http.return_value = True

        # Create instance of ValidateDocker class
        validate_docker = ValidateDocker(mock_validation_args.return_value)

        validate_docker.image_names_list = ['opensearchproject/opensearch']
        validate_docker.image_ids = {'opensearch': 'images_id_0'}
        validate_docker.image_digests = [True]
        validate_docker.replacements = [('opensearchproject/opensearch:1', 'images_id_0')]

        # Call validation method and assert the result
        result = validate_docker.validation()
        self.assertTrue(result)

    @patch('validation_workflow.docker.validation_docker.ValidationArgs')
    def test_cleanup(self, mock_validation_args: Mock) -> None:

        # Create instance of ValidateDocker class
        validate_docker = ValidateDocker(mock_validation_args.return_value)

        # Call cleanup method
        with patch.object(validate_docker, 'cleanup_process') as mock_cleanup_process:
            mock_cleanup_process.return_value = True
            mock_cleanup_process.docker_command = 'mocked_command'
            # Call cleanup method
            result = validate_docker.cleanup()
            self.assertTrue(result)

    @patch('validation_workflow.docker.validation_docker.ValidationArgs')
    @patch('validation_workflow.docker.validation_docker.subprocess.run')
    @patch('validation_workflow.docker.validation_docker.os.remove')
    def test_cleanup_process(self, mock_os_remove: Mock, mock_subprocess_run: Mock, mock_validation_args: Mock) -> None:

        # Set up mock objects
        mock_validation_args.return_value = 'validation_args'
        mock_subprocess_run.return_value = subprocess.CompletedProcess(['command'], 0)

        # Create instance of class
        validate_docker = ValidateDocker(mock_validation_args)
        validate_docker._target_yml_file = 'validation_args'

        # Call method to test
        result = validate_docker.cleanup_process()

        # Assert that the method returned the expected result
        self.assertTrue(result)
        mock_subprocess_run.assert_called_with(
            'docker-compose -f validation_args down', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        mock_os_remove.assert_called_with('validation_args')

    @patch('validation_workflow.docker.validation_docker.ValidationArgs')
    @patch('validation_workflow.docker.validation_docker.ValidateDocker.pull_image')
    @patch.object(subprocess, 'run')
    def test_get_pull_image_id(self, mock_subprocess_run: Mock, mock_pull_image: Mock, mock_validation_args: Mock) -> None:

        # Set up mock objects
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_pull_image.return_value = 'opensearch/opensearch'

        # Create instance of class
        validate_docker = ValidateDocker(mock_validation_args)

        # Call method to test
        image_id = validate_docker.get_image_id('opensearch/opensearch', '1.0.0')

        # Assert that the method returned the expected result
        self.assertEqual(image_id, 'opensearch/opensearch')
        mock_pull_image.assert_called_once_with('opensearch/opensearch', '1.0.0')

    def test_docker_compose_files_exist(self) -> None:
        # set up docker-compose files
        docker_compose_file_v1_url = 'https://github.com/opensearch-project/opensearch-build/blob/main/docker/release/dockercomposefiles/docker-compose-1.x.yml'
        docker_compose_file_v2_url = 'https://github.com/opensearch-project/opensearch-build/blob/main/docker/release/dockercomposefiles/docker-compose-2.x.yml'

        self.assertTrue(urllib.request.urlopen(docker_compose_file_v1_url).getcode() == 200)
        self.assertTrue(urllib.request.urlopen(docker_compose_file_v2_url).getcode() == 200)


if __name__ == '__main__':
    unittest.main()
