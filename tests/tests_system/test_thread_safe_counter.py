# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from system.thread_safe_counter import ThreadSafeCounter


class TestThreadSafeCounter(unittest.TestCase):
    @patch("threading.Lock")
    def test_constructor(self, mock_lock: MagicMock) -> None:
        counter = ThreadSafeCounter()

        self.assertEqual(counter.call_count, 0)
        mock_lock.assert_called_once()

    @patch("threading.Lock")
    def test_thread_safe_count(self, mock_lock: MagicMock) -> None:
        counter = ThreadSafeCounter()

        counter.thread_safe_count()

        self.assertEqual(counter.call_count, 1)
