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

from validation_workflow.validation_args import ValidationArgs

"""
This class is to compare the image digest/SHA-256 on OS and OSD between opensearchproject(downloaded/local) and opensearchstaging(on dockerHub).
It retuns False if the digest does not match.
"""


class InspectDockerImage:

    def __init__(self, image_id: str, image_name: str, prod_image_tag: str) -> None:
        self.image_id = image_id
        self.image_name = image_name
        self.prod_image_tag = prod_image_tag
        self.image_tag = ValidationArgs().stg_tag('opensearch_dashboards').replace(" ", "") if ("dashboards" in self.image_name) else ValidationArgs().stg_tag('opensearch').replace(" ", "")
        self.auth_token_url = "https://auth.docker.io/token?"
        self.auth_service_scope = "service=registry.docker.io&scope=repository:"
        self.registry_url = "https://index.docker.io/v2/"
        self.access_type = 'Bearer'

    def inspect_digest(self) -> bool:

        logging.info('Fetching access token from dockerHub')
        api_url = f"{self.auth_token_url}{self.auth_service_scope}{self.image_name.replace('opensearchproject', 'opensearchstaging')}:pull"

        response = requests.get(api_url)
        response_dict = json.loads(response.text)

        logging.info('Fetching mainfest from DockerHub')
        api_url = f"{self.registry_url}{self.image_name.replace('opensearchproject', 'opensearchstaging')}/manifests/{self.image_tag}"
        access_token = response_dict['token']

        # set up all necessary token ( if you use VPN, it may slow down the response from dockerHub )
        headersToken = {
            "Authorization": f'{self.access_type} {access_token}',
            "Accept": "application/vnd.docker.distribution.manifest.list.v2+json",
            "Content-Type": "application/json;charset=UTF-8"
        }

        x = requests.get(api_url, headers=headersToken)
        dockerHub_repo_digest = x.headers.get('etag')
        logging.info(f'{dockerHub_repo_digest} <-- DockerHub image repon digest {self.image_name.replace("opensearchproject", "opensearchstaging")}:{self.image_tag}')

        logging.info('Fetching mainfest from local')
        local_inspect = f"docker image inspect --format '{{{{json .}}}}' {self.image_id} | jq -r '. | {{RepoDigests: .RepoDigests}}'"
        result = subprocess.run(local_inspect, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        response_dict = json.loads(result.stdout)
        local_image_digests = response_dict['RepoDigests']
        local_image_digest = local_image_digests[0].split("@")[1]
        formatted_local_image_digest = f'"{local_image_digest}"'
        logging.info(f'{formatted_local_image_digest} <-- local image repo digest {self.image_name}:{self.prod_image_tag}')

        return True if (formatted_local_image_digest == dockerHub_repo_digest) else False
