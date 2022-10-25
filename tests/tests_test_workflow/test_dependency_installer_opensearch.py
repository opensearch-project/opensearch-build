# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from unittest.mock import Mock, call, patch
from urllib.error import HTTPError

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from system.thread_safe_counter import ThreadSafeCounter
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch


class DependencyInstallerOpenSearchTests(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "local", "builds", "opensearch", "manifest.yml")
    DIST_MANIFEST_LOCAL = os.path.join(DATA, "local", "dist", "opensearch", "manifest.yml")
    DIST_MANIFEST_REMOTE = os.path.join(DATA, "remote", "dist", "opensearch", "manifest.yml")

    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_maven_dependencies_local(self, mock_request: Mock, mock_copyfile: Mock, mock_makedirs: Mock) -> None:
        counter = ThreadSafeCounter()
        mock_copyfile.side_effect = counter.thread_safe_count

        dependency_installer = DependencyInstallerOpenSearch(
            self.DATA,
            BuildManifest.from_path(self.BUILD_MANIFEST),
            BundleManifest.from_path(self.DIST_MANIFEST_LOCAL)
        )

        dependency_installer.install_maven_dependencies()

        mock_makedirs.assert_called_with(
            os.path.realpath(
                os.path.join(
                    dependency_installer.maven_local_path, "org", "opensearch", "notification"
                )
            ),
            exist_ok=True
        )
        mock_request.assert_not_called()
        self.assertEqual(counter.call_count, 2375)
        mock_copyfile.assert_has_calls([
            call(
                os.path.join(self.DATA, "builds", "opensearch", "maven", "org", "opensearch", "notification", "alerting-notification-1.2.0.0.jar"),
                os.path.realpath(os.path.join(dependency_installer.maven_local_path, "org", "opensearch", "notification", "alerting-notification-1.2.0.0.jar"))
            )
        ])

    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_maven_dependencies_remote(self, mock_request: Mock, mock_copyfile: Mock, mock_makedirs: Mock) -> None:
        counter = ThreadSafeCounter()
        mock_request.side_effect = counter.thread_safe_count
        dependency_installer = DependencyInstallerOpenSearch(
            "https://ci.opensearch.org/x/y",
            BuildManifest.from_path(self.BUILD_MANIFEST),
            BundleManifest.from_path(self.DIST_MANIFEST_REMOTE)
        )

        dependency_installer.install_maven_dependencies()
        self.assertEqual(counter.call_count, 2375)

        mock_makedirs.assert_called_with(
            os.path.realpath(
                os.path.join(
                    dependency_installer.maven_local_path, "org", "opensearch", "notification"
                )
            ),
            exist_ok=True
        )
        mock_copyfile.assert_not_called()
        mock_request.assert_has_calls([
            call(
                "https://ci.opensearch.org/x/y/builds/opensearch/maven/org/opensearch/notification/alerting-notification-1.2.0.0.jar",
                os.path.realpath(os.path.join(dependency_installer.maven_local_path, "org", "opensearch", "notification", "alerting-notification-1.2.0.0.jar"))
            )
        ])

    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_maven_dependencies_remote_failure(self, mock_request: Mock, mock_copyfile: Mock, mock_makedirs: Mock) -> None:
        def mock_retrieve(source: str, dest: str) -> str:
            raise HTTPError(url=source, hdrs=None, fp=None, msg="Not Found", code=404)

        mock_request.side_effect = mock_retrieve

        dependency_installer = DependencyInstallerOpenSearch(
            "https://ci.opensearch.org/x/y",
            BuildManifest.from_path(self.BUILD_MANIFEST),
            BundleManifest.from_path(self.DIST_MANIFEST_REMOTE)
        )

        with self.assertRaises(HTTPError) as ctx:
            dependency_installer.install_maven_dependencies()
        self.assertEqual(str(ctx.exception), "HTTP Error 404: Not Found")

    @patch("os.makedirs")
    @patch("shutil.copyfile")
    @patch("urllib.request.urlretrieve")
    def test_install_build_dependencies_local(self, mock_request: Mock, mock_copyfile: Mock, mock_makedirs: Mock) -> None:
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
    def test_install_build_dependencies_remote(self, mock_request: Mock, mock_copyfile: Mock, mock_makedirs: Mock) -> None:
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
