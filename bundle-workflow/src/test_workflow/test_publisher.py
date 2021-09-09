import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))
from aws.s3_bucket import S3Bucket
from manifests.bundle_manifest import BundleManifest

class TestPublisher:
    def __init__(self, s3_bucket=None, bundle_manifest=None, test_recorder=None):
        self.bundle_manifest = BundleManifest.from_path('/Users/kazabdu/Downloads/manifest.yaml')
        #self.bundle_manifest = bundle_manifest
        self.test_recorder = test_recorder
    
    def publish_test_results_to_s3(self):
        """
            Publishes tests results to S3 pulling information from {self.test_recorder}
            And cleans up all local storage after publishing ({self.test_recorder}.clean_up())
        """
        s3_bucket = S3Bucket('test-publisher-upload', 'arn:aws:iam::821468782434:role/test-publisher', 'test-publisher')
        base_path = self._get_base_path()

        for subdir,dirs,files in os.walk('/Users/kazabdu/1/'):
            for filename in files:
                file_path = subdir + '/' + filename
                if not file_path.startswith('.'):
                    s3_path = base_path + file_path
                    print(s3_path)
                    s3_bucket.upload_file(s3_path, file_path)

    def _get_base_path(self):
        """
            Returns the base path to store logs: /builds/bundles/<bundle-version>/<build-id>/<arch-id>/tests/
        """
        work_dir = 'builds/bundles'
        bundle_version = self.bundle_manifest.build.version
        build_id = self.bundle_manifest.build.id
        arch = self.bundle_manifest.build.architecture
        s3_path = os.path.join(work_dir, bundle_version, build_id, arch, 'tests')
        return s3_path

test_publisher = TestPublisher()
test_publisher.publish_test_results_to_s3()
