# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from system.temporary_directory import TemporaryDirectory


class TestTemporaryDirectory(unittest.TestCase):
    def test_mkdtemp_keep_true(self):
        with TemporaryDirectory.mkdtemp(keep=True) as work_dir:
            self.assertTrue(os.path.exists(work_dir.name))
        self.assertTrue(os.path.exists(work_dir.name))

    def test_mkdtemp_keep_false(self):
        with TemporaryDirectory.mkdtemp() as work_dir:
            self.assertTrue(os.path.exists(work_dir.name))
        self.assertFalse(os.path.exists(work_dir.name))
