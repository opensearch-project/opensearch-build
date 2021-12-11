# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest

from test_workflow.test_args_path_validator import TestArgsPathValidator


class TestTestArgsPathValidator(unittest.TestCase):
    def test(self):
        self.assertEqual(
            TestArgsPathValidator.validate("https://ci.opensearch.org/ci/dbc/bundle-build-dashboards/1.2.0/428"),
            "https://ci.opensearch.org/ci/dbc/bundle-build-dashboards/1.2.0/428"
        )

        self.assertEqual(
            TestArgsPathValidator.validate("test"),
            os.path.join(os.getcwd(), "test")
        )

        self.assertEqual(
            TestArgsPathValidator.validate("."),
            os.path.join(os.getcwd())
        )
