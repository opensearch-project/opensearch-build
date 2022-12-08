# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, call, patch

from assemble_workflow.dist import DistDeb, DistRpm, DistTar
from manifests.build_manifest import BuildManifest


class TestDist(unittest.TestCase):

    def setUp(self) -> None:

        self.artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts/dist/")
        self.manifest = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-rpm-1.3.0.yml"))
        self.distDeb = DistDeb(
            "OpenSearch",
            self.artifacts_path + "opensearch-min-1.3.0-linux-x64.deb",
            "opensearch-1.3.0",
            self.manifest.build
        )
        self.distRpm = DistRpm(
            "OpenSearch",
            self.artifacts_path + "opensearch-min-1.3.0-linux-x64.rpm",
            "opensearch-1.3.0",
            self.manifest.build
        )
        self.distTar = DistTar(
            "OpenSearch",
            self.artifacts_path + "opensearch-min-1.3.0-linux-x64.tar.gz",
            "opensearch-1.3.0",
            self.manifest.build
        )

    def test_dist_variables(self) -> None:
        self.assertEqual(self.distTar.name, "OpenSearch")
        self.assertEqual(os.path.exists(self.distTar.path), True)
        self.assertEqual(self.distTar.min_path, "opensearch-1.3.0")

    @patch("assemble_workflow.dist.Dist.find_min_archive_path", return_value="opensearch-1.3.0")
    @patch("assemble_workflow.dist.Dist.rename_archive_path", return_value="test_path")
    @patch("assemble_workflow.dist.DistTar.__extract__")
    def test_dist_extract(self, distTar_extract: Mock, dist_rename_path: Mock, dist_find_min_path: Mock) -> None:
        archive_path = self.distTar.extract("test_dest")
        self.assertEqual(archive_path, "test_path")
        dist_find_min_path.assert_called_once()
        dist_rename_path.assert_called_once()
        distTar_extract.assert_called_once()

    @patch("assemble_workflow.dist.DistTar.__build__")
    @patch("shutil.copyfile")
    def test_dist_build(self, shutil_copyfile: Mock, distTar_build: Mock) -> None:
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
    def test_rename_archive_path_rename(self, os_rename: Mock, os_path_dirname: Mock) -> None:
        self.assertEqual(
            self.distTar.rename_archive_path(os.path.join("temp_path", "opensearch-x.y.z")),
            os.path.join("temp_path", "opensearch-1.3.0")
        )

    @patch("assemble_workflow.dist.Dist.find_min_archive_path", return_value="opensearch-1.3.0")
    @patch("assemble_workflow.dist.Dist.rename_archive_path", return_value="test_path")
    @patch("assemble_workflow.dist.BundleLinuxDeb", return_value=MagicMock())
    def test_extract_with_deb_extension(self, bundle_linux_deb_mock: Mock, dist_rename_path: Mock, dist_find_min_path: Mock) -> None:

        self.distDeb.extract("test_dest")

        bundle_linux_deb_mock.assert_has_calls(
            [
                call("opensearch", self.artifacts_path + "opensearch-min-1.3.0-linux-x64.deb", "opensearch-1.3.0")
            ]
        )

        bundle_linux_deb_mock.return_value.extract.assert_has_calls(
            [
                call("test_dest")
            ]
        )

    @patch("shutil.copyfile")
    @patch("assemble_workflow.dist.BundleLinuxDeb", return_value=MagicMock())
    def test_build_with_deb_extension(self, bundle_linux_deb_mock: Mock, shutil_copyfile: Mock) -> None:

        self.distDeb.archive_path = "archive_path"
        self.distDeb.build("opensearch", "test_dest")
        bundle_linux_deb_mock.assert_has_calls(
            [
                call("opensearch", self.artifacts_path + "opensearch-min-1.3.0-linux-x64.deb", "opensearch-1.3.0")
            ]
        )

        bundle_linux_deb_mock.return_value.build.assert_has_calls(
            [
                call("opensearch", "test_dest", "archive_path", self.manifest.build)
            ]
        )

    @patch("assemble_workflow.dist.Dist.find_min_archive_path", return_value="opensearch-1.3.0")
    @patch("assemble_workflow.dist.Dist.rename_archive_path", return_value="test_path")
    @patch("assemble_workflow.dist.BundleLinuxRpm", return_value=MagicMock())
    def test_extract_with_rpm_extension(self, bundle_linux_rpm_mock: Mock, dist_rename_path: Mock, dist_find_min_path: Mock) -> None:

        self.distRpm.extract("test_dest")

        bundle_linux_rpm_mock.assert_has_calls(
            [
                call("opensearch", self.artifacts_path + "opensearch-min-1.3.0-linux-x64.rpm", "opensearch-1.3.0")
            ]
        )

        bundle_linux_rpm_mock.return_value.extract.assert_has_calls(
            [
                call("test_dest")
            ]
        )

    @patch("shutil.copyfile")
    @patch("assemble_workflow.dist.BundleLinuxRpm", return_value=MagicMock())
    def test_build_with_rpm_extension(self, bundle_linux_rpm_mock: Mock, shutil_copyfile: Mock) -> None:

        self.distRpm.archive_path = "archive_path"
        self.distRpm.build("opensearch", "test_dest")
        bundle_linux_rpm_mock.assert_has_calls(
            [
                call("opensearch", self.artifacts_path + "opensearch-min-1.3.0-linux-x64.rpm", "opensearch-1.3.0")
            ]
        )

        bundle_linux_rpm_mock.return_value.build.assert_has_calls(
            [
                call("opensearch", "test_dest", "archive_path", self.manifest.build)
            ]
        )
