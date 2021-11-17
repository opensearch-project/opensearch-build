# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from system.process import Process, ProcessNotStartedError, ProcessStartedError


class TestProcess(unittest.TestCase):
    def test(self):

        process_handler = Process()

        process_handler.start("./tests/tests_system/data/wait_for_input.sh", ".")

        self.assertTrue(process_handler.started)
        self.assertIsNotNone(process_handler.pid)
        self.assertIsNotNone(process_handler.output)
        self.assertEqual(process_handler.output.mode, "r+")
        self.assertIsNotNone(process_handler.error)
        self.assertEqual(process_handler.error.mode, "r+")

        return_code, stdout_data, stderr_data = process_handler.terminate()

        self.assertIsNone(return_code)
        self.assertIsNotNone(stdout_data)
        self.assertIsNotNone(stderr_data)

        self.assertFalse(process_handler.started)
        self.assertIsNone(process_handler.pid)
        self.assertIsNone(process_handler.output)
        self.assertIsNone(process_handler.error)

    def test_start_twice(self):
        process_handler = Process()
        process_handler.start("ls", ".")

        with self.assertRaises(ProcessStartedError) as ctx:
            process_handler.start("pwd", ".")

        self.assertTrue(str(ctx.exception).startswith("Process already started, pid: "))

    def test_terminate_unstarted_process(self):
        process_handler = Process()

        with self.assertRaises(ProcessNotStartedError) as ctx:
            process_handler.terminate()

        self.assertEqual(str(ctx.exception), "Process has not started")
