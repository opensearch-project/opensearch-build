# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, mock_open, patch

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from test_workflow.smoke_test.smoke_test_cluster_opensearch import SmokeTestClusterOpenSearch


class TestSmokeTestClusterOpenSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.TEST_MANIFEST = TestManifest.from_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                                                                 "test_manifest.yml"))
        self.BUILD_MANIFEST = BuildManifest.from_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                                                                   "build_manifest.yml"))
        self.BUNDLE_MANIFEST = BundleManifest.from_path(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                     "data", "bundle_manifest.yml"))

    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Distributions.get_distribution")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BundleManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BuildManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.TestManifest.from_path")
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("shutil.copy2")
    def test_download_or_copy_bundle_http(self, mock_copy: Mock, mock_open_file: Mock, mock_requests_get: Mock,
                                          mock_test_manifest: Mock, mock_build_manifest: Mock,
                                          mock_bundle_manifest: Mock, mock_distribution: Mock) -> None:
        mock_test_manifest.return_value = self.TEST_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_bundle_manifest.return_value = self.BUNDLE_MANIFEST
        # Setup test arguments and mock response
        args = MagicMock()
        args.paths.get.return_value = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.17.0/10292/linux/x64/tar/"
        test_recorder = MagicMock()

        # Initialize cluster
        cluster = SmokeTestClusterOpenSearch(args, "/mock/work_dir", test_recorder)

        # Mock response for an HTTP download
        mock_response = MagicMock()
        mock_response.content = "opensearch-2.17.0-linux-x64.tar.gz"
        mock_requests_get.return_value = mock_response

        artifact_name = cluster.download_or_copy_bundle("/mock/work_dir")

        # Ensure it tries to download and save the file
        self.assertEqual(artifact_name, "opensearch-2.17.0-linux-x64.tar.gz")
        mock_requests_get.assert_called_once_with(
            "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.17.0/10292/linux/x64/tar/dist/"
            "opensearch/opensearch-2.17.0-linux-x64.tar.gz")
        mock_open_file.assert_called_with(os.path.join("/mock/work_dir", "opensearch-2.17.0-linux-x64.tar.gz"), "wb")
        mock_open_file().write.assert_called_once_with("opensearch-2.17.0-linux-x64.tar.gz")

    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Distributions.get_distribution")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BundleManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BuildManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.TestManifest.from_path")
    @patch("os.path.isfile", return_value=True)
    @patch("shutil.copy2")
    def test_download_or_copy_bundle_local(self, mock_copy2: Mock, mock_isfile: Mock, mock_test_manifest: Mock,
                                           mock_build_manifest: Mock, mock_bundle_manifest: Mock, mock_distribution: Mock) -> None:
        mock_test_manifest.return_value = self.TEST_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_bundle_manifest.return_value = self.BUNDLE_MANIFEST
        # Setup test arguments
        args = MagicMock()
        args.paths.get.return_value = os.path.join("local", "temp", "opensearch")
        test_recorder = MagicMock()

        # Initialize cluster
        cluster = SmokeTestClusterOpenSearch(args, "/mock/work_dir", test_recorder)

        artifact_name = cluster.download_or_copy_bundle("/mock/work_dir")

        # Verify file copy operation
        mock_copy2.assert_called_once_with(
            os.path.join("local", "temp", "opensearch", "dist", "opensearch", "opensearch-2.17.0-linux-x64.tar.gz"),
            os.path.join("/mock/work_dir", "opensearch-2.17.0-linux-x64.tar.gz"))
        self.assertEqual(artifact_name, "opensearch-2.17.0-linux-x64.tar.gz")

    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Distributions")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BundleManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BuildManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.TestManifest.from_path")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Process")
    def test_installation(self, mock_process: Mock, mock_test_manifest: Mock,
                          mock_build_manifest: Mock, mock_bundle_manifest: Mock, mock_distributions: Mock) -> None:
        mock_test_manifest.return_value = self.TEST_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_bundle_manifest.return_value = self.BUNDLE_MANIFEST

        args = MagicMock()
        args.paths.get.return_value = "/mock/work_dir"
        test_recorder = MagicMock()

        mock_distribution = MagicMock()
        mock_distributions.get_distribution.return_value = mock_distribution

        # Initialize cluster and call installation
        cluster = SmokeTestClusterOpenSearch(args, "/mock/work_dir", test_recorder)
        cluster.__installation__("/mock/work_dir")

        # Check that install was called correctly
        mock_distribution.install.assert_called_once()

    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Distributions.get_distribution")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BundleManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BuildManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.TestManifest.from_path")
    @patch("time.sleep", return_value=None)  # Skip actual sleep for testing
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Process")
    def test_start_cluster(self, mock_process: Mock, mock_sleep: Mock, mock_test_manifest: Mock,
                           mock_build_manifest: Mock, mock_bundle_manifest: Mock, mock_distribution: Mock) -> None:
        mock_test_manifest.return_value = self.TEST_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_bundle_manifest.return_value = self.BUNDLE_MANIFEST

        args = MagicMock()
        args.paths.get.return_value = "/mock/work_dir"
        test_recorder = MagicMock()
        mock_process_handler = mock_process.return_value

        # Initialize cluster and start it
        cluster = SmokeTestClusterOpenSearch(args, "/mock/work_dir", test_recorder)
        cluster.__start_cluster__("/mock/work_dir")

        # Verify start command was called
        mock_process_handler.start.assert_called_once_with(cluster.distribution.start_cmd, cluster.distribution.install_dir, cluster.distribution.require_sudo)

    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Distributions.get_distribution")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BundleManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BuildManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.TestManifest.from_path")
    @patch("requests.get")
    def test_check_cluster_ready(self, mock_requests_get: Mock, mock_test_manifest: Mock,
                                 mock_build_manifest: Mock, mock_bundle_manifest: Mock, mock_distribution: Mock) -> None:
        mock_test_manifest.return_value = self.TEST_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_bundle_manifest.return_value = self.BUNDLE_MANIFEST

        args = MagicMock()
        test_recorder = MagicMock()
        cluster = SmokeTestClusterOpenSearch(args, "/mock/work_dir", test_recorder)

        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        # Check if the cluster is ready
        self.assertTrue(cluster.__check_cluster_ready__())
        mock_requests_get.assert_called_once_with("https://localhost:9200/", verify=False, auth=("admin", "myStrongPassword123!"))

    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Distributions.get_distribution")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BundleManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.BuildManifest.from_urlpath")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.TestManifest.from_path")
    @patch("test_workflow.smoke_test.smoke_test_cluster_opensearch.Process")
    def test_uninstall(self, mock_process: Mock, mock_test_manifest: Mock,
                       mock_build_manifest: Mock, mock_bundle_manifest: Mock, mock_distribution: Mock) -> None:
        mock_test_manifest.return_value = self.TEST_MANIFEST
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_bundle_manifest.return_value = self.BUNDLE_MANIFEST

        args = MagicMock()
        test_recorder = MagicMock()
        mock_process_handler = mock_process.return_value

        # Initialize cluster and call uninstall
        cluster = SmokeTestClusterOpenSearch(args, "/mock/work_dir", test_recorder)
        cluster.__uninstall__()

        # Verify termination
        mock_process_handler.terminate.assert_called_once()
