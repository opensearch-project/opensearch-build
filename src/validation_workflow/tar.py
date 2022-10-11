# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from .download_utils import DownloadUtils
from .validation import Validation


class Tar(Validation, DownloadUtils):
    @classmethod
    def get_architectures(cls) -> list:
        return ["x64", "arm64"]

    @classmethod
    def download_urls(cls, projects: list, version: str, platform: str) -> None:
        for project in projects:
            for package_type in cls.get_architectures():
                url = f"https://artifacts.opensearch.org/releases/bundle/{project}/{version}/{project}-{version}-{platform}-{package_type}.tar.gz"
                if Tar.is_url_valid(url):
                    print(f"Valid URL - {url}")
                    Tar.download(url)
                    print("Download Successful !")
                else:
                    print(f"Invalid URL - {url}")
