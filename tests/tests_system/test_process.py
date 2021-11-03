# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from system.process import Process


class TestProcess(unittest.TestCase):
    def test(self):

        process_handler = Process(".")

        process_handler.start("ls", ".")

        self.assertIsNotNone(process_handler.pid)

        process_handler.terminate()

        self.assertIsNone(process_handler.pid)

    # TODO: add test for subprocess.TimeoutExpired
