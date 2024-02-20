# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import logging
import os
import re
import shutil
import time
from abc import ABC, abstractmethod
from typing import Any

import requests

from system.temporary_directory import TemporaryDirectory
from validation_workflow.api_request import ApiTest
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation_args import ValidationArgs


class Validation(ABC):
    """
        Abstract class for all types of artifact validation
    """

    def __init__(self, args: ValidationArgs) -> None:
        self.args = args
        self.base_url_production = "https://artifacts.opensearch.org/releases/bundle/"
        self.base_url_staging = "https://ci.opensearch.org/ci/dbc/distribution-build-"
        self.tmp_dir = TemporaryDirectory()

    def check_url(self, url: str) -> bool:
        if DownloadUtils().download(url, self.tmp_dir) and DownloadUtils().is_url_valid(url):  # type: ignore
            logging.info(f"Valid URL - {url} and Download Successful !")
            return True
        else:
            raise Exception(f"Invalid url - {url}")

    def copy_artifact(self, filepath: str, tempdir_path: str) -> bool:
        if filepath:
            shutil.copy2(filepath, tempdir_path)
            return True
        else:
            raise Exception("Provided path for local artifacts does not exist")

    def check_for_security_plugin(self, work_dir: str) -> bool:
        path = os.path.exists(os.path.join(work_dir, "plugins", "opensearch-security"))
        return path

    def get_version(self, project: str) -> str:
        return re.search(r'(\d+\.\d+\.\d+)', os.path.basename(project)).group(1)

    def run(self) -> Any:
        try:
            return self.download_artifacts() and self.installation() and self.start_cluster() and self.validation() and self.cleanup()
        except Exception as e:
            raise Exception(f'An error occurred while running the validation tests: {str(e)}')

    def download_artifacts(self) -> bool:
        isFilePathEmpty = bool(self.args.file_path)
        for project in self.args.projects:
            if (isFilePathEmpty):
                if ("https:" not in self.args.file_path.get(project)):
                    self.copy_artifact(self.args.file_path.get(project), str(self.tmp_dir.path))
                else:
                    self.args.version = self.get_version(self.args.file_path.get(project))
                    self.check_url(self.args.file_path.get(project))
            else:
                self.args.file_path[project] = self.get_filepath(project)
                self.check_url(self.args.file_path.get(project))
        return True

    def get_filepath(self, project: str) -> str:
        file_name_suffix = "tar.gz" if self.args.distribution == "tar" else self.args.distribution
        if self.args.artifact_type == "staging":
            if self.args.distribution == "yum":
                return (
                    f"{self.base_url_staging}{project}/{self.args.version}/{self.args.build_number[project]}/{self.args.platform}/"
                    f"{self.args.arch}/rpm/dist/{project}/{project}-{self.args.version}.staging.repo"
                )
            return (
                f"{self.base_url_staging}{project}/{self.args.version}/{self.args.build_number[project]}/{self.args.platform}/"
                f"{self.args.arch}/{self.args.distribution}/dist/{project}/{project}-{self.args.version}-{self.args.platform}-"
                f"{self.args.arch}.{file_name_suffix}"
            )
        if self.args.distribution == "yum":
            return f"{self.base_url_production}{project}/{self.args.version[0:1]}.x/{project}-{self.args.version[0:1]}.x.repo"
        return f"{self.base_url_production}{project}/{self.args.version}/{project}-{self.args.version}-{self.args.platform}-{self.args.arch}.{file_name_suffix}"

    def check_cluster_readiness(self) -> bool:
        max_retry = 20
        retry_count = 0
        while retry_count < max_retry:
            logging.info(f'Sleeping 5sec for retry {retry_count + 1}/{max_retry}')
            time.sleep(5)
            if self.check_http_request():
                logging.info('\n\nCluster is now ready for API test\n\n')
                return True
            retry_count += 1
        logging.error(f"Maximum number of retries ({max_retry}) reached. Cluster is not ready for API test.")
        return False

    def check_http_request(self) -> bool:
        self.test_readiness_urls = {
            'https://localhost:9200': 'opensearch cluster API'
        }
        if 'opensearch-dashboards' in self.args.projects:
            self.test_readiness_urls['http://localhost:5601/api/status'] = 'opensearch-dashboards API'
        for url, name in self.test_readiness_urls.items():
            try:
                status_code, response_text = ApiTest(url, self.args.version).api_get()
                if status_code != 200:
                    logging.error(f'Error connecting to {name} ({url}): status code {status_code}')
                    return False
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
                logging.error(f'Error connecting to {name} ({url}): {e}')
                return False
        return True

    @abstractmethod
    def installation(self) -> bool:
        pass

    @abstractmethod
    def start_cluster(self) -> bool:
        pass

    @abstractmethod
    def validation(self) -> bool:
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        pass
