# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import base64
import unittest

from test_workflow.integ_test.utils import get_password, str_to_base64


class TestUtils(unittest.TestCase):
    def test_strong_password(self) -> None:
        self.assertEqual("admin", get_password("2.11.1"))
        self.assertEqual("myStrongPassword123!", get_password("3.0.0"))
        self.assertEqual("YWRtaW4=", get_password("2.11.1", True))
        self.assertEqual("bXlTdHJvbmdQYXNzd29yZDEyMyE=", get_password("2.12.0", True))

    def test_str_to_base64(self) -> None:
        value = "admin"
        result = base64.b64encode(value.encode("utf-8")).decode("utf-8")
        self.assertEqual(str_to_base64(value), result)
