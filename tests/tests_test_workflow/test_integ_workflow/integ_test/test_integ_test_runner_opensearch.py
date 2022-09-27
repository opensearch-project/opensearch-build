# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, Mock, patch

from test_workflow.integ_test.integ_test_runner_opensearch import IntegTestRunnerOpenSearch


class TestIntegTestRunnerOpenSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.args = MagicMock()
        self.test_manifest = MagicMock()

    @patch("test_workflow.integ_test.integ_test_runner_opensearch.IntegTestStartPropertiesOpenSearch")
    @patch("test_workflow.integ_test.integ_test_runner_opensearch.IntegTestSuiteOpenSearch")
    @patch("test_workflow.integ_test.integ_test_runner.TestRecorder")
    @patch("test_workflow.integ_test.integ_test_runner.TemporaryDirectory")
    def test_with_integ_test(self, mock_temp: Mock, mock_test_recorder: Mock, mock_suite: Mock, mock_properties: Mock) -> None:
        self.args.paths = {"opensearch": "test-path"}
        self.args.component = "sql"
        self.args.test_run_id = "12345"

        mock_test_config = MagicMock()
        mock_test_config.integ_test = MagicMock()
        self.test_manifest.components = {"sql": mock_test_config}

        mock_bundle_manifest = MagicMock()
        mock_components = MagicMock()
        mock_component = MagicMock()
        mock_component.name = "sql"
        mock_components.select.return_value = [mock_component]
        mock_bundle_manifest.components = mock_components

        mock_build_manifest = MagicMock()
        mock_dependency_installer = MagicMock()

        mock_properties_object = MagicMock()
        mock_properties_object.bundle_manifest = mock_bundle_manifest
        mock_properties_object.build_manifest = mock_build_manifest
        mock_properties_object.dependency_installer = mock_dependency_installer

        mock_properties.return_value = mock_properties_object

        mock_suite_object = MagicMock()
        mock_test_results = MagicMock()

        mock_suite_object.execute_tests.return_value = mock_test_results

        mock_suite.return_value = mock_suite_object

        mock_path = MagicMock()
        mock_temp.return_value.__enter__.return_value.path = mock_path

        mock_test_recorder_object = MagicMock()
        mock_test_recorder.return_value = mock_test_recorder_object

        runner = IntegTestRunnerOpenSearch(self.args, self.test_manifest)

        # call the test target
        results = runner.run()

        self.assertEqual(results["sql"], mock_test_results)

        mock_suite.assert_called_once_with(
            mock_properties_object.dependency_installer,
            mock_component,
            mock_test_config,
            mock_properties_object.bundle_manifest,
            mock_properties_object.build_manifest,
            mock_path,
            mock_test_recorder_object
        )

    @patch("test_workflow.integ_test.integ_test_runner_opensearch.IntegTestStartPropertiesOpenSearch")
    @patch("test_workflow.integ_test.integ_test_runner_opensearch.IntegTestSuiteOpenSearch")
    def test_without_integ_test(self, mock_suite: Mock, mock_properties: Mock) -> None:
        self.args.paths = {"opensearch": "test-path"}
        self.args.component = "sql"
        self.args.test_run_id = "12345"

        mock_test_config = MagicMock()
        mock_test_config.integ_test = None
        self.test_manifest.components = {"sql": mock_test_config}

        mock_bundle_manifest = MagicMock()
        mock_components = MagicMock()
        mock_component = MagicMock()
        mock_component.name = "sql"
        mock_components.select.return_value = [mock_component]
        mock_bundle_manifest.components = mock_components

        mock_build_manifest = MagicMock()
        mock_dependency_installer = MagicMock()

        mock_properties_object = MagicMock()
        mock_properties_object.bundle_manifest = mock_bundle_manifest
        mock_properties_object.build_manifest = mock_build_manifest
        mock_properties_object.dependency_installer = mock_dependency_installer

        mock_properties.return_value = mock_properties_object

        runner = IntegTestRunnerOpenSearch(self.args, self.test_manifest)

        # call the test target
        results = runner.run()

        self.assertEqual(results.__len__(), 0)
        mock_suite.assert_not_called()

    @patch("test_workflow.integ_test.integ_test_runner_opensearch.IntegTestStartPropertiesOpenSearch")
    @patch("test_workflow.integ_test.integ_test_runner_opensearch.IntegTestSuiteOpenSearch")
    def test_component_not_in_test_manifest(self, mock_suite: Mock, mock_properties: Mock) -> None:
        self.args.paths = {"opensearch": "test-path"}
        self.args.component = "sql"
        self.args.test_run_id = "12345"

        mock_test_config = MagicMock()
        mock_test_config.integ_test = MagicMock()
        self.test_manifest.components = {"alerting": mock_test_config}

        mock_bundle_manifest = MagicMock()
        mock_components = MagicMock()
        mock_component = MagicMock()
        mock_component.name = "sql"
        mock_components.select.return_value = [mock_component]
        mock_bundle_manifest.components = mock_components

        mock_build_manifest = MagicMock()
        mock_dependency_installer = MagicMock()

        mock_properties_object = MagicMock()
        mock_properties_object.bundle_manifest = mock_bundle_manifest
        mock_properties_object.build_manifest = mock_build_manifest
        mock_properties_object.dependency_installer = mock_dependency_installer

        mock_properties.return_value = mock_properties_object

        mock_suite_object = MagicMock()
        mock_test_results = MagicMock()

        mock_suite_object.execute_tests.return_value = mock_test_results

        mock_suite.return_value = mock_suite_object

        runner = IntegTestRunnerOpenSearch(self.args, self.test_manifest)

        # call the test target
        results = runner.run()

        self.assertEqual(results.__len__(), 0)
        mock_suite.assert_not_called()
