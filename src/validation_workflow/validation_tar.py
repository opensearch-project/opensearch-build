# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from validation_workflow.download_utils import DownloadUtils
from validation_workflow.validation import Validation


class ValidationTar(Validation, DownloadUtils):

    @classmethod
    def download_artifacts(self, projects: list, version: str) -> bool:
        architectures = ["x64", "arm64"]
        for project in projects:
            for architecture in architectures:
                url = f"{self.base_url}{project}/{version}/{project}-{version}-linux-{architecture}.tar.gz"
                if ValidationTar.is_url_valid(url) and ValidationTar.download(url, self.tmp_dir):
                    logging.info(f"Valid URL - {url} and Download Successful !")
                else:
                    logging.info(f"Invalid URL - {url}")
                    raise Exception(f"Invalid url - {url}")
        return True
