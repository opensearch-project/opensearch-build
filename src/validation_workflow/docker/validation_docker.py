# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import subprocess
import time
from subprocess import PIPE
from typing import Any

from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.docker.inspect_docker_image import InspectDockerImage
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateDocker(Validation):

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)

    def download_artifacts(self) -> bool:

        if (self.is_container_daemon_running()):

            # STEP 1 . pull the images for OS and OSD
            if (self.args.using_staging_artifact_only):
                self._OS_image_name = 'opensearchstaging/opensearch' if self.args.docker_source == 'dockerhub' else 'public.ecr.aws/opensearchstaging/opensearch'
                self._OSD_image_name = 'opensearchstaging/opensearch-dashboards' if self.args.docker_source == 'dockerhub' else 'public.ecr.aws/opensearchstaging/opensearch-dashboards'
                self.local_image_OS_id = self.get_image_id(self._OS_image_name, ValidationArgs().stg_tag('opensearch').replace(" ", ""))
                self.local_image_OSD_id = self.get_image_id(self._OSD_image_name, ValidationArgs().stg_tag('opensearch_dashboards').replace(" ", ""))
            else:
                self._OS_image_name = 'opensearchproject/opensearch' if self.args.docker_source == 'dockerhub' else 'public.ecr.aws/opensearchproject/opensearch'
                self._OSD_image_name = 'opensearchproject/opensearch-dashboards' if self.args.docker_source == 'dockerhub' else 'public.ecr.aws/opensearchproject/opensearch-dashboards'
                self.local_image_OS_id = self.get_image_id(self._OS_image_name, self.args.version)
                self.local_image_OSD_id = self.get_image_id(self._OSD_image_name, self.args.version)
            logging.info(f'the OS image ID is : {self.local_image_OS_id}')
            logging.info(f'the OSD image ID is : {self.local_image_OSD_id} \n\n')

            return True

        else:
            raise Exception('Docker Daemon is not running. Exiting the docker validation.')

    # Pass this method for docker as no installation required in docker
    def installation(self) -> bool:
        return True

    # Pass this method for docker and combine it with the following method because we want to Pass the digest validation in docker first before spinning up the docker container
    def start_cluster(self) -> bool:
        return True

    def validation(self) -> bool:
        # STEP 2 . inspect image digest between opensearchproject(downloaed/local) and opensearchstaging(dockerHub)
        if not self.args.using_staging_artifact_only:
            self._OS_inspect_digest = InspectDockerImage(self.local_image_OS_id, self.args.OS_image, self.args.version).inspect_digest()
            self._OSD_inspect_digest = InspectDockerImage(self.local_image_OSD_id, self.args.OSD_image, self.args.version).inspect_digest()

            if self._OS_inspect_digest and self._OSD_inspect_digest:
                logging.info('Image digest is validated.\n\n')
                if self.args.validate_digest_only:
                    return True
            else:
                logging.info('\n\nImage digest is Not validated. Exiting..\n\n')
                raise Exception('Image digest does not match between the opensearchstaging at dockerHub/ecr and opensearchproject at local download. Exiting the validation.')

        # STEP 3 . spin-up OS/OSD cluster
        if not self.args.validate_digest_only:
            return_code, self._target_yml_file = self.run_container(
                self._OS_image_name,
                self._OSD_image_name,
                self.args.version
            )
            if (return_code):
                logging.info('Cluster is running now')
                logging.info('Checking if cluster is ready for API test every 10 seconds\n\n')

                self.max_retry = 20
                self.retry_count = 0
                while self.retry_count < self.max_retry:
                    logging.info(f'sleeping 10sec for retry {self.retry_count + 1}/{self.max_retry}')
                    time.sleep(10)
                    if self.check_http_request():
                        logging.info('\n\ncluster is now ready for API test\n\n')
                        break
                    self.retry_count += 1
                else:
                    logging.warning(f"Maximum number of retries ({self.max_retry}) reached. Cluster is not ready for API test.")
                    raise Exception(f"Maximum number of retries ({self.max_retry}) reached. Cluster is not ready for API test.")

                # STEP 4 . OS, OSD API validation
                _test_result, _counter = ApiTestCases().test_cases()

                if (_test_result):
                    logging.info(f'All tests Pass : {_counter}')
                    return True
                else:
                    logging.info(f'Not all tests Pass : {_counter}')
                    self.cleanup()
                    raise Exception(f'Not all tests Pass : {_counter}')
            else:
                raise Exception('The container failed to start. Exiting the validation.')
        else:
            return True

    def check_http_request(self) -> bool:
        try:
            subprocess.check_output(['curl', 'https://localhost:9200', '-u', 'admin:admin', '--insecure'])
            logging.info('status code : 200')
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f'Error connecting to https://localhost:9200: {e}')
            return False

    def cleanup(self) -> bool:
        # clean up
        if self.args.validate_digest_only:
            return True
        if self.cleanup_process():
            logging.info('cleanup is completed')
            return True
        else:
            logging.info('cleanup is Not completed')
            return False

    def cleanup_process(self) -> bool:
        # stop the containers
        self.docker_compose_down = f'docker-compose -f {self._target_yml_file} down'
        result = subprocess.run(self.docker_compose_down, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        # remove docker-compose.yml from the tmp folder
        try:
            os.remove(self._target_yml_file)
        except OSError as e:
            logging.info("Error: %s - %s." % (e.filename, e.strerror))

        return('returncode=0' in (str(result)))

    def is_container_daemon_running(self) -> Any:
        try:
            subprocess.check_output(["docker", "info"])
            logging.info("Docker daemon is running.")
            return True
        except subprocess.CalledProcessError:
            logging.info("Docker daemon is not running.")
            return False

    def run_container(self, OpenSearch_image: str, OpenSearchDashboard_image: str, version: str) -> Any:
        self.docker_compose_files = {
            '1': 'docker-compose-1.x.yml',
            '2': 'docker-compose-2.x.yml'
        }

        self.tmp_dir = TemporaryDirectory()
        self.target_yml_file = os.path.join(self.tmp_dir.name, 'docker-compose.yml')

        self.version_number = version[0]
        if self.version_number in self.docker_compose_files:
            self.source_file = os.path.join('docker', 'release', 'dockercomposefiles', self.docker_compose_files[self.version_number])
            shutil.copy2(self.source_file, self.target_yml_file)

        if (self.args.using_staging_artifact_only):
            self.images_used = f'{OpenSearch_image}:{version}'
        else:
            self.images_used = f'{OpenSearch_image}:{version}'

        self.inplace_change(
            self.target_yml_file,
            f'opensearchproject/opensearch:{version[0]}',
            f'{OpenSearch_image}:{version}.{self.args.os_build_number}'
            if self.args.using_staging_artifact_only
            else f'{OpenSearch_image}:{version}'
        )

        self.inplace_change(
            self.target_yml_file,
            f'opensearchproject/opensearch-dashboards:{version[0]}',
            f'{OpenSearchDashboard_image}:{version}.{self.args.osd_build_number}'
            if self.args.using_staging_artifact_only
            else f'{OpenSearchDashboard_image}:{version}'
        )
        # spin up containers
        self.docker_compose_up = f'docker-compose -f {self.target_yml_file} up -d'
        result = subprocess.run(self.docker_compose_up, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return ('returncode=0' in (str(result)), self.target_yml_file)

    def inplace_change(self, filename: str, old_string: str, new_string: str) -> None:

        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                print('"{old_string}" not found in {filename}.'.format(**locals()))
                return

        with open(filename, 'w') as f:
            print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)

    def get_image_id(self, image_name: str, image_version: str) -> str:
        local_inspect = f"docker image inspect -f '{{{{ .Id }}}}' {image_name}:{image_version}"

        # Removing the image if it exists at local
        result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if (result_inspect.returncode == 0):
            logging.info(f'Image exists at local : {result_inspect.stdout} : {image_name}:{image_version}')
            logging.info(f'Overwriting the local image by pulling a fresh {image_name}:{image_version} from {self.args.docker_source}')
        else:
            logging.info(f'Image does not exist at local, proceed with Pull from the {self.args.docker_source}')

        return (self.pull_image(image_name, image_version))

    def pull_image(self, image_name: str, image_version: str) -> str:

        dockerHub_pull = f"docker pull {image_name}:{image_version}"
        local_inspect = f"docker image inspect -f '{{{{ .Id }}}}' {image_name}:{image_version}"

        # Pulling image from dockerHub and return the image Id
        logging.info(f'Pulling {image_name}:{image_version} from the {self.args.docker_source}')
        result_pull = subprocess.run(dockerHub_pull, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if (result_pull.returncode == 0):
            result_inspect = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            logging.info(f'Image is pulled at local : {result_inspect.stdout} : {image_name} : {image_version}')
            return (result_inspect.stdout)
        else:
            raise Exception(f'error on pulling image : return code {str(result_pull.returncode)}')
