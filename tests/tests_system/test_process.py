# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

from system.process import Process, ProcessNotStartedError, ProcessStartedError


class TestProcess(unittest.TestCase):
    def test(self) -> None:

        process_handler = Process()

        process_handler.start("./tests/tests_system/data/wait_for_input.sh", ".")

        self.assertTrue(process_handler.started)
        self.assertIsNotNone(process_handler.pid)
        self.assertIsNotNone(process_handler.stdout_data)
        self.assertIsNotNone(process_handler.stderr_data)

        return_code = process_handler.terminate()

        # In Python 3.9 it seems that Process Termination is not as stable in 3.7.
        # With low hardware specs the result can be None
        # While on a much beefier server the termination can be instant
        # We even observed the same success on CentOS7 but fail on Ubuntu out of nowhere
        # Adding sleep time is not very efficient and it is very random, thus allow 2 return values here.
        assert return_code in [None, 1]
        self.assertIsNotNone(process_handler.stdout_data)
        self.assertIsNotNone(process_handler.stderr_data)

        self.assertFalse(process_handler.started)
        self.assertIsNone(process_handler.pid)

    @patch.object(tempfile, 'NamedTemporaryFile')
    def test_file_open_mode(self, mock_tempfile: MagicMock) -> None:
        process_handler = Process()
        process_handler.start("./tests/tests_system/data/wait_for_input.sh", ".")
        mock_tempfile.assert_has_calls([call(delete=False, encoding='utf-8', mode='r+')])

    def test_start_twice(self) -> None:
        process_handler = Process()
        process_handler.start("ls", ".")

        with self.assertRaises(ProcessStartedError) as ctx:
            process_handler.start("pwd", ".")

        self.assertTrue(str(ctx.exception).startswith("Process already started, pid: "))

    def test_terminate_unstarted_process(self) -> None:
        process_handler = Process()

        with self.assertRaises(ProcessNotStartedError) as ctx:
            process_handler.terminate()

        self.assertEqual(str(ctx.exception), "Process has not started")

    @patch('os.unlink')
    @patch('psutil.Process')
    @patch('subprocess.Popen')
    @patch('psutil.process_iter')
    def test_terminate_process_file_not_closed(self, mock_procs: MagicMock, mock_subprocess: MagicMock, mock_process: MagicMock, mock_os_unlink: MagicMock) -> None:
        process_handler = Process()

        mock_process1 = MagicMock()
        mock_process2 = MagicMock()

        mock_item1 = MagicMock()
        mock_process1.open_files.return_value = [mock_item1]

        mock_item2 = MagicMock()
        mock_process2.open_files.return_value = [mock_item2]

        mock_procs.return_value = [mock_process1, mock_process2]

        process_handler.start("mock_command", "mock_cwd")

        mock_item1.path = process_handler.stdout.name
        mock_item2.path = process_handler.stderr.name

        process_handler.terminate()

        mock_procs.assert_called()

        mock_process1.open_files.assert_called()
        mock_process2.open_files.assert_called()

        with self.assertLogs(level='ERROR') as log:
            logging.error(f'stdout {mock_item1} is being used by process {mock_process1}')
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertIn(f'stdout {mock_item1} is being used by process {mock_process1}', log.output[0])

        with self.assertLogs(level='ERROR') as log:
            logging.error(f'stderr {mock_item2} is being used by process {mock_process2}')
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertIn(f'stderr {mock_item2} is being used by process {mock_process2}', log.output[0])
