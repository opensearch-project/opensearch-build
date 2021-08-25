import os
import shutil
import unittest

from src.test_workflow.dependency_installer import DependencyInstaller


class DependencyInstallerTests(unittest.TestCase):
    dependency_installer = DependencyInstaller("7", "job-scheduler", "1.1.0.0", "arm64")

    def test_get_dependency_path(self):
        self.assertEqual(
            "org/opensearch/job-scheduler/1.1.0.0/",
            self.dependency_installer.get_dependency_path(),
        )

    def test_copy_to_maven_local(self):
        dependency_from_s3 = self.get_test_dependencies()
        maven_local_path = self.dependency_installer.get_maven_local_path()
        if not os.path.exists(maven_local_path):
            os.makedirs(maven_local_path)
        else:
            self.clean_maven_local_path(maven_local_path)
        self.dependency_installer.copy_to_maven_local(
            dependency_from_s3, maven_local_path
        )
        self.assertCountEqual(dependency_from_s3, os.listdir(maven_local_path))
        self.assertListEqual(dependency_from_s3, os.listdir(maven_local_path))

    def test_install(self):
        maven_local_path = self.dependency_installer.get_maven_local_path()
        self.clean_maven_local_path(maven_local_path)
        self.dependency_installer.install()
        self.assertCountEqual(
            self.get_test_dependencies(), os.listdir(maven_local_path)
        )
        self.assertListEqual(self.get_test_dependencies(), os.listdir(maven_local_path))

    def get_test_dependencies(self):
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../src/test_workflow"
        )
        return [
            file_name
            for file_name in os.listdir(test_dir)
            if os.path.isfile(os.path.join(test_dir, file_name))
        ]

    def clean_maven_local_path(self, maven_local_path):
        for file_name in os.listdir(maven_local_path):
            local_file_path = os.path.join(maven_local_path, file_name)
            try:
                if os.path.isfile(local_file_path) or os.path.islink(local_file_path):
                    os.unlink(local_file_path)
                elif os.path.isdir(local_file_path):
                    shutil.rmtree(local_file_path)
            except OSError as e:
                print(f"Failed to clean {local_file_path}. Reason: {e}")
                raise
