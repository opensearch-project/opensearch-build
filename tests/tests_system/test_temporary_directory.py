# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import stat
import unittest
from pathlib import Path

from system.temporary_directory import TemporaryDirectory


class TestTemporaryDirectory(unittest.TestCase):
    def test_keep_true(self) -> None:
        with TemporaryDirectory(keep=True) as work_dir:
            self.assertTrue(os.path.exists(work_dir.name))
        self.assertTrue(os.path.exists(work_dir.name))

    def test_keep_false(self) -> None:
        with TemporaryDirectory() as work_dir:
            self.assertTrue(os.path.exists(work_dir.name))
        self.assertFalse(os.path.exists(work_dir.name))

    def test_remove_readonly(self) -> None:
        with TemporaryDirectory() as work_dir:
            filename = os.path.join(work_dir.name, "test.txt")
            with open(filename, "w+") as f:
                f.write("This is intentionally left blank.")
            mode = os.stat(filename)[stat.ST_MODE]
            os.chmod(filename, mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
            self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(work_dir.name))
        self.assertFalse(os.path.exists(filename))

    def test_chdir_true(self) -> None:
        before_dir = os.getcwd()
        with TemporaryDirectory(chdir=True):
            self.assertNotEqual(before_dir, os.getcwd())
        self.assertEqual(before_dir, os.getcwd())

    def test_chdir_false(self) -> None:
        before_dir = os.getcwd()
        with TemporaryDirectory():
            self.assertEqual(before_dir, os.getcwd())
        self.assertEqual(before_dir, os.getcwd())

    def test_path(self) -> None:
        with TemporaryDirectory() as work_dir:
            self.assertIsInstance(work_dir.path, Path)
            self.assertTrue(work_dir.path.exists())
