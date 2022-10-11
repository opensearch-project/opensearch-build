# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import requests


class DownloadUtils:
    @staticmethod
    def is_url_valid(url: str) -> int:
        response = requests.head(url)
        if response.status_code == 200:
            return 'content-length' in response.headers
        else:
            return 0

    @staticmethod
    def download(url: str) -> None:
        response = requests.get(url, stream=True)
        open(url.split("/")[-1], "wb").write(response.content)
