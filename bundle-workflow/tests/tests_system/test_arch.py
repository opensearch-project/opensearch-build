# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest
from unittest.mock import patch

from system.arch import current_arch


class TestArch(unittest.TestCase):
    def test_current_arch(self):
        self.assertTrue(current_arch() in ["x64", "arm64"])

    @patch("subprocess.check_output", return_value="x86_64".encode())
    def test_x86_64_return_x64_arch(self, mock_subprocess):
        self.assertTrue(current_arch() == "x64")

    @patch("subprocess.check_output", return_value="aarch64".encode())
    def test_aarch64_return_arm64_arch(self, mock_subprocess):
        self.assertTrue(current_arch() == "arm64")

    @patch("subprocess.check_output", return_value="arm64".encode())
    def test_arm64_return_arm64_arch(self, mock_subprocess):
        self.assertTrue(current_arch() == "arm64")

    @patch("subprocess.check_output", return_value="invalid".encode())
    def test_invalid_arch(self, mock_subprocess):
        with self.assertRaises(ValueError) as context:
            current_arch()
        self.assertEqual("Unsupported architecture: invalid", str(context.exception))

    @patch("subprocess.check_output", return_value="x86_64".encode())
    def test_subprocess_call(self, mock_subprocess):
        current_arch()
        subprocess.check_output.assert_called_with(["uname", "-m"])
