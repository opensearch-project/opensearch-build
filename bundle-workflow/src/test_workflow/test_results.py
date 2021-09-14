import os

from aws.s3_bucket import S3Bucket


class TestResults:
    def __init__(self, bundle_manifest, test_recorder):
        self.bundle_manifest = bundle_manifest
        self.test_recorder = test_recorder

    def to_s3(self, bucket):
        """
            Publishes tests results to S3 pulling information from {self.test_recorder}
            And cleans up all local storage after publishing ({self.test_recorder}.clean_up())
        """
        s3_bucket = S3Bucket(bucket, '<role-arn>', 'test-publisher-session')
        base_path = self._get_base_path()

        for subdir, dirs, files in os.walk(self.test_recorder.location):
            test_path = subdir[subdir.find('tests'):]
            for file_name in files:
                file_path = os.path.join(subdir, file_name)
                if not file_path.startswith('.'):
                    s3_path = os.path.join(base_path, test_path, file_name)
                    s3_bucket.upload_file(s3_path, file_path)

    def _get_base_path(self):
        """
            Returns the base path to store logs: /builds/bundles/<bundle-version>/<build-id>/<arch-id>/tests/
        """
        work_dir = 'builds/bundles'
        bundle_version = self.bundle_manifest.build.version
        build_id = self.bundle_manifest.build.id
        arch = self.bundle_manifest.build.architecture
        s3_path = os.path.join(work_dir, bundle_version, build_id, arch)
        return s3_path
