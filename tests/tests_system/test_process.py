# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from system.process import Process


class TestProcess(unittest.TestCase):
    def test(self):

        process_handler = Process(".")

        process_handler.start("ls", ".")

        self.assertIsNotNone(process_handler.get_pid())

        process_handler.terminate()

        self.assertIsNone(process_handler.get_pid())

        # clean up
        os.remove("stdout.txt")
        os.remove("stderr.txt")

    # TODO: add test for subprocess.TimeoutExpired
