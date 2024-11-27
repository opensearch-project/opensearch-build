# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import json
import os
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock, mock_open, patch

from test_workflow.smoke_test.smoke_test_runner import SmokeTestRunner


class TestSmokeTestRunner(SmokeTestRunner):
    """Concrete class for testing purposes only."""

    def start_test(self, work_dir: Path) -> str:
        # Mock implementation of abstract method
        return "Test results"


class TestSmokeTestRunnerMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.args = MagicMock()
        self.test_manifest = MagicMock()
        mock_components = MagicMock()
        mock_component = MagicMock()
        mock_component.name = "opensearch"
        mock_component.smoke_test = True
        mock_components.select.return_value = [mock_component]
        self.test_manifest.components = mock_components

    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("builtins.open", new_callable=mock_open, read_data="paths:\n  /_cat/plugins:\n    get:\n      parameters: []")
    @patch("os.path.dirname", return_value="/dummy-path")
    @patch("os.path.exists", return_value=True)
    def test_extract_paths_from_yaml(self, mock_exists: Mock, mock_dirname: Mock, mock_open_file: Mock,
                                     mock_recorder: Mock) -> None:
        runner = TestSmokeTestRunner(self.args, self.test_manifest)

        component_name = "test_component"

        # Run extract_paths_from_yaml and check output
        result = runner.extract_paths_from_yaml(component_name)
        expected_output = {"/_cat/plugins": {"get": {"parameters": []}}}  # type: Any

        self.assertEqual(result, expected_output)
        mock_open_file.assert_called_once_with(os.path.join("/dummy-path", "smoke_tests_spec", f"{component_name}.yml"), 'r')

    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    def test_convert_parameter_json(self, mock_recorder: Mock) -> None:
        runner = TestSmokeTestRunner(self.args, self.test_manifest)
        data = [{"param1": "value1"}, {"param2": "value2"}]
        result = runner.convert_parameter_json(data)
        expected_output = json.dumps(data[0]) + "\n" + json.dumps(data[1]) + "\n"
        self.assertEqual(result, expected_output)

    @patch("test_workflow.smoke_test.smoke_test_runner.TestRecorder")
    @patch("test_workflow.smoke_test.smoke_test_runner.SmokeTestClusterOpenSearch")
    @patch("test_workflow.smoke_test.smoke_test_runner.TemporaryDirectory")
    def test_run(self, mock_temp_dir: Mock, mock_cluster: Mock, mock_recorder: Mock) -> None:
        runner = TestSmokeTestRunner(self.args, self.test_manifest)
        # Mock temporary directory context and path
        temp_dir_instance = mock_temp_dir.return_value.__enter__.return_value
        temp_dir_instance.path = "/mock/temp/path"

        # # Mock cluster behavior for start and uninstall
        mock_cluster_instance = mock_cluster.return_value
        mock_cluster_instance.__start_cluster__ = MagicMock()
        mock_cluster_status = MagicMock()
        mock_cluster_status.side_effect = [False, True]  # Fails first check, passes second
        mock_cluster_instance.__check_cluster_ready__ = mock_cluster_status
        mock_cluster_instance.__uninstall__ = MagicMock()

        # Run the method
        result = runner.run()

        # Assert cluster start, ready check, and uninstall were called
        mock_cluster_instance.__start_cluster__.assert_called_once_with("/mock/temp/path")
        self.assertEqual(mock_cluster_instance.__check_cluster_ready__.call_count, 2)  # Attempted twice
        mock_cluster_instance.__uninstall__.assert_called_once()

        # Assert result returned from start_test
        self.assertEqual(result, "Test results")
