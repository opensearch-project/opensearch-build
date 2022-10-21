# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import requests

from system.temporary_directory import TemporaryDirectory


class DownloadUtils:
    @staticmethod
    def is_url_valid(url: str) -> int:
        response = requests.head(url)
        if response.status_code == 200:
            return 1
        else:
            return 0

    @staticmethod
    def download(url: str, tmp_dir: TemporaryDirectory) -> bool:
        response = requests.get(url, stream=True)  # get() method sends a GET request to the url
        path = tmp_dir.name + "/" + url.split("/")[-1]
        val = bool(open(path, "wb").write(response.content))  # writes the contents from the response object into temporary directory file name fetched from the end of the url
        return val
