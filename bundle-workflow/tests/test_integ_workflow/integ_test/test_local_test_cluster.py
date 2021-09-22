# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

import requests

from manifests.bundle_manifest import BundleManifest
from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.test_cluster import ClusterCreationException


class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code


class LocalTestClusterTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.data_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../../tests_manifests/data")
        )
        self.manifest_filename = os.path.join(
            self.data_path, "opensearch-bundle-1.1.0.yml"
        )
        self.manifest = BundleManifest.from_path(self.manifest_filename)
        with tempfile.TemporaryDirectory() as work_dir:
            self.local_test_cluster = LocalTestCluster(work_dir, "index-management", "", self.manifest, True, "dummy-bucket")

    def mocked_response(*args, **kwargs):
        if args[0] == "https://localhost:9200/_cluster/health":
            return MockResponse({"status": "green"}, 200)
        else:
            return MockResponse({"status": "red"}, 404)

    @patch("subprocess.Popen")
    def test_create_cluster(self, *mocks):
        self.local_test_cluster.download = MagicMock()
        self.local_test_cluster.wait_for_service = MagicMock()
        with patch("builtins.open", mock_open()):
            with open("stdout.txt", "w") as stdout, open("stderr.txt", "w") as stderr:
                self.local_test_cluster.create_cluster()
                subprocess.Popen.assert_called_with(
                    "./opensearch-tar-install.sh",
                    cwd=f"opensearch-{self.manifest.build.version}",
                    shell=True,
                    stdout=stdout,
                    stderr=stderr,
                )

    def test_endpoint(self):
        self.assertEqual(self.local_test_cluster.endpoint(), "localhost")

    def test_port(self):
        self.assertEqual(self.local_test_cluster.port(), 9200)

    def test_url(self):
        self.assertEqual(self.local_test_cluster.url("/_cluster/health"), "https://localhost:9200/_cluster/health")

    @patch("os.chdir")
    @patch("subprocess.check_call")
    @patch("test_workflow.integ_test.local_test_cluster.S3Bucket")
    def test_download(self, mock_s3_bucket, *mocks):
        s3_bucket = mock_s3_bucket.return_value
        with tempfile.TemporaryDirectory() as work_dir:
            local_test_cluster = LocalTestCluster(work_dir, "index-management", "", self.manifest, True, "bucket_name")
            s3_path = BundleManifest.get_tarball_relative_location(
                self.manifest.build.id, self.manifest.build.version, self.manifest.build.architecture)
            work_dir_path = os.path.join(work_dir, "local-test-cluster")
            bundle_name = BundleManifest.get_tarball_name(self.manifest.build.version, self.manifest.build.architecture)
            local_test_cluster.download()
            os.chdir.assert_called_once_with(work_dir_path)
            s3_bucket.download_file.assert_called_once_with(s3_path, work_dir_path)
            subprocess.check_call.assert_called_once_with(f"tar -xzf {bundle_name}", shell=True)

    @patch("subprocess.check_call")
    def test_disable_security(self, mock_subprocess):
        self.local_test_cluster.disable_security("tmp")
        mock_subprocess.assert_called_once_with(
            f'echo "plugins.security.disabled: true" >> {os.path.join("tmp", "config", "opensearch.yml")}',
            shell=True,
        )

    @patch("requests.get", side_effect=mocked_response)
    def test_wait_for_service(self, mock_requests):
        self.local_test_cluster.wait_for_service()
        requests.get.assert_called_once_with(self.local_test_cluster.url("/_cluster/health"), verify=False, auth=("admin", "admin"))

    @patch("requests.get", side_effect=mocked_response)
    def test_wait_for_service_cluster_unavailable(self, mock_requests):
        with tempfile.TemporaryDirectory() as work_dir:
            local_test_cluster = LocalTestCluster(work_dir, "index-management", "", self.manifest, False, "dummy-bucket")
            with self.assertRaises(ClusterCreationException):
                local_test_cluster.wait_for_service()
                requests.get.assert_called_once_with("http://localhost:9200/_cluster/health", verify=False, auth=("admin", "admin"))
