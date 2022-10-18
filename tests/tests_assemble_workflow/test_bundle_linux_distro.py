# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, call, patch

from assemble_workflow.bundle_linux_distro import BundleLinuxDistro
from manifests.build_manifest import BuildManifest


class TestBundleLinuxDistro(unittest.TestCase):

    def setUp(self) -> None:

        self.bundle_linux_distro = BundleLinuxDistro("filename", "package_path", "min_path")

    def test_initialized_values(self) -> None:

        self.assertEqual(self.bundle_linux_distro.filename, "filename")
        self.assertEqual(self.bundle_linux_distro.package_path, "package_path")
        self.assertEqual(self.bundle_linux_distro.min_path, "min_path")

    @patch("assemble_workflow.bundle_linux_distro.BundleLinuxDeb", return_value=MagicMock())
    def test_extract_with_deb_extension(self, bundle_linux_deb_mock: Mock) -> None:

        self.bundle_linux_distro.extract("deb", "dest")

        bundle_linux_deb_mock.assert_has_calls(
            [
                call("filename", "package_path", "min_path")
            ]
        )

        bundle_linux_deb_mock.return_value.extract.assert_has_calls(
            [
                call("dest")
            ]
        )

    @patch("assemble_workflow.bundle_linux_distro.BundleLinuxDeb", return_value=MagicMock())
    def test_build_with_deb_extension(self, bundle_linux_deb_mock: Mock) -> None:

        manifest_deb = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-deb-1.3.0.yml"))
        self.bundle_linux_distro.build("deb", "name", "dest", "archive_path", manifest_deb.build)

        bundle_linux_deb_mock.assert_has_calls(
            [
                call("filename", "package_path", "min_path")
            ]
        )

        bundle_linux_deb_mock.return_value.build.assert_has_calls(
            [
                call("name", "dest", "archive_path", manifest_deb.build)
            ]
        )

    @patch("assemble_workflow.bundle_linux_distro.BundleLinuxRpm", return_value=MagicMock())
    def test_extract_with_rpm_extension(self, bundle_linux_rpm_mock: Mock) -> None:

        self.bundle_linux_distro.extract("rpm", "dest")

        bundle_linux_rpm_mock.assert_has_calls(
            [
                call("filename", "package_path", "min_path")
            ]
        )

        bundle_linux_rpm_mock.return_value.extract.assert_has_calls(
            [
                call("dest")
            ]
        )

    @patch("assemble_workflow.bundle_linux_distro.BundleLinuxRpm", return_value=MagicMock())
    def test_build_with_rpm_extension(self, bundle_linux_rpm_mock: Mock) -> None:

        manifest_rpm = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-rpm-1.3.0.yml"))
        self.bundle_linux_distro.build("rpm", "name", "dest", "archive_path", manifest_rpm.build)

        bundle_linux_rpm_mock.assert_has_calls(
            [
                call("filename", "package_path", "min_path")
            ]
        )

        bundle_linux_rpm_mock.return_value.build.assert_has_calls(
            [
                call("name", "dest", "archive_path", manifest_rpm.build)
            ]
        )
