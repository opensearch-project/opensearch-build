# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, call, mock_open, patch

from assemble_workflow.bundle_linux_deb import BundleLinuxDeb
from manifests.build_manifest import BuildManifest


class TestBundleLinuxDeb(unittest.TestCase):

    def setUp(self) -> None:

        self.package_name = 'opensearch-1.3.0.x86_64.deb'
        self.artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts/dist")
        self.package_path = os.path.join(self.artifacts_path, self.package_name)

        self.bundle_linux_deb = BundleLinuxDeb('opensearch', self.package_path, 'opensearch-1.3.0')
        self.manifest_deb = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-deb-1.3.0.yml"))

        self.bundle_linux_deb_qualifier = BundleLinuxDeb('opensearch', self.package_path, 'opensearch-2.0.0-alpha1')
        self.manifest_deb_qualifier = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-deb-2.0.0-alpha1.yml"))

    @patch("builtins.open")
    @patch("shutil.move")
    @patch("shutil.copy2")
    @patch("subprocess.check_call")
    def test_extract_deb(self, check_call_mock: Mock, shutil_copy2_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock) -> None:

        self.bundle_linux_deb.extract(self.artifacts_path)
        args_list = check_call_mock.call_args_list

        self.assertEqual(check_call_mock.call_count, 2)
        self.assertEqual(['ar', '-xf', self.package_path, 'data.tar.gz'], args_list[0][0][0])
        self.assertEqual(['tar', '-zvxf', '-'], args_list[1][0][0])
        self.assertEqual(shutil_copy2_mock.call_count, 0)
        self.assertEqual(shutil_move_mock.call_count, 1)
        self.assertEqual(os.environ['OPENSEARCH_PATH_CONF'], os.path.join(self.artifacts_path, 'etc', 'opensearch'))

    @patch("os.path.exists", return_value=True)
    @patch("os.walk")
    @patch("builtins.open")
    @patch("shutil.move")
    @patch("subprocess.check_call")
    @patch("assemble_workflow.bundle_linux_deb.BundleLinuxDeb.generate_changelog_file")
    def test_build_deb(self, generate_changelog_file_call_mock: Mock, check_call_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock, os_walk_mock: Mock, os_path_exists: Mock) -> None:

        self.bundle_linux_deb.build(self.package_path, self.artifacts_path, os.path.join(self.artifacts_path, 'opensearch-1.3.0'), self.manifest_deb.build)
        args_list_deb = check_call_mock.call_args_list

        self.assertRaises(KeyError, lambda: os.environ['OPENSEARCH_PATH_CONF'])
        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual('debmake -f "OpenSearch Team" -e "opensearch@amazon.com" -i debuild -p opensearch -n -r 1 -u 1.3.0', args_list_deb[0][0][0])
        self.assertEqual(shutil_move_mock.call_count, 2)
        self.assertEqual(generate_changelog_file_call_mock.call_count, 1)

    @patch("os.path.exists", return_value=True)
    @patch("os.walk")
    @patch("builtins.open")
    @patch("shutil.move")
    @patch("subprocess.check_call")
    @patch("assemble_workflow.bundle_linux_deb.BundleLinuxDeb.generate_changelog_file")
    def test_build_deb_qualifier(self, generate_changelog_file_call_mock: Mock, check_call_mock: Mock, shutil_move_mock: Mock, builtins_open: Mock, os_walk_mock: Mock, os_path_exists: Mock) -> None:

        self.bundle_linux_deb_qualifier.build(self.package_path, self.artifacts_path, os.path.join(self.artifacts_path, 'opensearch-2.0.0-alpha1'), self.manifest_deb_qualifier.build)
        args_list_deb_qualifier = check_call_mock.call_args_list

        self.assertRaises(KeyError, lambda: os.environ['OPENSEARCH_PATH_CONF'])
        self.assertEqual(check_call_mock.call_count, 1)
        self.assertEqual('debmake -f "OpenSearch Team" -e "opensearch@amazon.com" -i debuild -p opensearch -n -r 1 -u 2.0.0.alpha1',
                         args_list_deb_qualifier[0][0][0])
        self.assertEqual(shutil_move_mock.call_count, 2)
        self.assertEqual(generate_changelog_file_call_mock.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_changelog_file(self, file_mock: Mock) -> None:

        self.bundle_linux_deb.generate_changelog_file("dest", "2.3.4")

        self.assertEqual(file_mock.call_count, 1)
        self.assertEqual(os.path.join('dest', 'debian', 'changelog'),
                         file_mock.call_args_list[0][0][0])

        file_mock.return_value.write.assert_has_calls(
            [
                call('opensearch (2.3.4) UNRELEASED; urgency=low\n'),
                call('\n'),
                call('  * Initial release.\n'),
                call('\n'),
                call(' -- OpenSearch Team <opensearch@amazon.com>  Fri, 14 Oct 2022 10:06:23 +0000\n')
            ]
        )
