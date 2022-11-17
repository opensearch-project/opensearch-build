# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation


class ValidationYum(Validation, DownloadUtils):

    @classmethod
    def download_artifacts(self, projects: list, version: str) -> bool:
        for project in projects:
            url = f"{self.base_url}{project}/{version[0:1]}.x/{project}-{version[0:1]}.x.repo"
            if ValidationYum.is_url_valid(url) and ValidationYum.download(url, self.tmp_dir):
                logging.info(f"Valid URL - {url} and Download Successful !")
            else:
                logging.info(f"Invalid URL - {url}")
                raise Exception(f"Invalid url - {url}")
        return True
