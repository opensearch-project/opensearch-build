# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_suite import PerformanceTestSuite


class TestPerformanceSuite(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        self.manifest = BundleManifest.from_path("data/test_manifest.yaml")
        self.endpoint = None
        self.perf_test_suite = PerformanceTestSuite(
            bundle_manifest=self.manifest, endpoint=None, security=False, current_workspace='current_workspace'
        )

    def test_execute(self):
        with patch('test_workflow.perf_test_suite.os.chdir'):
            with patch("subprocess.check_call") as mock_check_call:
                self.perf_test_suite.execute()
                self.assertEqual(mock_check_call.call_count, 3)
