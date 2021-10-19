# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from contextlib import contextmanager
from unittest.mock import patch

from run_integ_test import BuildManifest, BundleManifest, main


class TestRunIntegTest(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        self.bundle_manifest = BundleManifest.from_path("data/bundle_manifest.yml")
        self.build_manifest = BuildManifest.from_path("data/build_manifest.yml")

    @contextmanager
    def __mock_args(self):
        with patch("run_integ_test.TestArgs") as mock_test_args:
            mock_test_args.s3_bucket = "s3bucket"
            mock_test_args.platform = "linux"
            mock_test_args.architecture = "x64"
            mock_test_args.opensearch_version = "1.1.0"
            mock_test_args.build_id = 100
            mock_test_args.test_run_id = 1
            mock_test_args.keep = False
            mock_test_args.logging_level = "INFO"
            yield mock_test_args

    @patch("run_integ_test.console")
    @patch("run_integ_test.GitRepository")
    @patch("run_integ_test.DependencyInstaller")
    @patch("os.chdir")
    @patch("os.makedirs")
    @patch("run_integ_test.TestSuiteResults")
    @patch.object(BundleManifest, "from_s3")
    @patch.object(BuildManifest, "from_s3")
    @patch("run_integ_test.IntegTestSuite")
    def test_run_integ_test(self, mock_integ_test_suite, mock_build_from_s3, mock_bundle_from_s3, mock_results, *mock):
        """
        test_manifest.yml has 8 plugin components listed for integration tests. This test ensures all get executed
        as part of integration test job.
        """
        mock_bundle_from_s3.return_value = self.bundle_manifest
        mock_build_from_s3.return_value = self.build_manifest
        mock_integ_test_suite.return_value.execute.return_value = 0, True
        mock_results.return_value.failed.return_value = False
        with self.__mock_args():
            main()
        self.assertEqual(mock_bundle_from_s3.call_count, 1)
        self.assertEqual(mock_integ_test_suite.return_value.execute.call_count, 8)
        self.assertEqual(mock_results.return_value.log.call_count, 1)

    @patch("run_integ_test.console")
    @patch("run_integ_test.GitRepository")
    @patch("run_integ_test.DependencyInstaller")
    @patch("os.chdir")
    @patch("run_integ_test.TestSuiteResults")
    @patch.object(BundleManifest, "from_s3")
    @patch.object(BuildManifest, "from_s3")
    @patch("run_integ_test.IntegTestSuite")
    def test_run_integ_test_failure(self, mock_integ_test_suite, mock_build_from_s3, mock_bundle_from_s3, mock_results, *mock):
        """
        test_manifest.yml has 8 plugin components listed for integration tests. This test ensures all get executed
        as part of integration test job.
        """
        mock_bundle_from_s3.return_value = self.bundle_manifest
        mock_build_from_s3.return_value = self.build_manifest
        mock_integ_test_suite.return_value.execute.return_value = 0, True
        mock_results.return_value.failed.return_value = True
        with self.__mock_args() and self.assertRaises(SystemExit):
            main()
            self.assertEqual(mock_bundle_from_s3.call_count, 1)
            self.assertEqual(mock_integ_test_suite.return_value.execute.call_count, 8)
            self.assertEqual(mock_results.return_value.log.call_count, 1)
