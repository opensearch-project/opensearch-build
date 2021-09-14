import os
import unittest
from unittest.mock import patch

from aws.s3_bucket import S3Bucket
from manifests.bundle_manifest import BundleManifest
from test_workflow.test_results import TestResults


class TestTestResults(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "data")
        )
        self.manifest_filename = os.path.join(
            self.data_path, "bundle_manifest.yaml"
        )
        self.manifest = BundleManifest.from_path(self.manifest_filename)
        self.bucket_name = "unitTestBucket"
        self.test_publisher = TestResults(
            bundle_manifest=self.manifest, test_recorder=None
        )

    def test_get_base_path(self):
        s3_path = self.test_publisher._get_base_path()
        self.assertEqual(s3_path, 'builds/bundles/1.0.0/41d5ae25183d4e699e92debfbe3f83bd/x64')

    @patch("boto3.client")
    def test_to_s3(self, mock_boto_client):
        s3bucket = S3Bucket(self.bucket_name)
        self.test_publisher.to_s3(self.bucket_name)
        s3bucket.upload_file(
            "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz",
            "/tmp/opensearch-1.1.0-linux-x64.tar.gz",
        )
        mock_boto_client("s3").upload_file.assert_called_with(
            "/tmp/opensearch-1.1.0-linux-x64.tar.gz",
            self.bucket_name,
            "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz",
        )
