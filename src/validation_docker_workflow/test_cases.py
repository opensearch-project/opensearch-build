# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
from typing import Any

from validation_docker_workflow.api_test import ApiTest

"""
This class, STEP4, is just the collection of test cases to run.
"""


class TestCases():

    @staticmethod
    def test_cases() -> Any:

        success_counter = 0
        fail_counter = 0
        # STEP 4 . OS, OSD API validation
        # Test case 1 . Get cluster info
        status_code, response_text = ApiTest.api_test("")
        if (status_code == 200):
            logging.info('response code : ' + str(status_code) + ' result :\n' + response_text + '\n\n')
            success_counter += 1
        else:
            logging.info('response error code :' + str(status_code))
            fail_counter += 1

        # Test case 2 . Get plugin info
        status_code, response_text = ApiTest.api_test("_cat/plugins?v")
        if (status_code == 200):
            logging.info('response code : ' + str(status_code) + ' result :\n' + response_text + '\n\n')
            success_counter += 1
        else:
            logging.info('response error code :' + str(status_code))
            fail_counter += 1

        # Test case 3 . Get health info
        status_code, response_text = ApiTest.api_test("_cat/health?v")
        if (status_code == 200):
            logging.info('response code : ' + str(status_code) + ' result :\n' + response_text + '\n\n')
            success_counter += 1
        else:
            logging.info('response error code :' + str(status_code))
            fail_counter += 1

        return (fail_counter == 0, "There are " + str(success_counter) + "/" + str(success_counter + fail_counter) + " test cases Pass")
