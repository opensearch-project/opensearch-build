#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import requests
from typing import Any

apiURL = "https://127.0.0.1:9200/"  # default localhost OS API URL and port assigned in docker-compose.yml
apiHeaders_auth = {"Authorization": "Basic YWRtaW46YWRtaW4="}  # default user/pass "admin/admin"
apiHeaders_accept = {"Accept": "*/*"}
apiHeaders_content_type = {"Content-Type": "application/json"}
apiHeaders = {}
apiHeaders.update(apiHeaders_auth)
apiHeaders.update(apiHeaders_accept)
apiHeaders.update(apiHeaders_content_type)

"""
This class is to run API test againt on local OpenSearch API URL with default port 9200.
It returns response status code and the response content.
"""


class ApiTest:

    @classmethod
    def api_test(self, api_request: str) -> Any:

        response = requests.get(apiURL + api_request, headers=apiHeaders, verify=False)
        return response.status_code, response.text
