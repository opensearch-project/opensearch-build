# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest
from unittest.mock import patch

from system.execute import execute


class TestExecute(unittest.TestCase):
    def test_current_arch(self):
        results = execute("uname -m", "/")  # (0, 'x86_64\n', '')
        self.assertTrue(results[0] in [0, 1])
        self.assertTrue(results[1].strip() in ["x86_64", "aarch64", "arm64"])
