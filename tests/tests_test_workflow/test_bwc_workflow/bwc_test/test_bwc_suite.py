# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from manifests.bundle_manifest import BundleManifest
from paths.script_finder import ScriptFinder
from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite


class TestBwcSuite(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    MANIFEST = os.path.join(DATA, "remote", "dist", "opensearch", "manifest.yml")

    def setUp(self):
        os.chdir(os.path.dirname(__file__))

        self.manifest = BundleManifest.from_path(self.MANIFEST)
        self.bwc_test_suite = BwcTestSuite(manifest=self.manifest, work_dir=".", component=None, keep=False)

    def test_execute(self):
        expected = []
        for component in self.manifest.components.values():
            expected.append(call(component))
        self.bwc_test_suite.component_bwc_tests = MagicMock()
        self.bwc_test_suite.execute()
        self.assertEqual(self.bwc_test_suite.component_bwc_tests.call_args_list, expected)

    @patch("test_workflow.bwc_test.bwc_test_suite.execute")
    def test_run_bwctest(self, mock_execute):
        mock_execute.return_value = (0, "", "")
        self.bwc_test_suite.run_tests(".", "job-scheduler")
        script = os.path.join(ScriptFinder.default_scripts_path, "bwctest.sh")
        mock_execute.assert_called_with(script, ".", True, False)

    @patch("test_workflow.bwc_test.bwc_test_suite.TestComponent")
    def test_component_bwctest(self, test_component_mock):
        component = self.manifest.components["job-scheduler"]
        self.bwc_test_suite.run_tests = MagicMock()
        expected = [call(os.path.join(".", component.name), component.name)]

        self.bwc_test_suite.component_bwc_tests(component)
        test_component_mock.return_value.checkout.assert_called_with(os.path.join(".", component.name))
        self.assertEqual(self.bwc_test_suite.run_tests.call_args_list, expected)
