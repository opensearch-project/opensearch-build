# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest

from system.execute import execute


class TestExecute(unittest.TestCase):
    def test_execute_status_capture_true_raise_false(self) -> None:
        (status, stdout, stderr) = execute("echo output && exit 128", "/", capture=True, raise_on_failure=False)  # (128, 'output', '')
        self.assertEqual(status, 128)
        self.assertEqual(stdout.strip(), "output")
        self.assertEqual(stderr.strip(), "")

    def test_execute_status_capture_false_raise_false(self) -> None:
        (status, stdout, stderr) = execute("echo output && exit 128", "/", capture=False, raise_on_failure=False)  # (128, None, None)
        self.assertEqual(status, 128)
        self.assertEqual(stdout, None)
        self.assertEqual(stderr, None)

    def test_execute_status_capture_true_raise_True(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError) as context:
            (status, stdout, stderr) = execute("echo output && exit 128", "/", capture=True, raise_on_failure=True)  # (128, 'error', '')
        self.assertEqual(
            "Command 'echo output && exit 128' returned non-zero exit status 128.",
            str(context.exception),
        )

    def test_execute_stdout(self) -> None:
        (status, stdout, stderr) = execute("echo success", "/")  # (0, 'success\n', '')
        self.assertEqual(status, 0)
        self.assertEqual(stdout.strip(), "success")
        self.assertEqual(stderr.strip(), "")

    def test_execute_stderr(self) -> None:
        (status, stdout, stderr) = execute(">&2 echo error", "/")  # (0, '', 'error\n')
        self.assertEqual(status, 0)
        self.assertEqual(stdout.strip(), "")
        self.assertEqual(stderr.strip(), "error")
