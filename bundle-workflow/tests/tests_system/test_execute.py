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
    def test_execute_stdout(self):
        (status, stdout, stderr) = execute("echo success", "/")  # (0, 'success\n', '')
        self.assertEqual(status, 0)
        self.assertEqual(stdout.strip(), "success")
        self.assertEqual(stderr.strip(), "")

    def test_execute_stderr(self):
        (status, stdout, stderr) = execute(">&2 echo error", "/")  # (0, '', 'error\n')
        self.assertEqual(status, 0)
        self.assertEqual(stdout.strip(), "")
        self.assertEqual(stderr.strip(), "error")
