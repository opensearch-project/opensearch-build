import unittest
import os

from unittest.mock import patch
from run_integ_test import BuildManifest, BundleManifest, main


class TestRunIntegTest(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        self.bundle_manifest = BundleManifest.from_path("data/bundle_manifest.yml")
        self.build_manifest = BuildManifest.from_path("data/build_manifest.yml")

    @staticmethod
    def mock_args(mock_test_args):
        mock_test_args.s3_bucket = 's3bucket'
        mock_test_args.architecture = 'x64'
        mock_test_args.opensearch_version = '1.1.0'
        mock_test_args.build_id = 100
        mock_test_args.test_run_id = 1
        mock_test_args.keep = False
        mock_test_args.logging_level = 'INFO'

    @patch("run_integ_test.console")
    @patch("run_integ_test.GitRepository")
    @patch("run_integ_test.DependencyInstaller")
    @patch("os.chdir")
    @patch.object(BundleManifest, "from_s3")
    @patch.object(BuildManifest, "from_s3")
    @patch("run_integ_test.TestArgs")
    @patch("run_integ_test.IntegTestSuite")
    def test_run_integ_test(self, mock_integ_test_suite, mock_test_args, mock_bundle_from_s3, mock_build_from_s3, mock_os_chdir, *mock):
        """
        test_manifest.yml has 8 plugin components listed for integration tests. This test ensures all get executed
        as part of integration test job.
        """
        self.mock_args(mock_test_args)
        mock_bundle_from_s3.return_value = self.bundle_manifest
        mock_build_from_s3.return_value = self.build_manifest
        mock_integ_test_suite.return_value.execute.return_value = 0, True
        main()
        self.assertEqual(mock_bundle_from_s3.call_count, 1)
        self.assertEqual(mock_integ_test_suite.return_value.execute.call_count, 8)


if __name__ == '__main__':
    unittest.main()
