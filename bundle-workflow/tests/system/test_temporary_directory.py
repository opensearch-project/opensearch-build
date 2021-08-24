# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import unittest

from src.system.temporary_directory import TemporaryDirectory


class TestTemporaryDirectory(unittest.TestCase):
    def test_keep_true(self):
        with TemporaryDirectory(keep=True) as work_dir:
            self.assertTrue(os.path.exists(work_dir))
        self.assertTrue(os.path.exists(work_dir))

    def test_keep_false(self):
        with TemporaryDirectory() as work_dir:
            self.assertTrue(os.path.exists(work_dir))
        self.assertFalse(os.path.exists(work_dir))
