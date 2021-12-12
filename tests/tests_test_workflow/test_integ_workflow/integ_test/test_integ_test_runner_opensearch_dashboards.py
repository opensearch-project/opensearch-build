# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from test_workflow.integ_test.integ_test_runner_opensearch_dashboards import IntegTestRunnerOpenSearchDashboards


class TestIntegTestRunnerOpenSearchDashboards(unittest.TestCase):
    def setUp(self):
        self.args = MagicMock()
        self.test_manifest = MagicMock()

    @patch("test_workflow.integ_test.integ_test_runner_opensearch_dashboards.IntegTestStartPropertiesOpenSearch")
    @patch("test_workflow.integ_test.integ_test_runner_opensearch_dashboards.IntegTestStartPropertiesOpenSearchDashboards")
    @patch("test_workflow.integ_test.integ_test_runner_opensearch_dashboards.IntegTestSuiteOpenSearchDashboards")
    @patch("test_workflow.integ_test.integ_test_runner.TestRecorder")
    @patch("test_workflow.integ_test.integ_test_runner.TemporaryDirectory")
    def test_with_integ_test(self, mock_temp, mock_test_recorder, mock_suite, mock_properties, mock_properties_dependency):
        self.args.paths = {"opensearch-dashboards": "test-path"}
        self.args.component = "sql"
        self.args.test_run_id = "12345"

        mock_test_config = MagicMock()
        mock_test_config.integ_test = MagicMock()
        self.test_manifest.components = {"sql": mock_test_config}

        mock_build_manifest = MagicMock()
        mock_components = MagicMock()
        mock_component = MagicMock()
        mock_component.name = "sql"
        mock_components.select.return_value = [mock_component]
        mock_build_manifest.components = mock_components

        mock_bundle_manifest = MagicMock()
        mock_dependency_installer = MagicMock()

        mock_properties_object = MagicMock()
        mock_properties_object.bundle_manifest = mock_bundle_manifest
        mock_properties_object.build_manifest = mock_build_manifest
        mock_properties_object.dependency_installer = mock_dependency_installer

        mock_properties.return_value = mock_properties_object

        mock_properties_dependency_object = MagicMock()
        mock_properties_dependency_object.bundle_manifest = MagicMock()
        mock_properties_dependency_object.build_manifest = MagicMock()
        mock_properties_dependency_object.dependency_installer = MagicMock()
        mock_properties_dependency.return_value = mock_properties_dependency_object

        mock_suite_object = MagicMock()
        mock_test_results = MagicMock()

        mock_suite_object.execute_tests.return_value = mock_test_results

        mock_suite.return_value = mock_suite_object

        mock_temp.return_value.__enter__.return_value.name = "temp-name"

        mock_test_recorder_object = MagicMock()
        mock_test_recorder.return_value = mock_test_recorder_object

        runner = IntegTestRunnerOpenSearchDashboards(self.args, self.test_manifest)

        # call the test target
        results = runner.run()

        self.assertEqual(results["sql"], mock_test_results)

        mock_suite.assert_called_once_with(
            mock_properties_dependency_object.dependency_installer,
            mock_properties_object.dependency_installer,
            mock_component,
            mock_test_config,
            mock_properties_dependency_object.bundle_manifest,
            mock_properties_object.bundle_manifest,
            mock_properties_dependency_object.build_manifest,
            mock_properties_object.build_manifest,
            "temp-name",
            mock_test_recorder_object
        )
