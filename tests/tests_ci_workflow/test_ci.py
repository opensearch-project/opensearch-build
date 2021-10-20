# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock

from ci_workflow.ci import Ci


class TestCi(unittest.TestCase):
    def setUp(self):
        self.ci = Ci("component", MagicMock(dir="/tmp/checked-out-component"), MagicMock())

    def test_ci(self):
        self.assertEqual(self.ci.component, "component")

    def test_check(self):
        pass
