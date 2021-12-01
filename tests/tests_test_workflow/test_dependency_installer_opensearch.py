import os
import unittest
from unittest.mock import MagicMock, patch

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch


class DependencyInstallerOpenSearchTests(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "local", "builds", "opensearch", "manifest.yml")
    DIST_MANIFEST_LOCAL = os.path.join(DATA, "local", "dist", "opensearch", "manifest.yml")
    DIST_MANIFEST_REMOTE = os.path.join(DATA, "remote", "dist", "opensearch", "manifest.yml")

    @patch("concurrent.futures.ThreadPoolExecutor", return_value=MagicMock())
    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_maven_dependencies_local(self, mock_request, mock_copyfile, mock_makedirs, mock_threadpool):
        def submit_and_run(callable, source, dest):
            # Filter down the actual calls to make analyzing failures easier
            if 'alerting-notification-1.2.0.0.jar' in source:
                return callable(source, dest)
            return None
        mock_threadpool.return_value.__enter__().submit.side_effect = submit_and_run
        dependency_installer = DependencyInstallerOpenSearch(
            self.DATA,
            BuildManifest.from_path(self.BUILD_MANIFEST),
            BundleManifest.from_path(self.DIST_MANIFEST_LOCAL)
        )
        dependency_installer.install_maven_dependencies()
        self.assertEqual(mock_threadpool.call_count, 4)
        self.assertEqual(mock_threadpool().__enter__().submit.call_count, 2375)

        mock_makedirs.assert_called_with(
            os.path.realpath(
                os.path.join(
                    dependency_installer.maven_local_path, "org", "opensearch", "notification"
                )
            ),
            exist_ok=True
        )
        mock_request.assert_not_called()
        mock_copyfile.assert_called_with(
            os.path.join(self.DATA, "builds", "maven", "org", "opensearch", "notification", "alerting-notification-1.2.0.0.jar"),
            os.path.realpath(os.path.join(dependency_installer.maven_local_path, "org", "opensearch", "notification", "alerting-notification-1.2.0.0.jar"))
        )

    @patch("concurrent.futures.ThreadPoolExecutor", return_value=MagicMock())
    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_maven_dependencies_remote(self, mock_request, mock_copyfile, mock_makedirs, mock_threadpool):
        def submit_and_run(callable, source, dest):
            # Filter down the actual calls to make analyzing failures easier
            if 'alerting-notification-1.2.0.0.jar' in source:
                return callable(source, dest)
            return None
        mock_threadpool.return_value.__enter__().submit.side_effect = submit_and_run
        dependency_installer = DependencyInstallerOpenSearch(
            "https://ci.opensearch.org/x/y",
            BuildManifest.from_path(self.BUILD_MANIFEST),
            BundleManifest.from_path(self.DIST_MANIFEST_REMOTE)
        )
        dependency_installer.install_maven_dependencies()
        self.assertEqual(mock_threadpool.call_count, 4)
        self.assertEqual(mock_threadpool().__enter__().submit.call_count, 2375)
        mock_makedirs.assert_called_with(
            os.path.realpath(
                os.path.join(
                    dependency_installer.maven_local_path, "org", "opensearch", "notification"
                )
            ),
            exist_ok=True
        )
        mock_copyfile.assert_not_called()
        mock_request.assert_called_with(
            "https://ci.opensearch.org/x/y/builds/maven/org/opensearch/notification/alerting-notification-1.2.0.0.jar",
            os.path.realpath(os.path.join(dependency_installer.maven_local_path, "org", "opensearch", "notification", "alerting-notification-1.2.0.0.jar"))
        )

    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_build_dependencies_local(self, mock_request, mock_copyfile, mock_makedirs):
        dependency_installer = DependencyInstallerOpenSearch(
            self.DATA,
            BuildManifest.from_path(self.BUILD_MANIFEST),
            BundleManifest.from_path(self.DIST_MANIFEST_LOCAL)
        )
        dependencies = dict({"opensearch-job-scheduler": "1.1.0.0"})
        dependency_installer.install_build_dependencies(dependencies, os.path.dirname(__file__))
        mock_makedirs.assert_called_with(os.path.dirname(__file__), exist_ok=True)
        mock_request.assert_not_called()
        mock_copyfile.assert_called_once_with(
            os.path.join(self.DATA, "builds", "opensearch", "plugins", "opensearch-job-scheduler-1.1.0.0.zip"),
            os.path.realpath(os.path.join(os.path.dirname(__file__), "opensearch-job-scheduler-1.1.0.0.zip")),
        )

    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_build_dependencies_remote(self, mock_request, mock_copyfile, mock_makedirs):
        dependency_installer = DependencyInstallerOpenSearch(
            "https://ci.opensearch.org/x/y", BuildManifest.from_path(self.BUILD_MANIFEST), BundleManifest.from_path(self.DIST_MANIFEST_REMOTE)
        )
        dependencies = dict({"opensearch-job-scheduler": "1.1.0.0"})
        dependency_installer.install_build_dependencies(dependencies, os.path.dirname(__file__))
        mock_makedirs.assert_called_with(os.path.dirname(__file__), exist_ok=True)
        mock_copyfile.assert_not_called()
        mock_request.assert_called_once_with(
            "https://ci.opensearch.org/x/y/builds/opensearch/plugins/opensearch-job-scheduler-1.1.0.0.zip",
            os.path.realpath(os.path.join(os.path.dirname(__file__), "opensearch-job-scheduler-1.1.0.0.zip")),
        )
