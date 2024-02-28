#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any

import requests

from test_workflow.integ_test.utils import get_password, str_to_base64

"""
This class is to run API test againt on local OpenSearch API URL with default port 9200.
It returns response status code and the response content.
"""


class ApiTest:

    def __init__(self, request_url: str, version: str) -> None:
        self.request_url = request_url
        self.apiHeaders_auth = {"Authorization": f'Basic {str_to_base64("admin:" + get_password(version))}'}  # user/pass "admin/pass" in Base64 format fetched from get_password() method
        self.apiHeaders_accept = {"Accept": "*/*"}
        self.apiHeaders_content_type = {"Content-Type": "application/json"}
        self.apiHeaders = {}
        self.apiHeaders.update(self.apiHeaders_auth)
        self.apiHeaders.update(self.apiHeaders_accept)
        self.apiHeaders.update(self.apiHeaders_content_type)

    def api_get(self) -> Any:

        response = requests.get(self.request_url, headers=self.apiHeaders, verify=False)
        return response.status_code, response.text
