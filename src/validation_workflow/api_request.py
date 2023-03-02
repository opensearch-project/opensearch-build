#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
from typing import Any

"""
This class is to run API test againt on local OpenSearch API URL with default port 9200.
It returns response status code and the response content.
"""


class ApiTest:

    def __init__(self, request_url: str) -> None:
        self.request_url = request_url

    def api_get(self) -> Any:
        self.command = ['curl', self.request_url, '-u', 'admin:admin', '--insecure', '-i']
        result = subprocess.run(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = result.stdout.decode().strip()
        response_code = int(response.split()[1])
        response_content = response.split('\r\n\r\n', 1)[1]
        return response_code, response_content
