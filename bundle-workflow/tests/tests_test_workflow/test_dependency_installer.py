import os
import tempfile
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

    def test_install(self):
        with patch(
            "test_workflow.dependency_installer.DependencyInstaller.MavenLocalFileHandler.copy"
        ) as mock_maven_copy:
            self.dependency_installer.maven_local_file_handler = [
                DependencyInstaller.MavenLocalFileHandler(),
                DependencyInstaller.MavenLocalFileHandler(),
            ]
            dependencies = ["job-scheduler", "anomaly-detection"]
            self.dependency_installer.install(dependencies)
            self.assertEqual(mock_maven_copy.call_count, 2)
            maven_local_paths = []
            for dependency in dependencies:
                maven_local_paths.append(os.path.join(
                    os.path.expanduser("~"),
                    f".m2/{self.manifest.build.id}/repository/org/opensearch/{dependency}/{self.manifest.build.version}/",
                ))
            mock_maven_copy.assert_has_calls(
                [
                    call(self.__get_test_dependencies(), maven_local_paths[0]),
                    call(self.__get_test_dependencies(), maven_local_paths[1]),
                ]
            )

    @staticmethod
    def __get_test_dependencies():
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../src/test_workflow"
        )
        return [
            file_name
            for file_name in os.listdir(test_dir)
            if os.path.isfile(os.path.join(test_dir, file_name))
        ]

    class MavenLocalFileHandlerTests(unittest.TestCase):
        def setUp(self):
            self.maven_local_file_handler = DependencyInstaller.MavenLocalFileHandler()

        def test_copy(self):
            with tempfile.TemporaryFile() as maven_local_path:
                test_files = DependencyInstallerTests.__get_test_dependencies()
                self.assertTrue(len(test_files) > 0)
                self.maven_local_file_handler.copy(test_files, maven_local_path)
                self.assertCountEqual(test_files, os.listdir(maven_local_path))
                self.assertListEqual(sorted(test_files), sorted(os.listdir(maven_local_path)))
