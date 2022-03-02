# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from assemble_workflow.dist import DistTar


class TestDist(unittest.TestCase):

    def setUp(self) -> None:

        self.artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts/dist/")
        self.distTar = DistTar(
            "OpenSearch",
            self.artifacts_path + "opensearch-min-1.3.0-linux-x64.tar.gz",
            "opensearch-1.3.0"
        )

    def test_dist_variables(self) -> None:
        self.assertEqual(self.distTar.name, "OpenSearch")
        self.assertEqual(os.path.exists(self.distTar.path), True)
        self.assertEqual(self.distTar.min_path, "opensearch-1.3.0")

    @patch("assemble_workflow.dist.Dist.find_min_archive_path", return_value="opensearch-1.3.0")
    @patch("assemble_workflow.dist.Dist.rename_archive_path", return_value="test_path")
    @patch("assemble_workflow.dist.DistTar.__extract__")
    def test_dist_extract(self, dist_find_min_path: Mock, dist_rename_path: Mock, distTar_extract: Mock) -> None:
        archive_path = self.distTar.extract("test_dest")
        self.assertEqual(archive_path, "test_path")
        dist_find_min_path.assert_called_once()
        dist_rename_path.assert_called_once()
        distTar_extract.assert_called_once()

    @patch("assemble_workflow.dist.DistTar.__build__")
    @patch("shutil.copyfile")
    def test_dist_build(self, distTar_build: Mock, shutil_copyfile: Mock) -> None:
        self.distTar.build("temp_name", "temp_dest")
        distTar_build.assert_called_once()
        shutil_copyfile.assert_called_once()

    def test_find_min_archive_path(self) -> None:
        self.assertEqual(
            self.distTar.find_min_archive_path(self.artifacts_path),
            self.artifacts_path + "opensearch-1.3.0"
        )

    @patch("os.path.basename", return_value="opensearch-1.3.0")
    def test_rename_archive_path_norename(self, os_path_basename: Mock) -> None:
        self.assertEqual(
            self.distTar.rename_archive_path(os.path.join("temp_path", "opensearch-1.3.0")),
            os.path.join("temp_path", "opensearch-1.3.0")
        )

    @patch("os.path.dirname", return_value="temp_path")
    @patch("os.rename")
    def test_rename_archive_path_rename(self, os_path_dirname: Mock, os_rename: Mock) -> None:
        self.assertEqual(
            self.distTar.rename_archive_path(os.path.join("temp_path", "opensearch-x.y.z")),
            os.path.join("temp_path", "opensearch-1.3.0")
        )
