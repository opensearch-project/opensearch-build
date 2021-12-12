# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from test_workflow.integ_test.integ_test_runners import IntegTestRunners


class TestIntegTestRunners(unittest.TestCase):

    def test_opensearch(self):

        mock_args = MagicMock()
        mock_test_manifest = MagicMock()
        mock_test_manifest.name = "OpenSearch"

        mock_opensearch_runner_object = MagicMock()
        mock_opensearch_runner = MagicMock()
        mock_opensearch_runner.return_value = mock_opensearch_runner_object

        mock_opensearch_dashboards_runner = MagicMock()

        with patch.dict("test_workflow.integ_test.integ_test_runners.IntegTestRunners.RUNNERS", {
            "OpenSearch": mock_opensearch_runner,
            "OpenSearch Dashboards": mock_opensearch_dashboards_runner,
        }):
            runner = IntegTestRunners.from_test_manifest(mock_args, mock_test_manifest)

            self.assertEqual(runner, mock_opensearch_runner_object)

            mock_opensearch_runner.assert_called_once_with(mock_args, mock_test_manifest)

    def test_opensearch_dashboards(self):

        mock_args = MagicMock()
        mock_test_manifest = MagicMock()
        mock_test_manifest.name = "OpenSearch Dashboards"

        mock_opensearch_runner = MagicMock()

        mock_opensearch_dashboards_runner_object = MagicMock()
        mock_opensearch_dashboards_runner = MagicMock()
        mock_opensearch_dashboards_runner.return_value = mock_opensearch_dashboards_runner_object

        with patch.dict("test_workflow.integ_test.integ_test_runners.IntegTestRunners.RUNNERS", {
            "OpenSearch": mock_opensearch_runner,
            "OpenSearch Dashboards": mock_opensearch_dashboards_runner,
        }):
            runner = IntegTestRunners.from_test_manifest(mock_args, mock_test_manifest)

            self.assertEqual(runner, mock_opensearch_dashboards_runner_object)
            mock_opensearch_dashboards_runner.assert_called_once_with(mock_args, mock_test_manifest)
