# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from system.temporary_directory import TemporaryDirectory
from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation


class ValidationRpm(Validation, DownloadUtils):

    @classmethod
    def download_artifacts(self, projects: list, version: str, platform: str, architectures: list) -> bool:
        tmp_dir = TemporaryDirectory()
        for project in projects:
            for architecture in architectures:
                url = f"{self.url}{project}/{version}/{project}-{version}-{platform}-{architecture}.rpm"
                if ValidationRpm.is_url_valid(url) and ValidationRpm.download(url, tmp_dir):
                    logging.info(f" Valid URL - {url} and Download Successful !")
                else:
                    logging.info(f"Invalid URL - {url}")
                    raise Exception("Invalid url - check version")
        return True
