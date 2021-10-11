# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import patch

from run_bwc_test import BundleManifest, main


class TestRunBwcTest(unittest.TestCase):
    def setUp(self):
        self.bundle_manifest = BundleManifest.from_path("data/bundle_manifest.yml")

    @staticmethod
    def mock_args(mock_test_args):
        mock_test_args.s3_bucket = 's3bucket'
        mock_test_args.architecture = 'x64'
        mock_test_args.opensearch_version = '1.1.0'
        mock_test_args.build_id = 100
        mock_test_args.test_run_id = 1
        mock_test_args.keep = False
        mock_test_args.logging_level = 'INFO'

    @patch("run_bwc_test.console")
    @patch.object(BundleManifest, "from_s3")
    @patch("run_bwc_test.TestArgs")
    @patch("run_bwc_test.BwcTestSuite")
    def test_run_bwc_test(self, mock_bwc_suite, mock_test_args, *mock):
        self.mock_args(mock_test_args)
        main()
        self.assertEqual(mock_bwc_suite.return_value.execute.call_count, 1)
