# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.integ_test.service import ServiceTerminationResult
from test_workflow.test_cluster import ClusterServiceNotInitializedException


class LocalTestClusterTests(unittest.TestCase):

    def setUp(self) -> None:
        mock_manifest = MagicMock()
        mock_manifest.build.version = "1.1.0"
        mock_manifest.build.distribution = "tar"
        self.manifest = mock_manifest

        self.work_dir = "test_work_dir"

        self.component_name = "sql"
        self.security_enabled = True
        self.component_test_config = "test_config"
        self.additional_cluster_config = {"script.context.field.max_compilations_rate": "1000/1m"}
        self.save_logs = ""
        self.dependency_installer = None
        self.test_recorder = None

    @patch("test_workflow.integ_test.local_test_cluster.ServiceOpenSearch")
    def test_start(self, mock_service: Mock) -> None:
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_object = MagicMock()
        mock_service.return_value = mock_service_object

        cluster = LocalTestCluster(
            self.dependency_installer,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.manifest,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        cluster.start()

        mock_service.assert_called_once_with(
            "1.1.0",
            "tar",
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            os.path.join(self.work_dir, "local-test-cluster")
        )

        mock_service_object.start.assert_called_once()
        mock_service_object.wait_for_service.assert_called_once()

    @patch("test_workflow.integ_test.local_test_cluster.ServiceOpenSearch")
    @patch("test_workflow.test_cluster.TestResultData")
    def test_terminate(self, mock_test_result_data: Mock, mock_service: Mock) -> None:
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_object = MagicMock()
        mock_service.return_value = mock_service_object

        cluster = LocalTestCluster(
            self.dependency_installer,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.manifest,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        mock_log_files = MagicMock()

        mock_service_object.terminate.return_value = ServiceTerminationResult(
            123,
            "test stdout_data",
            "test stderr_data",
            mock_log_files
        )

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        cluster.terminate()

        mock_service_object.terminate.assert_called_once()

        mock_test_result_data.assert_called_once_with(
            self.component_name,
            self.component_test_config,
            123,
            "test stdout_data",
            "test stderr_data",
            mock_log_files
        )

        mock_local_cluster_logs.save_test_result_data.assert_called_once_with(mock_test_result_data_object)

    @patch("test_workflow.integ_test.local_test_cluster.ServiceOpenSearch")
    def test_terminate_service_not_initialized(self, mock_service: Mock) -> None:
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service.return_value = None

        cluster = LocalTestCluster(
            self.dependency_installer,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.manifest,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        with self.assertRaises(ClusterServiceNotInitializedException) as ctx:
            cluster.terminate()

        self.assertEqual(str(ctx.exception), "Service is not initialized")

    @patch("test_workflow.integ_test.local_test_cluster.ServiceOpenSearch")
    def test_endpoint_port(self, mock_service: Mock) -> None:
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_object = MagicMock()
        mock_service.return_value = mock_service_object

        cluster = LocalTestCluster(
            self.dependency_installer,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.manifest,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        self.assertEqual(cluster.endpoint, "localhost")
        self.assertEqual(cluster.port, 9200)
