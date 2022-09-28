# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from assemble_workflow.bundle_rpm import BundleRpm
from manifests.build_manifest import BuildManifest


class TestBundleRpm(unittest.TestCase):

    def setUp(self) -> None:

        self.package_name = 'opensearch-1.3.0-1.x86_64.rpm'
        self.artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts/dist")
        self.package_path = os.path.join(self.artifacts_path, self.package_name)

        self.bundle_rpm = BundleRpm('opensearch', self.package_path, 'opensearch-1.3.0')
        self.manifest_rpm = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-rpm-1.3.0.yml"))

        self.bundle_rpm_qualifier = BundleRpm('opensearch', self.package_path, 'opensearch-2.0.0-alpha1')
        self.manifest_rpm_qualifier = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-rpm-2.0.0-alpha1.yml"))

    @patch("builtins.open")
    @patch("shutil.move")
    @patch("shutil.copy2")
    @patch("subprocess.check_call")
    def test_extract_rpm(self, check_call_mock: Mock, shutil_copy2_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock) -> None:

        self.bundle_rpm.extract(self.artifacts_path)
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 2)
        self.assertEqual(['rpm2cpio', self.package_path], args_list[0][0][0])
        self.assertEqual(['cpio', '-imdv'], args_list[1][0][0])
        self.assertEqual(shutil_copy2_mock.call_count, 0)
        self.assertEqual(shutil_move_mock.call_count, 1)
        self.assertEqual(os.environ['OPENSEARCH_PATH_CONF'], os.path.join(self.artifacts_path, 'etc', 'opensearch'))

    @patch("os.path.exists", return_value=True)
    @patch("os.walk")
    @patch("builtins.open")
    @patch("shutil.move")
    @patch("subprocess.check_call")
    def test_build_rpm(self, check_call_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock, os_walk_mock: Mock, os_path_exists: Mock) -> None:

        self.bundle_rpm.build(self.package_path, self.artifacts_path, os.path.join(self.artifacts_path, 'opensearch-1.3.0'), self.manifest_rpm.build)
        args_list_rpm = check_call_mock.call_args_list

        self.assertRaises(KeyError, lambda: os.environ['OPENSEARCH_PATH_CONF'])
        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"rpmbuild -bb --define '_topdir {self.artifacts_path}' --define '_version 1.3.0' --define '_architecture x86_64' opensearch.rpm.spec", args_list_rpm[0][0][0])
        self.assertEqual(shutil_move_mock.call_count, 2)

    @patch("os.path.exists", return_value=True)
    @patch("os.walk")
    @patch("builtins.open")
    @patch("shutil.move")
    @patch("subprocess.check_call")
    def test_build_rpm_qualifier(self, check_call_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock, os_walk_mock: Mock, os_path_exists: Mock) -> None:

        self.bundle_rpm_qualifier.build(self.package_path, self.artifacts_path, os.path.join(self.artifacts_path, 'opensearch-2.0.0-alpha1'), self.manifest_rpm_qualifier.build)
        args_list_rpm_qualifier = check_call_mock.call_args_list

        self.assertRaises(KeyError, lambda: os.environ['OPENSEARCH_PATH_CONF'])
        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"rpmbuild -bb --define '_topdir {self.artifacts_path}' --define '_version 2.0.0.alpha1' --define '_architecture x86_64' opensearch.rpm.spec",
                         args_list_rpm_qualifier[0][0][0])
        self.assertEqual(shutil_move_mock.call_count, 2)
