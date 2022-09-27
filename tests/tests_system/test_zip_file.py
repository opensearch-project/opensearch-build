# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
import zipfile

from system.temporary_directory import TemporaryDirectory
from system.zip_file import ZipFile


class TestZipFile(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path = os.path.join(os.path.dirname(__file__), "data")

    def test_extractall_preserves_permissions(self) -> None:
        with TemporaryDirectory() as tmp:
            temp_file = os.path.join(tmp.name, "test.zip")
            with ZipFile(temp_file, "w", zipfile.ZIP_DEFLATED) as zip:
                zip.write(os.path.join(self.data_path, "executable.sh"), "executable.sh")
                zip.write(__file__, "regular.py")

            with ZipFile(temp_file, "r") as zip:
                zip.extractall(tmp.name)

            executable_file = os.path.join(tmp.name, "executable.sh")
            self.assertTrue(os.path.exists(executable_file))
            self.assertTrue(os.access(executable_file, os.X_OK))

            regular_file = os.path.join(tmp.name, "regular.py")
            self.assertTrue(os.path.exists(regular_file))
