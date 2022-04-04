# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_test_suite import PerfTestSuite


class TestPerfTestSuite(unittest.TestCase):
    def setUp(self):
        self.args = Mock()
        self.args.workload = "nyc_taxis"
        self.args.workload_options = "{}"
        self.args.warmup_iters = 0
        self.args.test_iters = 1
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "bundle_manifest.yml")
        self.manifest = BundleManifest.from_path(self.manifest_filename)
        self.endpoint = None

        self.perf_test_suite = PerfTestSuite(bundle_manifest=self.manifest, endpoint=None, security=False,
                                             current_workspace="current_workspace", test_results_path="test/results/",
                                             args=self.args)

    def test_execute(self):
        with patch("test_workflow.perf_test.perf_test_suite.os.chdir"):
            with patch("subprocess.check_call") as mock_check_call:
                self.perf_test_suite.execute()
                self.assertEqual(mock_check_call.call_count, 2)
