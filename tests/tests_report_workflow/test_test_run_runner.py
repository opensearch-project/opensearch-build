# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from manifests.test_manifest import TestManifest
from report_workflow.test_run_runner import TestRunRunner


class TestTestRunRunner(unittest.TestCase):
    TEST_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__), "data", "test_manifest.yml"
    )

    TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH = os.path.join(
        os.path.dirname(__file__), "data", "test-manifest-opensearch-dashboards.yml"
    )

    TEST_MANIFEST = TestManifest.from_path(TEST_MANIFEST_PATH)

    TEST_MANIFEST_OPENSEARCH_DASHBOARDS = TestManifest.from_path(TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH)

    @patch("report_workflow.report_args.ReportArgs")
    @patch("manifests.test_manifest.TestManifest")
    def test_runner_init(self, report_args_mock: MagicMock, test_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.test_type = "integ-test"

        test_run_runner = TestRunRunner(report_args_mock, self.TEST_MANIFEST)
        self.assertEqual(test_run_runner.name, "opensearch")
        self.assertEqual(test_run_runner.test_run_id, 123)
        self.assertEqual(test_run_runner.test_type, "integ-test")
        self.assertEqual(test_run_runner.test_manifest_path, self.TEST_MANIFEST_PATH)

    @patch("report_workflow.report_args.ReportArgs")
    @patch("manifests.test_manifest.TestManifest")
    def test_runner_update_test_run_data_local(self, report_args_mock: MagicMock, test_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.test_type = "integ-test"

        test_run_dict = TestRunRunner(report_args_mock, self.TEST_MANIFEST).update_test_run_data()
        self.assertEqual(test_run_dict.get("Command"), " ".join(["./test.sh", "integ-test", self.TEST_MANIFEST_PATH, "--paths", "opensearch=foo/bar"]))
        self.assertEqual(test_run_dict.get("TestType"), "integ-test")
        self.assertEqual(test_run_dict.get("TestManifest"), self.TEST_MANIFEST_PATH)
        self.assertEqual(test_run_dict.get("DistributionManifest"), os.path.join("foo/bar", "dist", "opensearch", "manifest.yml"))
        self.assertEqual(test_run_dict.get("TestID"), "123")

    @patch("report_workflow.report_args.ReportArgs")
    @patch("manifests.test_manifest.TestManifest")
    def test_runner_update_test_run_data_url(self, report_args_mock: MagicMock, test_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "https://foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.test_type = "integ-test"

        test_run_dict = TestRunRunner(report_args_mock, self.TEST_MANIFEST).update_test_run_data()
        self.assertEqual(test_run_dict.get("Command"), " ".join(["./test.sh", "integ-test", self.TEST_MANIFEST_PATH, "--paths", "opensearch=https://foo/bar"]))
        self.assertEqual(test_run_dict.get("TestType"), "integ-test")
        self.assertEqual(test_run_dict.get("TestManifest"), self.TEST_MANIFEST_PATH)
        self.assertEqual(test_run_dict.get("DistributionManifest"), "/".join(["https://foo/bar", "dist", "opensearch", "manifest.yml"]))
        self.assertEqual(test_run_dict.get("TestID"), "123")

    @patch("yaml.safe_load")
    @patch("urllib.request.urlopen")
    @patch("validators.url")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url(self, report_args_mock: MagicMock, validators_mock: MagicMock, urlopen_mock: MagicMock, yaml_safe_load_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/mock"
        report_args_mock.test_type = "integ-test"

        validators_mock.return_value = True
        yaml_safe_load_mock.return_value = {"test_result": "PASS"}
        urlopen_mock.return_value = MagicMock()

        test_run_component_dict = TestRunRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        urlopen_mock.assert_has_calls([call('https://ci.opensearch.org/ci/dbc/mock/test-results/123/integ-test/geospatial/with-security/geospatial.yml')])
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "PASS")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"], "https://ci.opensearch.org/ci/dbc/mock/test-results/123/integ-test/geospatial/with-security/geospatial.yml")

    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("validators.url")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local(self, report_args_mock: MagicMock, validators_mock: MagicMock, mock_open: MagicMock, yaml_safe_load_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/mock"
        report_args_mock.test_type = "integ-test"

        validators_mock.return_value = False
        yaml_safe_load_mock.return_value = {"test_result": "PASS"}
        mock_open.return_value = MagicMock()

        test_run_component_dict = TestRunRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        mock_open.assert_has_calls([call('https://ci.opensearch.org/ci/dbc/mock/test-results/123/integ-test/geospatial/with-security/geospatial.yml', 'r', encoding='utf8')])
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "PASS")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"], "https://ci.opensearch.org/ci/dbc/mock/test-results/123/integ-test/geospatial/with-security/geospatial.yml")

    @patch("yaml.safe_load")
    @patch("validators.url")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url_invalid(self, report_args_mock: MagicMock, validators_mock: MagicMock, yaml_safe_load_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/mock"
        report_args_mock.test_type = "integ-test"

        validators_mock.return_value = True

        test_run_component_dict = TestRunRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "Not Available")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"], "URL not available")

    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("validators.url")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local_invalid(self, report_args_mock: MagicMock, validators_mock: MagicMock, mock_open: MagicMock, yaml_safe_load_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/mock"
        report_args_mock.test_type = "integ-test"

        validators_mock.return_value = False
        yaml_safe_load_mock.return_value = {"test_result": "PASS"}
        mock_open.side_effect = FileNotFoundError

        test_run_component_dict = TestRunRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        mock_open.assert_has_calls([call('https://ci.opensearch.org/ci/dbc/mock/test-results/123/integ-test/geospatial/with-security/geospatial.yml', 'r', encoding='utf8')])
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "Not Available")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"], "URL not available")
