import subprocess
import unittest
from unittest.mock import MagicMock

from src.system.arch import current_arch


class ArchTests(unittest.TestCase):
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
