# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import unittest
from unittest.mock import MagicMock, call, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite


class TestBwcSuite(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        manifest_file_handle = open("data/test_manifest.yaml", "r")
        self.manifest = BundleManifest.from_file(manifest_file_handle)
        self.bwc_test_suite = BwcTestSuite(
            manifest=self.manifest, work_dir=".", component=None, keep=False
        )
        manifest_file_handle.close()

    def test_execute(self):
        expected = []
        for component in self.manifest.components:
            expected.append(call(component))
        self.bwc_test_suite.component_bwc_tests = MagicMock()
        self.bwc_test_suite.execute()
        self.assertEqual(
            self.bwc_test_suite.component_bwc_tests.call_args_list, expected
        )

    def test_run_bwctest(self):
        with self.assertRaises(subprocess.CalledProcessError) as process_ret:
            self.bwc_test_suite.run_tests(".", self.manifest.components[1].name)
        # 1 ret code == could find the script but the script exited because `./gradlew` doesn't exist
        self.assertEqual(process_ret.exception.returncode, 1)
        self.assertTrue("/bwctest.sh" in process_ret.exception.cmd)

    @patch("test_workflow.bwc_test.bwc_test_suite.TestComponent")
    def test_component_bwctest(self, test_component_mock):
        component = self.manifest.components[1]
        self.bwc_test_suite.run_tests = MagicMock()
        expected = [call("./" + self.manifest.components[1].name, self.manifest.components[1].name)]

        self.bwc_test_suite.component_bwc_tests(component)
        test_component_mock.return_value.checkout.assert_called_with(
            "./" + component.name
        )
        self.assertEqual(self.bwc_test_suite.run_tests.call_args_list, expected)
