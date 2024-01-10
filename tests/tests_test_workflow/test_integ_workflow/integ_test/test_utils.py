# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from test_workflow.integ_test.utils import get_password


class TestUtils(unittest.TestCase):
    def test_strong_password(self) -> None:
        self.assertEqual("admin", get_password("2.11.1"))
        self.assertEqual("myStrongPassword123!", get_password("3.0.0"))
