# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from assemble_workflow.bundle_deb import BundleDeb
from manifests.build_manifest import BuildManifest


class TestBundleDeb(unittest.TestCase):

    def setUp(self) -> None:

        self.package_name = 'opensearch-1.3.0-1.x86_64.deb'
        self.artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts/dist")
        self.package_path = os.path.join(self.artifacts_path, self.package_name)

        self.bundle_deb = BundleDeb('opensearch', self.package_path, 'opensearch-1.3.0')
        self.manifest_deb = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-deb-1.3.0.yml"))

        self.bundle_deb_qualifier = BundleDeb('opensearch', self.package_path, 'opensearch-2.0.0-alpha1')
        self.manifest_deb_qualifier = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-deb-2.0.0-alpha1.yml"))

    @patch("builtins.open")
    @patch("shutil.move")
    @patch("shutil.copy2")
    @patch("subprocess.check_call")
    def test_extract_deb(self, check_call_mock: Mock, shutil_copy2_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock) -> None:

        self.bundle_deb.extract(self.artifacts_path)
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 2)
        self.assertEqual(['deb2cpio', self.package_path], args_list[0][0][0])
        self.assertEqual(['cpio', '-imdv'], args_list[1][0][0])
        self.assertEqual(shutil_copy2_mock.call_count, 0)
        self.assertEqual(shutil_move_mock.call_count, 1)
        self.assertEqual(os.environ['OPENSEARCH_PATH_CONF'], os.path.join(self.artifacts_path, 'etc', 'opensearch'))

    @patch("os.path.exists", return_value=True)
    @patch("os.walk")
    @patch("builtins.open")
    @patch("shutil.move")
    @patch("subprocess.check_call")
    def test_build_deb(self, check_call_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock, os_walk_mock: Mock, os_path_exists: Mock) -> None:

        self.bundle_deb.build(self.package_path, self.artifacts_path, os.path.join(self.artifacts_path, 'opensearch-1.3.0'), self.manifest_deb.build)
        args_list_deb = check_call_mock.call_args_list

        self.assertRaises(KeyError, lambda: os.environ['OPENSEARCH_PATH_CONF'])
        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"dpkg-buildpackage -bb --define '_topdir {self.artifacts_path}' --define '_version 1.3.0' --define '_architecture x86_64' opensearch.deb.spec", args_list_deb[0][0][0])
        self.assertEqual(shutil_move_mock.call_count, 2)

    @patch("os.path.exists", return_value=True)
    @patch("os.walk")
    @patch("builtins.open")
    @patch("shutil.move")
    @patch("subprocess.check_call")
    def test_build_deb_qualifier(self, check_call_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock, os_walk_mock: Mock, os_path_exists: Mock) -> None:

        self.bundle_deb_qualifier.build(self.package_path, self.artifacts_path, os.path.join(self.artifacts_path, 'opensearch-2.0.0-alpha1'), self.manifest_deb_qualifier.build)
        args_list_deb_qualifier = check_call_mock.call_args_list

        self.assertRaises(KeyError, lambda: os.environ['OPENSEARCH_PATH_CONF'])
        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual(f"dpkg-buildpackage -bb --define '_topdir {self.artifacts_path}' --define '_version 2.0.0.alpha1' --define '_architecture x86_64' opensearch.deb.spec",
                         args_list_deb_qualifier[0][0][0])
        self.assertEqual(shutil_move_mock.call_count, 2)
