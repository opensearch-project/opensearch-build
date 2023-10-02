# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os

import requests

from system.temporary_directory import TemporaryDirectory


class DownloadUtils:
    @staticmethod
    def is_url_valid(url: str) -> bool:
        response = requests.head(url)
        status = bool(response.status_code in [200, 302])
        return status

    @staticmethod
    def download(url: str, tmp_dir: TemporaryDirectory) -> bool:
        # This method writes the contents from the response object into temporary directory file name fetched from the end of the url.
        response = requests.get(url, stream=True)
        path = os.path.join(tmp_dir.name, os.path.basename(url))
        status = bool(open(path, "wb").write(response.content))
        return status
