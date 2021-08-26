import os
import tempfile
import unittest
from unittest.mock import patch

from helper.test_utils import TestUtils

from test_workflow.dependency_installer import DependencyInstaller


class DependencyInstallerTests(unittest.TestCase):
    def setUp(self):
        self.dependency_installer = DependencyInstaller(
            "7", "job-scheduler", "1.1.0.0", "arm64"
        )

    def test_dependency_path(self):
        self.assertEqual(
            "org/opensearch/job-scheduler/1.1.0.0/",
            self.dependency_installer.dependency_path,
        )

    def test_install(self):
        maven_local_path = self.dependency_installer.maven_local_path
        with patch(
            "test_workflow.dependency_installer.DependencyInstaller.MavenLocalFileHandler.copy"
        ) as mock_maven_copy:
            self.dependency_installer.maven_local_file_handler = [
                DependencyInstaller.MavenLocalFileHandler(),
                DependencyInstaller.MavenLocalFileHandler(),
            ]
            self.dependency_installer.install()
            mock_maven_copy.assert_called_with(
                TestUtils.get_test_dependencies(), maven_local_path
            )


class MavenLocalFileHandlerTests(unittest.TestCase):
    def setUp(self):
        self.maven_local_file_handler = DependencyInstaller.MavenLocalFileHandler()

    def test_copy(self):
        maven_local_path = tempfile.mkdtemp()
        test_files = TestUtils.get_test_dependencies()
        self.maven_local_file_handler.copy(test_files, maven_local_path)
        self.assertCountEqual(test_files, os.listdir(maven_local_path))
        self.assertListEqual(test_files, os.listdir(maven_local_path))
