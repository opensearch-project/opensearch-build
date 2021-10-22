# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

import requests
import yaml

from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.test_cluster import ClusterCreationException


class LocalTestClusterTests(unittest.TestCase):
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def setUp(self, mock_test_recorder):
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests_manifests", "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-bundle-1.1.0.yml")
        self.manifest = BundleManifest.from_path(self.manifest_filename)
        self.work_dir = TemporaryDirectory()
        self.process = self.__get_process()
        self.process.returncode = 0
        self.local_test_cluster = LocalTestCluster(
            self.work_dir.name,
            "sql",
            {"script.context.field.max_compilations_rate": "1000/1m"},
            self.manifest,
            True,
            "with-security",
            mock_test_recorder,
            "dummy-bucket",
        )

    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    class MockProcess:
        def __init__(self, pid):
            self.pid = pid

        def children(self, recursive):
            return []

    def __mock_response(*args, **kwargs):
        if args[0] == "https://localhost:9200/_cluster/health":
            return LocalTestClusterTests.MockResponse({"status": "green"}, 200)
        else:
            return LocalTestClusterTests.MockResponse({"status": "red"}, 404)

    def __mock_process(*args, **kwargs):
        return LocalTestClusterTests.MockProcess(12)

    def __get_process(self):
        return subprocess.Popen(
            (sys.executable, "-c", "pass"),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    @patch("subprocess.Popen")
    @patch("yaml.dump")
    @patch("builtins.open", mock_open())
    def test_create_cluster(self, *mocks):
        self.local_test_cluster.download = MagicMock()
        self.local_test_cluster.wait_for_service = MagicMock()
        self.local_test_cluster.create_cluster()
        subprocess.Popen.assert_called_with(
            "./opensearch-tar-install.sh",
            cwd=f"opensearch-{self.manifest.build.version}",
            shell=True,
            stdout=self.local_test_cluster.stdout,
            stderr=self.local_test_cluster.stderr,
        )
        yaml.dump.assert_called_once_with({"script.context.field.max_compilations_rate": "1000/1m"})

    def test_endpoint(self):
        self.assertEqual(self.local_test_cluster.endpoint(), "localhost")

    def test_port(self):
        self.assertEqual(self.local_test_cluster.port(), 9200)

    def test_url(self):
        self.assertEqual(
            self.local_test_cluster.url("/_cluster/health"),
            "https://localhost:9200/_cluster/health",
        )

    @patch("os.chdir")
    @patch("subprocess.check_call")
    @patch("test_workflow.integ_test.local_test_cluster.S3Bucket")
    def test_download(self, mock_s3_bucket, *mocks):
        s3_bucket = mock_s3_bucket.return_value
        s3_path = BundleManifest.get_tarball_relative_location(
            self.manifest.build.id,
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture,
        )
        work_dir_path = os.path.join(self.work_dir.name, "local-test-cluster")
        bundle_name = BundleManifest.get_tarball_name(
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture,
        )
        self.local_test_cluster.download()
        os.chdir.assert_called_once_with(work_dir_path)
        s3_bucket.download_file.assert_called_once_with(s3_path, work_dir_path)
        subprocess.check_call.assert_called_once_with(f"tar -xzf {bundle_name}", shell=True)

    @patch("requests.get", side_effect=__mock_response)
    def test_wait_for_service(self, mock_requests):
        self.local_test_cluster.wait_for_service()
        requests.get.assert_called_once_with(
            self.local_test_cluster.url("/_cluster/health"),
            verify=False,
            auth=("admin", "admin"),
        )

    @patch("time.sleep")
    @patch("requests.get", side_effect=__mock_response)
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_wait_for_service_cluster_unavailable(self, mock_test_recorder, *mocks):
        local_test_cluster = LocalTestCluster(
            self.work_dir.name,
            "index-management",
            "",
            self.manifest,
            False,
            "without-security",
            mock_test_recorder,
            "dummy-bucket",
        )
        with self.assertRaises(ClusterCreationException) as err:
            local_test_cluster.wait_for_service()
            requests.get.assert_called_once_with(
                "http://localhost:9200/_cluster/health",
                verify=False,
                auth=("admin", "admin"),
            )
        self.assertEqual(str(err.exception), "Cluster is not available after 10 attempts")

    @patch(
        "test_workflow.integ_test.local_test_cluster.psutil.Process",
        side_effect=__mock_process,
    )
    @patch("test_workflow.integ_test.local_test_cluster.subprocess.Popen.wait")
    @patch("test_workflow.integ_test.local_test_cluster.subprocess.Popen.terminate")
    @patch("test_workflow.integ_test.local_test_cluster.logging", return_value=MagicMock())
    def test_terminate_process(self, mock_logging, mock_terminate, mock_wait, mock_process):
        self.local_test_cluster.stdout = None
        self.local_test_cluster.stderr = None
        self.local_test_cluster.process = self.process
        self.local_test_cluster.terminate_process()
        mock_process.assert_called_once_with(self.process.pid)
        mock_terminate.assert_called_once()
        mock_wait.assert_called_once_with(10)
        mock_logging.info.assert_has_calls(
            [
                call(f"Sending SIGTERM to PID {self.process.pid}"),
                call("Waiting for process to terminate"),
                call("Process terminated with exit code 0"),
            ]
        )
        mock_logging.debug.assert_has_calls([call("Checking for child processes")])

    @patch(
        "test_workflow.integ_test.local_test_cluster.psutil.Process",
        side_effect=__mock_process,
    )
    @patch("test_workflow.integ_test.local_test_cluster.subprocess.Popen.wait")
    @patch("test_workflow.integ_test.local_test_cluster.subprocess.Popen.terminate")
    @patch("test_workflow.integ_test.local_test_cluster.logging", return_value=MagicMock())
    def test_terminate_process_timeout(self, mock_logging, mock_terminate, mock_wait, mock_process):
        self.local_test_cluster.stdout = None
        self.local_test_cluster.stderr = None
        mock_wait.side_effect = subprocess.TimeoutExpired(cmd="pass", timeout=1)
        with self.assertRaises(subprocess.TimeoutExpired):
            self.local_test_cluster.process = self.process
            self.local_test_cluster.terminate_process()
        mock_process.assert_called_once_with(self.process.pid)
        mock_terminate.assert_called_once()
        mock_wait.assert_called_with(10)
        mock_logging.info.assert_has_calls(
            [
                call(f"Sending SIGTERM to PID {self.process.pid}"),
                call("Waiting for process to terminate"),
                call("Process did not terminate after 10 seconds. Sending SIGKILL"),
                call("Waiting for process to terminate"),
                call("Process failed to terminate even after SIGKILL"),
                call("Process terminated with exit code 0"),
            ]
        )
