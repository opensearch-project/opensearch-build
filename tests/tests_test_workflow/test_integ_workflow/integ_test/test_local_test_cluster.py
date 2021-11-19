# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, PropertyMock, mock_open, patch

import requests
import yaml

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from system.process import Process
from system.temporary_directory import TemporaryDirectory
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.test_cluster import ClusterCreationException


class LocalTestClusterTests(unittest.TestCase):

    DATA = os.path.join(os.path.dirname(__file__), "data")

    BUILD_MANIFEST = os.path.join(DATA, "build_manifest.yml")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def setUp(self, mock_test_recorder):
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests_manifests", "data"))
        self.work_dir = TemporaryDirectory()
        self.process = self.__get_process()
        self.process.returncode = 0
        self.bundle_manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.build_manifest = BuildManifest.from_path(self.BUILD_MANIFEST)
        self.dependency_installer = DependencyInstaller(self.DATA, self.build_manifest, self.bundle_manifest)
        self.local_test_cluster = LocalTestCluster(
            self.dependency_installer,
            self.work_dir.name,
            "sql",
            {"script.context.field.max_compilations_rate": "1000/1m"},
            self.bundle_manifest,
            True,
            "with-security",
            mock_test_recorder,
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

    def __mock_connection_error_response(*args, **kwargs):
        raise requests.exceptions.ConnectionError()

    def __mock_process(*args, **kwargs):
        return LocalTestClusterTests.MockProcess(12)

    def __get_process(self):
        return subprocess.Popen((sys.executable, "-c", "pass"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @patch.object(Process, 'start')
    @patch("yaml.dump")
    @patch("builtins.open", mock_open())
    def test_create_cluster(self, *mocks):
        self.local_test_cluster.download = MagicMock()
        self.local_test_cluster.wait_for_service = MagicMock()
        self.local_test_cluster.create_cluster()

        Process.start.assert_called_once()
        yaml.dump.assert_called_once_with({"script.context.field.max_compilations_rate": "1000/1m"})

    def test_endpoint(self):
        self.assertEqual(self.local_test_cluster.endpoint(), "localhost")

    def test_port(self):
        self.assertEqual(self.local_test_cluster.port(), 9200)

    def test_url(self):
        self.assertEqual(self.local_test_cluster.url("/_cluster/health"), "https://localhost:9200/_cluster/health")

    @patch("requests.get", side_effect=__mock_response)
    def test_wait_for_service(self, mock_requests):
        self.local_test_cluster.wait_for_service()
        requests.get.assert_called_once_with(self.local_test_cluster.url("/_cluster/health"), verify=False, auth=("admin", "admin"))

    @patch("time.sleep")
    @patch("requests.get", side_effect=__mock_response)
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_wait_for_service_cluster_unavailable(self, mock_test_recorder, *mocks):
        local_test_cluster = LocalTestCluster(
            self.dependency_installer, self.work_dir.name, "index-management", "", self.bundle_manifest, False, "without-security", mock_test_recorder
        )
        with self.assertRaises(ClusterCreationException) as err:
            local_test_cluster.wait_for_service()
            requests.get.assert_called_once_with("http://localhost:9200/_cluster/health", verify=False, auth=("admin", "admin"))
        self.assertEqual(str(err.exception), "Cluster is not available after 10 attempts")

    @patch("time.sleep")
    @patch('system.process.Process.stdout_data', new_callable=PropertyMock)
    @patch('system.process.Process.stderr_data', new_callable=PropertyMock)
    @patch("requests.get", side_effect=__mock_connection_error_response)
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_wait_for_service_cluster_unavailable_connection_error(self, mock_test_recorder, mock_stdout_data, mock_stderr_data, *mocks):
        local_test_cluster = LocalTestCluster(
            self.dependency_installer, self.work_dir.name, "index-management", "", self.bundle_manifest, False, "without-security", mock_test_recorder
        )
        with self.assertRaises(ClusterCreationException) as err:
            local_test_cluster.wait_for_service()
            requests.get.assert_called_once_with("http://localhost:9200/_cluster/health", verify=False, auth=("admin", "admin"))
        self.assertEqual(str(err.exception), "Cluster is not available after 10 attempts")
        self.assertEqual(mock_stdout_data.call_count, 10)
        self.assertEqual(mock_stderr_data.call_count, 10)

    @patch.object(Process, 'terminate', return_value=("1"))
    def test_terminate_process(self, *mocks):
        self.local_test_cluster.terminate_process()
        Process.terminate.assert_called_once()
