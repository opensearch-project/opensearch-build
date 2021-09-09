import os
import unittest
from unittest.mock import call, patch

from manifests.build_manifest import BuildManifest
from test_workflow.dependency_installer import DependencyInstaller


class DependencyInstallerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.manifest_filename = os.path.join(
            os.path.dirname(__file__),
            "../tests_assemble_workflow/data/opensearch-build-1.1.0.yml",
        )
        self.manifest = BuildManifest.from_path(self.manifest_filename)
        self.dependency_installer = DependencyInstaller(self.manifest.build)

    @patch("test_workflow.dependency_installer.S3Bucket")
    def test_install_maven_dependencies(self, mock_s3_bucket):
        s3_bucket = mock_s3_bucket.return_value
        dependencies = dict(
            {
                "opensearch-job-scheduler": "1.1.0.0",
                "opensearch-anomaly-detection": "1.1.0.0",
            }
        )
        self.dependency_installer.install_maven_dependencies(dependencies)
        self.assertEqual(s3_bucket.download_folder.call_count, 2)
        s3_bucket.download_folder.assert_has_calls(
            [
                call(
                    f"{self.dependency_installer.s3_maven_location}/opensearch-job-scheduler/1.1.0.0",
                    self.dependency_installer.maven_local_path("opensearch-job-scheduler", "1.1.0.0"),
                ),
                call(
                    f"{self.dependency_installer.s3_maven_location}/opensearch-anomaly-detection/1.1.0.0",
                    self.dependency_installer.maven_local_path("opensearch-anomaly-detection", "1.1.0.0"),
                ),
            ]
        )

    @patch("test_workflow.dependency_installer.S3Bucket")
    def test_install_build_dependencies(self, mock_s3_bucket):
        s3_bucket = mock_s3_bucket.return_value
        dependencies = dict({"opensearch-job-scheduler": "1.1.0.0"})
        self.dependency_installer.install_build_dependencies(
            dependencies, os.path.dirname(__file__)
        )
        self.assertEqual(s3_bucket.download_file.call_count, 1)
        s3_bucket.download_file.assert_has_calls(
            [
                call(
                    f"{self.dependency_installer.s3_build_location}/opensearch-job-scheduler-1.1.0.0.zip",
                    os.path.dirname(__file__),
                )
            ]
        )
