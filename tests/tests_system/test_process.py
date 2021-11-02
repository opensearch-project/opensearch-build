# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest

from system.process import terminate


class TestProcess(unittest.TestCase):
    def test_terminate(self):
        work_dir = "."

        stdout = open("unit_test_stdout.txt", "w+")
        stderr = open("unit_test_stderr.txt", "w+")

        process = subprocess.Popen(
            "ls",
            cwd=".",
            shell=True,
            stdout=stdout,
            stderr=stderr,
        )

        self.assertIsNotNone(process)

        terminated_process, local_cluster_stderr, local_cluster_stdout, return_code = terminate(process, work_dir, stdout, stderr)

        self.assertIsNone(terminated_process)
        self.assertIsNotNone(local_cluster_stdout)
