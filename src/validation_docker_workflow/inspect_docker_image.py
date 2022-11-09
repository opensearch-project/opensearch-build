#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import json
import logging
import subprocess
from subprocess import PIPE

import requests

auth_token_url = "https://auth.docker.io/token?"
auth_service_scope = "service=registry.docker.io&scope=repository:"
registry_url = "https://index.docker.io/v2/"
access_type = 'Bearer'

"""
This class is to compare the image digest/SHA-256 on OS and OSD between opensearchproject(downloaded/local) and opensearchstaging(on dockerHub).
It retuns False if the digest does not match.
"""


class InspectDockerImage():
    @staticmethod
    def inspect_digest(image_short_id, image_name) -> None:
        logging.info('Fetching token')
        # api_url = auth_token_url + auth_service_scope + image_name.split(':')[0].replace("opensearchproject","opensearchstaging") + ":pull"
        api_url = auth_token_url + auth_service_scope + image_name.split(':')[0] + ":pull"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)

        logging.info('Fetching mainfest from DockerHub')
        # api_url = registry_url + image_name.split(':')[0].replace("opensearchproject","opensearchstaging") + "/manifests/" + image_name.split(':')[1]
        api_url = registry_url + image_name.split(':')[0] + "/manifests/" + image_name.split(':')[1]
        access_token = response_dict['token']

        # set up all necessary token ( if you use VPN, it may slow down the response from dockerHub )
        headersToken = {
            "Authorization": f'{access_type} {access_token}',
            "Accept": "application/vnd.docker.distribution.manifest.v2+json",
            "Content-Type": "application/json;charset=UTF-8"
        }

        x = requests.get(api_url, headers=headersToken)
        response_dict = json.loads(x.text)
        dockerHub_image_digest = response_dict['config']['digest']
        logging.info(dockerHub_image_digest + " --> DockerHub image digest" + image_name)

        logging.info('Fetching mainfest from local')
        local_inspect = "docker image inspect --format '{{json .}}' " + image_short_id + " | jq -r '. | {Id: .Id}'"
        result = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        response_dict = json.loads(result.stdout)
        local_image_digest = response_dict['Id']
        logging.info(local_image_digest + " --> local image digest" + image_name)

        return (local_image_digest == dockerHub_image_digest)
