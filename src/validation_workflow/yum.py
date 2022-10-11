# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from .download_utils import DownloadUtils
from .validation import Validation


class Yum(Validation, DownloadUtils):
    @classmethod
    def get_architectures(cls) -> list:
        pass

    @classmethod
    def download_urls(cls, projects: list, version: str, platform: str) -> None:
        for project in projects:
            url = f"https://artifacts.opensearch.org/releases/bundle/{project}/2.x/{project}-2.x.repo"
            if Yum.is_url_valid(url):
                print(f"Valid URL - {url}")
                Yum.download(url)
                print("Download Successful !")
            else:
                print(f"Invalid URL - {url}")
