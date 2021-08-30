import boto3
import os
from aws.s3_bucket import S3Bucket

class TestPublisher:
    def __init__(self, s3_bucket, bundle_manifest, test_recorder):
        self.s3_bucket = s3_bucket
        self.bundle_manifest = bundle_manifest
        self.test_recorder = test_recorder
    
    def publish_test_results_to_s3(self):
        """
            Publishes tests results to S3 pulling information from {self.test_recorder}
            And cleans up all local storage after publishing ({self.test_recorder}.clean_up())
        """
        s3_bucket = S3Bucket()
        s3_bucket.u
    
    def _get_base_path(self):
        """
            Returns the base path to store logs: /builds/bundles/<bundle-version>/<build-id>/<arch-id>/tests/
        """
        work_dir = '/builds/bundles'
        bundle_version = self.bundle_manifest.bundle_version
        build_id = self.bundle_manifest.build.id
        arch = self.bundle_manifest.build.architecture
        s3_path = os.path.join(work_dir, bundle_version, build_id, arch)
        return s3_path
