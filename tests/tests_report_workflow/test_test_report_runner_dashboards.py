# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from unittest.mock import MagicMock, patch

from manifests.test_manifest import TestManifest
from report_workflow.test_report_runner import TestReportRunner
from system.temporary_directory import TemporaryDirectory


class TestTestReportRunnerDashboards(unittest.TestCase):
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH = os.path.join(DATA_DIR, "test-manifest-opensearch-dashboards.yml")
    TEST_MANIFEST_OPENSEARCH_DASHBOARDS = TestManifest.from_path(TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH)

    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_dashboards_init(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"
        report_args_mock.release_candidate = "100"

        test_report_runner = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS)
        test_report_runner_data = test_report_runner.update_data()
        self.assertEqual(test_report_runner.name, "opensearch-dashboards")
        self.assertEqual(test_report_runner.test_run_id, 123)
        self.assertEqual(test_report_runner.test_type, "integ-test")
        self.assertEqual(test_report_runner.test_manifest_path, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH)
        self.assertEqual(test_report_runner_data["version"], "1.3.18")
        self.assertEqual(test_report_runner_data["platform"], "linux")
        self.assertEqual(test_report_runner_data["architecture"], "x64")
        self.assertEqual(test_report_runner_data["distribution"], "tar")
        self.assertEqual(test_report_runner_data["id"], "7791")
        self.assertEqual(test_report_runner_data["rc"], "100")
        self.assertEqual(test_report_runner_data["components"][3]["repository"], "https://github.com/opensearch-project/alerting-dashboards-plugin.git")

    @patch("report_workflow.report_args.ReportArgs")
    def test_generate_file(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"
        report_args_mock.release_candidate = "100"

        test_report_runner = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS)
        test_report_runner_data = test_report_runner.update_data()

        with TemporaryDirectory() as path:
            output_path = os.path.join(path.name, "test-report.yml")
            test_report_runner.generate_report(test_report_runner_data, path.name)
            self.assertTrue(os.path.isfile(output_path))

    @patch("report_workflow.report_args.ReportArgs")
    def test_ci_group(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"
        report_args_mock.release_candidate = "100"

        test_report_runner = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS)
        test_report_runner_data = test_report_runner.update_data()

        self.assertEqual(len(test_report_runner_data["components"]), 9)
        for i in range(3):
            self.assertEqual(test_report_runner_data["components"][i]["name"], f"OpenSearch-Dashboards-ci-group-{i + 1}")
            self.assertEqual(test_report_runner_data["components"][i]["repository"], "https://github.com/opensearch-project/OpenSearch-Dashboards.git")

        for i in range(len(self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS.components.__to_dict__())):
            if self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS.components.__to_dict__()[i]["name"] == "OpenSearch-Dashboards":
                continue
            else:
                self.assertEqual(self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS.components.__to_dict__()[i]["name"],
                                 test_report_runner_data["components"][i + 2]["name"])

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url(self, report_args_mock: MagicMock, bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar"}
        report_args_mock.test_run_id = 6351
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar"
        report_args_mock.test_type = "integ-test"

        test_report_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS).component_entry("alertingDashboards")
        self.assertEqual(test_report_component_dict.get("configs")[0]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_report_component_dict.get("configs")[0]["yml"], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                              "test-results/6351/integ-test/alertingDashboards/with-security/alertingDashboards.yml")
        self.assertEqual(test_report_component_dict.get("configs")[0]["cluster_stdout"][0], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/with-security/local-cluster-logs/id-0/stdout.txt")
        self.assertEqual(test_report_component_dict.get("configs")[0]["cluster_stdout"][1], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/with-security/local-cluster-logs/id-1/stdout.txt")
        self.assertEqual(test_report_component_dict.get("configs")[0]["cluster_stderr"][0], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/with-security/local-cluster-logs/id-0/stderr.txt")
        self.assertEqual(test_report_component_dict.get("configs")[0]["cluster_stderr"][1], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/with-security/local-cluster-logs/id-1/stderr.txt")

        self.assertEqual(test_report_component_dict.get("configs")[1]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_report_component_dict.get("configs")[1]["yml"], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                              "test-results/6351/integ-test/alertingDashboards/without-security/alertingDashboards.yml")
        self.assertEqual(test_report_component_dict.get("configs")[1]["cluster_stdout"][0], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/without-security/local-cluster-logs/id-2/stdout.txt")
        self.assertEqual(test_report_component_dict.get("configs")[1]["cluster_stdout"][1], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/without-security/local-cluster-logs/id-3/stdout.txt")
        self.assertEqual(test_report_component_dict.get("configs")[1]["cluster_stderr"][0], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/without-security/local-cluster-logs/id-2/stderr.txt")
        self.assertEqual(test_report_component_dict.get("configs")[1]["cluster_stderr"][1], "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar/"
                                                                                            "test-results/6351/integ-test/alertingDashboards/without-security/local-cluster-logs/id-3/stderr.txt")

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url_failed_test(self, report_args_mock: MagicMock, bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar"}
        report_args_mock.test_run_id = 6351
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/2.17.0/7921/linux/x64/tar"
        report_args_mock.test_type = "integ-test"

        test_report_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS).component_entry("alertingDashboards")
        self.assertEqual(test_report_component_dict.get("configs")[0]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_report_component_dict.get("configs")[0]["failed_test"][0], "acknowledge_alerts_modal_spec.js#AcknowledgeAlertsModal "
                                                                                         "\"before all\" hook for \"Acknowledge button disabled when more than 1 trigger selected\"")

        self.assertEqual(test_report_component_dict.get("configs")[1]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_report_component_dict.get("configs")[1]["failed_test"][1], "alert_spec.js#Alerts can be in 'Active' state "
                                                                                         "\"before each\" hook for \"after the monitor starts running\"")

    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": self.DATA_DIR}
        report_args_mock.test_run_id = 123123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"

        test_report_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS).component_entry("indexManagementDashboards")
        self.assertEqual(test_report_component_dict.get("configs")[0]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_report_component_dict.get("configs")[0]["yml"],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "with-security", "indexManagementDashboards.yml"))
        self.assertEqual(test_report_component_dict.get("configs")[0]["cluster_stdout"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "with-security", "local-cluster-logs", "id-0", "stdout.txt"))
        self.assertEqual(test_report_component_dict.get("configs")[0]["cluster_stderr"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "with-security", "local-cluster-logs", "id-0", "stderr.txt"))
        self.assertEqual(test_report_component_dict.get("configs")[0]["test_stdout"],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "with-security", "stdout.txt"))
        self.assertEqual(test_report_component_dict.get("configs")[1]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_report_component_dict.get("configs")[1]["yml"],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "without-security", "indexManagementDashboards.yml"))
        self.assertEqual(test_report_component_dict.get("configs")[1]["cluster_stdout"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "without-security", "local-cluster-logs", "id-2", "stdout.txt"))
        self.assertEqual(test_report_component_dict.get("configs")[1]["cluster_stderr"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "without-security", "local-cluster-logs", "id-2", "stderr.txt"))
        self.assertEqual(test_report_component_dict.get("configs")[1]["test_stdout"],
                         os.path.join(self.DATA_DIR, "test-results", "123123", "integ-test", "indexManagementDashboards", "without-security", "stdout.txt"))

    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local_failed_test(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH
        report_args_mock.artifact_paths = {"opensearch-dashboards": self.DATA_DIR}
        report_args_mock.test_run_id = 123123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"

        test_report_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS).component_entry("indexManagementDashboards")
        self.assertEqual(test_report_component_dict.get("configs")[0]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_report_component_dict.get("configs")[0]["failed_test"][0], "aliases.js#Aliases can be "
                                                                                         "searched / sorted / paginated \"before each\" hook for \"successfully\"")

        self.assertEqual(test_report_component_dict.get("configs")[1]["status"], "FAIL")
        self.assertEqual(test_report_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_report_component_dict.get("configs")[1]["failed_test"][1], "create_index.js#Create Index "
                                                                                         "can be created and updated \"before each\" hook for \"Create a index successfully\"")
