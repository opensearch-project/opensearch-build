# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards
from test_workflow.integ_test.service import ServiceTerminationResult
from test_workflow.test_cluster import ClusterServiceNotInitializedException


class LocalTestClusterOpenSearchDashboardsTests(unittest.TestCase):

    def setUp(self):
        mock_bundle_manifest_opensearch = MagicMock()
        mock_bundle_manifest_opensearch.build.version = "1.1.0"
        self.mock_bundle_manifest_opensearch = mock_bundle_manifest_opensearch

        mock_bundle_manifest_opensearch_dashboards = MagicMock()
        mock_bundle_manifest_opensearch_dashboards.build.version = "1.1.0"
        mock_bundle_manifest_opensearch_dashboards.build.platform = "linux"
        mock_bundle_manifest_opensearch_dashboards.build.architecture = "x64"
        self.mock_bundle_manifest_opensearch_dashboards = mock_bundle_manifest_opensearch_dashboards

        dependency_installer_opensearch = MagicMock()
        self.dependency_installer_opensearch = dependency_installer_opensearch

        dependency_installer_opensearch_dashboards = MagicMock()
        self.dependency_installer_opensearch_dashboards = dependency_installer_opensearch_dashboards

        self.work_dir = "test_work_dir"

        self.component_name = "sql"
        self.security_enabled = True
        self.component_test_config = "test_config"
        self.additional_cluster_config = {"script.context.field.max_compilations_rate": "1000/1m"}
        self.save_logs = ""
        self.dependency_installer = ""
        self.test_recorder = ""

    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearch")
    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearchDashboards")
    def test_start(self, mock_service_opensearch_dashboards, mock_service_opensearch):
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_opensearch_object = MagicMock()
        mock_service_opensearch.return_value = mock_service_opensearch_object

        mock_service_opensearch_dashboards_object = MagicMock()
        mock_service_opensearch_dashboards.return_value = mock_service_opensearch_dashboards_object

        cluster = LocalTestClusterOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.mock_bundle_manifest_opensearch,
            self.mock_bundle_manifest_opensearch_dashboards,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        cluster.start()

        mock_service_opensearch.assert_called_once_with(
            "1.1.0",
            {},
            self.security_enabled,
            self.dependency_installer_opensearch,
            os.path.join(self.work_dir, "local-test-cluster")
        )

        mock_service_opensearch_object.start.assert_called_once()
        mock_service_opensearch_object.wait_for_service.assert_called_once()

        mock_service_opensearch_dashboards.assert_called_once_with(
            "1.1.0",
            "linux",
            "x64",
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer_opensearch_dashboards,
            os.path.join(self.work_dir, "local-test-cluster")
        )

        mock_service_opensearch_dashboards_object.start.assert_called_once()
        mock_service_opensearch_dashboards_object.wait_for_service.assert_called_once()

    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearch")
    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearchDashboards")
    @patch("test_workflow.test_cluster.TestResultData")
    def test_terminate(self, mock_test_result_data, mock_service_opensearch_dashboards, mock_service_opensearch):
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_opensearch_object = MagicMock()
        mock_service_opensearch.return_value = mock_service_opensearch_object

        mock_service_opensearch_dashboards_object = MagicMock()
        mock_service_opensearch_dashboards.return_value = mock_service_opensearch_dashboards_object

        cluster = LocalTestClusterOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.mock_bundle_manifest_opensearch,
            self.mock_bundle_manifest_opensearch_dashboards,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        mock_log_files = MagicMock()
        mock_service_opensearch_dashboards_object.terminate.return_value = ServiceTerminationResult(123, "test stdout_data", "test stderr_data", mock_log_files)

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        cluster.terminate()

        mock_service_opensearch_object.terminate.assert_called_once()
        mock_service_opensearch_dashboards_object.terminate.assert_called_once()

        mock_test_result_data.assert_called_once_with(
            self.component_name,
            self.component_test_config,
            123,
            "test stdout_data",
            "test stderr_data",
            mock_log_files
        )

        mock_local_cluster_logs.save_test_result_data.assert_called_once_with(mock_test_result_data_object)

    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearch")
    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearchDashboards")
    def test_terminate_service_not_initialized(self, mock_service_opensearch_dashboards, mock_service_opensearch):
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_opensearch_object = MagicMock()
        mock_service_opensearch.return_value = mock_service_opensearch_object

        mock_service_opensearch_dashboards.return_value = None

        cluster = LocalTestClusterOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.mock_bundle_manifest_opensearch,
            self.mock_bundle_manifest_opensearch_dashboards,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        with self.assertRaises(ClusterServiceNotInitializedException) as ctx:
            cluster.terminate()

        self.assertEqual(str(ctx.exception), "Service is not initialized")

        mock_service_opensearch_object.terminate.assert_called_once()

    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearch")
    @patch("test_workflow.integ_test.local_test_cluster_opensearch_dashboards.ServiceOpenSearchDashboards")
    def test_endpoint_port(self, mock_service_opensearch_dashboards, mock_service_opensearch):
        mock_test_recorder = MagicMock()
        mock_local_cluster_logs = MagicMock()
        mock_test_recorder.local_cluster_logs = mock_local_cluster_logs

        mock_service_opensearch_object = MagicMock()
        mock_service_opensearch.return_value = mock_service_opensearch_object

        mock_service_opensearch_dashboards_object = MagicMock()
        mock_service_opensearch_dashboards.return_value = mock_service_opensearch_dashboards_object

        cluster = LocalTestClusterOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.mock_bundle_manifest_opensearch,
            self.mock_bundle_manifest_opensearch_dashboards,
            self.security_enabled,
            self.component_test_config,
            mock_test_recorder
        )

        self.assertEqual(cluster.endpoint(), "localhost")
        self.assertEqual(cluster.port(), 5601)
