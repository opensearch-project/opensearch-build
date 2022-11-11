#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import sys
import time

from system import console
from validation_docker_workflow.api_test import ApiTest
from validation_docker_workflow.check_docker_daemon import DockerDaemonRunning
from validation_docker_workflow.cleanup_docker import CleanupDocker
from validation_docker_workflow.inspect_docker_image import InspectDockerImage
from validation_docker_workflow.pull_docker_image import PullDockerImage
from validation_docker_workflow.spinup_docker_container import RunDocker
from validation_docker_workflow.validation_dockerecr_args import DockerEcrArgs


# Validate the OpenSearch distribution artifacts on DockerHub - https://github.com/opensearch-project/opensearch-build/issues/2759
def main() -> int:

    args = DockerEcrArgs()
    console.configure(level=args.logging_level)

    # Check if the docker daemon is running; or else, bring it up
    if (DockerDaemonRunning.is_container_daemon_running() == 0):
        logging.info('docker_daemon is running')

        # STEP 1 . pull the images for OS and OSD
        local_image_OS_id = PullDockerImage.pull_image(args.OS_image, args.OS_image_version)
        local_image_OSD_id = PullDockerImage.pull_image(args.OSD_image, args.OSD_image_version)
        logging.info('the OS image ID is : ' + local_image_OS_id)
        logging.info('the OSD image ID is : ' + local_image_OSD_id + '\n\n')

        # STEP 2 . inspect image digest betwwen opensearchproject(downloaed/local) and opensearchstaging(dockerHub)
        if (InspectDockerImage.inspect_digest(local_image_OS_id, args.OS_image, args.OS_image_version)) \
                and (InspectDockerImage.inspect_digest(local_image_OSD_id, args.OSD_image, args.OSD_image_version)):
            logging.info('Image digest is validated\n\n')

            # STEP 3 . spin-up OS/OSD cluster
            return_code, target_yml_file = RunDocker.run_container(
                args.OS_image,
                args.OSD_image,
                args.OS_image_version,
                args.OSD_image_version,
                'opensearch-node1-test',
                'opensearch-node2-test',
                'opensearch-dashboards-test',
            )
            if (return_code):
                logging.info('Cluster is running now')
                logging.info('Sleeping 2 minutes for cluster to be ready for API test\n\n')
                time.sleep(120)

                # STEP 4 . OS, OSD API validation
                # Test case 1 . Get cluster info
                status_code, response_text = ApiTest.api_test("")
                logging.info('response code : ' + str(status_code) + ' result : \n' + response_text + '\n\n') if (status_code == 200) else logging.info('response error code :' + str(status_code))

                # Test case 2 . Get plugin info
                status_code, response_text = ApiTest.api_test("_cat/plugins?v")
                logging.info('response code : ' + str(status_code) + ' result : \n' + response_text + '\n\n') if (status_code == 200) else logging.info('response error code :' + str(status_code))

                # Test case 3 . Get health info
                status_code, response_text = ApiTest.api_test("_cat/health?v")
                logging.info('response code : ' + str(status_code) + ' result : \n' + response_text + '\n\n') if (status_code == 200) else logging.info('response error code :' + str(status_code))

                # clean up
                CleanupDocker.cleanup('opensearch-node1-test', 'opensearch-node2-test', 'opensearch-dashboards-test', target_yml_file)
                return 0
            else:
                logging.info('The container is fail to run. Exiting the validation.')
                return False
        else:
            logging.info('Image digest does not match between the opensearchstaging at dockerHub and opensearchproject at local download. Exiting the validation.')
            return False
    else:
        logging.info('docker_daemon check is fail. Exiting the validation.')
        return False


if __name__ == "__main__":
    sys.exit(main())
