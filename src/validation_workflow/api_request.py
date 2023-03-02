#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any

import subprocess

"""
This class is to run API test againt on local OpenSearch API URL with default port 9200.
It returns response status code and the response content.
"""


class ApiTest:

    def __init__(self, request_url: str) -> None:
        self.request_url = request_url

    def api_get(self) -> Any:
        self.command = ['curl', self.request_url, '-u', 'admin:admin', '--insecure']
        result = subprocess.run(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode, result.stdout.decode('utf-8')
