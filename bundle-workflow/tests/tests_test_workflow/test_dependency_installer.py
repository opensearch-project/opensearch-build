import os
import shutil
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

    @patch("test_workflow.dependency_installer.S3Bucket")
    def test_install_maven_dependencies(self, mock_s3_bucket):
        s3_bucket = mock_s3_bucket.return_value
        self.dependency_installer = DependencyInstaller(self.manifest.build)
        dependencies = dict(
            {
                "opensearch-job-scheduler": "1.1.0.0",
                "opensearch-anomaly-detection": "1.1.0.0",
            }
        )
        self.dependency_installer.install_maven_dependencies(dependencies)
        self.assertEqual(s3_bucket.download_folder.call_count, 2)
        maven_local_paths = []
        for dependency, version in dependencies.items():
            maven_local_paths.append(
                os.path.join(
                    os.path.expanduser("~"),
                    f".m2/repository/org/opensearch/{dependency}/{version}/",
                )
            )
        s3_bucket.download_folder.assert_has_calls(
            [
                call(
                    "opensearch-job-scheduler/1.1.0.0",
                    maven_local_paths[0],
                ),
                call(
                    "opensearch-anomaly-detection/1.1.0.0",
                    maven_local_paths[1],
                ),
            ]
        )

    @patch("test_workflow.dependency_installer.S3Bucket")
    def test_install_build_dependencies(self, mock_s3_bucket):
        s3_bucket = mock_s3_bucket.return_value
        self.dependency_installer = DependencyInstaller(self.manifest.build)
        dependencies = dict({"opensearch-job-scheduler": "1.1.0.0"})
        self.dependency_installer.install_build_dependencies(
            dependencies, os.path.dirname(__file__)
        )
        self.assertEqual(s3_bucket.download_file.call_count, 1)
        s3_bucket.download_file.assert_has_calls(
            [
                call(
                    "opensearch-job-scheduler-1.1.0.0.zip",
                    os.path.dirname(__file__),
                )
            ]
        )

    def test_cleanup_for_dir(self):
        self.dependency_installer = DependencyInstaller(self.manifest.build)
        dest_path = self.__get_test_dir()
        os.makedirs(dest_path)
        shutil.copy(self.manifest_filename, dest_path)
        self.assertEqual(len(os.listdir(dest_path)), 1)
        self.dependency_installer.cleanup(dest_path)
        self.assertFalse(os.path.exists(dest_path))

    def test_cleanup_for_file(self):
        self.dependency_installer = DependencyInstaller(self.manifest.build)
        dest_dir = self.__get_test_dir()
        dest_path = os.path.join(dest_dir, "opensearch-build-1.1.0.yml")
        os.makedirs(dest_dir)
        shutil.copy(self.manifest_filename, dest_path)
        self.assertEqual(len(os.listdir(dest_dir)), 1)
        self.dependency_installer.cleanup(dest_path)
        self.assertFalse(os.path.exists(dest_path))
        self.assertTrue(os.path.exists(dest_dir))
        shutil.rmtree(dest_dir)
        self.assertFalse(os.path.exists(dest_dir))

    def __get_test_dir(self):
        return os.path.join(os.path.dirname(__file__), "test-temp")
