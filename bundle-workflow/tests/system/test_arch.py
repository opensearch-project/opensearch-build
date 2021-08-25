# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest
from unittest.mock import MagicMock

from src.system.arch import current_arch


class TestArch(unittest.TestCase):
    def test_current_arch(self):
        self.assertTrue(current_arch() in ["x64", "arm64"])

    def test_invalid_arch(self):
        subprocess.check_output = MagicMock(return_value="invalid".encode())
        with self.assertRaises(ValueError) as context:
            current_arch()
        subprocess.check_output.assert_called_with(["uname", "-m"])
        self.assertEqual(
            "Unsupported architecture: invalid", context.exception.__str__()
        )
