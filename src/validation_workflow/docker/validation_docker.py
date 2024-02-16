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
from subprocess import PIPE
from typing import Any

from test_workflow.integ_test.utils import get_password
from validation_workflow.api_test_cases import ApiTestCases
from validation_workflow.docker.inspect_docker_image import InspectDockerImage
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ValidateDocker(Validation):

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)

    def download_artifacts(self) -> bool:
        try:
            assert self.is_container_daemon_running(), 'Docker daemon is not running. Exiting the docker validation.'

            # STEP 1 . pull the images for OS and OSD
            product_names = self.args.projects
            using_staging_artifact_only = 'staging' if self.args.using_staging_artifact_only else 'production'
            get_image_id = lambda product: self.get_image_id(  # noqa: E731
                self.get_artifact_image_name(product, using_staging_artifact_only),
                self.args.version if not self.args.using_staging_artifact_only else ValidationArgs().stg_tag(product).replace(" ", ""))
            self.image_ids = {key: value for key, value in zip(product_names, list(map(get_image_id, product_names)))}
            self.image_ids = {key: value.strip() for key, value in self.image_ids.items()}

            return True

        except AssertionError as e:
            logging.error(str(e))
            return False

        finally:
            logging.info('Docker images are downloaded')

    # Pass this method for docker as no installation required in docker
    def installation(self) -> bool:
        return True

    # Pass this method for docker and combine it with the following method because we want to Pass the digest validation in docker first before spinning up the docker container
    def start_cluster(self) -> bool:
        return True

    def validation(self) -> bool:
        # STEP 2 . inspect image digest between opensearchproject(downloaded/local) and opensearchstaging(dockerHub)
        if not self.args.using_staging_artifact_only:
            self.image_names_list = ['opensearchproject/' + project for project in self.args.projects]
            self.image_digests = list(map(lambda x: self.inspect_docker_image(x[0], x[1]), zip(self.image_ids.values(), self.image_names_list)))  # type: ignore
            if all(self.image_digests):
                logging.info('Image digest is validated.\n\n')
                if self.args.validate_digest_only:
                    return True
            else:
                logging.info('\n\nImage digest is Not validated. Exiting..\n\n')
                raise Exception('Image digest does not match between the opensearchstaging at dockerHub/ecr and opensearchproject at local download. Exiting the validation.')

        # STEP 3 . spin-up OS/OSD cluster
        if not self.args.validate_digest_only:
            return_code, self._target_yml_file = self.run_container(
                self.image_ids,
                self.args.version
            )
            if return_code:
                logging.info('Checking if cluster is ready for API test in every 5 seconds\n\n')

                if self.check_cluster_readiness():
                    # STEP 4 . OS, OSD API validation
                    _test_result, _counter = ApiTestCases().test_apis(self.args.version, self.args.projects, True)

                    if _test_result:
                        logging.info(f'All tests Pass : {_counter}')
                        return True
                    else:
                        logging.info(f'Not all tests Pass : {_counter}')
                        self.cleanup()
                        raise Exception(f'Not all tests Pass : {_counter}')
                else:
                    raise Exception("Cluster is not ready for API test.")
            else:
                raise Exception('The container failed to start. Exiting the validation.')

        return True

    def cleanup(self) -> bool:
        try:
            # clean up
            if self.args.validate_digest_only:
                return True
            if self.cleanup_process():
                logging.info('cleanup is complete')
                return True
            else:
                logging.info('cleanup is not complete')
                return False
        except Exception as e:
            logging.error(f'An error occurred during cleanup: {e}')
            return False
        finally:
            logging.info('Docker validation cleanup is complete')

    def cleanup_process(self) -> bool:
        # stop the containers
        self.docker_compose_down = f'docker-compose -f {self._target_yml_file} down'
        result = subprocess.run(self.docker_compose_down, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        # remove docker-compose.yml from the tmp folder
        try:
            os.remove(self._target_yml_file)
        except OSError as e:
            logging.error("Error: %s - %s." % (e.filename, e.strerror))

        return('returncode=0' in (str(result)))

    def get_artifact_image_name(self, artifact: str, using_staging_artifact_only: str) -> Any:
        self.image_names = {
            'dockerhub': {
                'opensearch': {
                    'staging': 'opensearchstaging/opensearch',
                    'production': 'opensearchproject/opensearch'
                },
                'opensearch-dashboards': {
                    'staging': 'opensearchstaging/opensearch-dashboards',
                    'production': 'opensearchproject/opensearch-dashboards'
                }
            },
            'ecr': {
                'opensearch': {
                    'staging': 'public.ecr.aws/opensearchstaging/opensearch',
                    'production': 'public.ecr.aws/opensearchproject/opensearch'
                },
                'opensearch-dashboards': {
                    'staging': 'public.ecr.aws/opensearchstaging/opensearch-dashboards',
                    'production': 'public.ecr.aws/opensearchproject/opensearch-dashboards'
                }
            }
        }
        return self.image_names[self.args.docker_source][artifact][using_staging_artifact_only]

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

    def inplace_change(self, filename: str, old_string: str, new_string: str) -> None:
        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                logging.info
                ('"{old_string}" not found in {filename}.'.format(**locals()))
                return
        with open(filename, 'w') as f:
            logging.info('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)

    def inspect_docker_image(self, image_id: str, image_name: str) -> Any:
        return InspectDockerImage(image_id, image_name, self.args.version).inspect_digest()

    def is_container_daemon_running(self) -> Any:
        try:
            subprocess.check_output(["docker", "info"])
            logging.info("Docker daemon is running")
            return True
        except subprocess.CalledProcessError:
            logging.info("Docker daemon is not running")
            return False

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

    def run_container(self, image_ids: dict, version: str) -> Any:
        self.docker_compose_files = {
            '1': 'docker-compose-1.x.yml',
            '2': 'docker-compose-2.x.yml'
        }

        self.target_yml_file = os.path.join(self.tmp_dir.name, 'docker-compose.yml')

        self.major_version_number = version[0]

        self.source_file = os.path.join('docker', 'release', 'dockercomposefiles', self.docker_compose_files[self.major_version_number])
        shutil.copy2(self.source_file, self.target_yml_file)

        self.replacements = [(f'opensearchproject/{key}:{self.major_version_number}', value) for key, value in image_ids.items()]

        list(map(lambda r: self.inplace_change(self.target_yml_file, r[0], r[1]), self.replacements))
        os.environ["OPENSEARCH_INITIAL_ADMIN_PASSWORD"] = get_password(str(version))
        # spin up containers
        services = "opensearch-node1 opensearch-node2" if "opensearch-dashboards" not in self.args.projects else ""
        self.docker_compose_up = f'docker-compose -f {self.target_yml_file} up -d {services}'
        result = subprocess.run(self.docker_compose_up, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return ('returncode=0' in (str(result)), self.target_yml_file)
