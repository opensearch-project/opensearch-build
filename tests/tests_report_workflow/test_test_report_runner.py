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
from report_workflow.test_report_runner import TestReportRunner
from system.temporary_directory import TemporaryDirectory


class TestTestReportRunner(unittest.TestCase):
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    TEST_MANIFEST_PATH = os.path.join(DATA_DIR, "test_manifest.yml")
    TEST_MANIFEST = TestManifest.from_path(TEST_MANIFEST_PATH)

    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_init(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"
        report_args_mock.release_candidate = "100"

        test_run_runner = TestReportRunner(report_args_mock, self.TEST_MANIFEST)
        test_run_runner_data = test_run_runner.update_data()
        self.assertEqual(test_run_runner.name, "opensearch")
        self.assertEqual(test_run_runner.test_run_id, 123)
        self.assertEqual(test_run_runner.test_type, "integ-test")
        self.assertEqual(test_run_runner.test_manifest_path, self.TEST_MANIFEST_PATH)
        self.assertEqual(test_run_runner_data["version"], "2.15.0")
        self.assertEqual(test_run_runner_data["platform"], "linux")
        self.assertEqual(test_run_runner_data["architecture"], "x64")
        self.assertEqual(test_run_runner_data["distribution"], "tar")
        self.assertEqual(test_run_runner_data["id"], "9992")
        self.assertEqual(test_run_runner_data["rc"], "100")
        self.assertEqual(test_run_runner_data["components"][3]["repository"], "https://github.com/opensearch-project/cross-cluster-replication.git")

    @patch("report_workflow.report_args.ReportArgs")
    def test_generate_file(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"
        report_args_mock.release_candidate = "100"

        test_run_runner = TestReportRunner(report_args_mock, self.TEST_MANIFEST)
        test_run_runner_data = test_run_runner.update_data()

        with TemporaryDirectory() as path:
            output_path = os.path.join(path.name, "test-report.yml")
            test_run_runner.generate_report(test_run_runner_data, path.name)
            self.assertTrue(os.path.isfile(output_path))

    @patch("report_workflow.report_args.ReportArgs")
    def test_update_data_skip_component(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"
        report_args_mock.release_candidate = "100"

        test_report_runner = TestReportRunner(report_args_mock, self.TEST_MANIFEST)
        test_report_runner_data = test_report_runner.update_data()

        self.assertFalse("opensearch-system-templates" in test_report_runner.bundle_components_list)
        self.assertEqual(len(test_report_runner_data["components"]), 6)

        for i in range(len(self.TEST_MANIFEST.components.__to_dict__())):
            if self.TEST_MANIFEST.components.__to_dict__()[i]["name"] == "opensearch-system-templates":
                self.assertEqual(i, len(self.TEST_MANIFEST.components) - 1)
            else:
                self.assertEqual(self.TEST_MANIFEST.components.__to_dict__()[i]["name"], test_report_runner_data["components"][i]["name"])

    @patch("report_workflow.report_args.ReportArgs")
    @patch("manifests.test_manifest.TestManifest")
    def test_runner_update_test_run_data_local(self, report_args_mock: MagicMock,
                                               test_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"

        test_run_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).update_test_run_data()
        self.assertEqual(test_run_dict.get("Command"), " ".join(
            ["./test.sh", "integ-test", self.TEST_MANIFEST_PATH, "--paths", f"opensearch={self.DATA_DIR}"]))
        self.assertEqual(test_run_dict.get("TestType"), "integ-test")
        self.assertEqual(test_run_dict.get("TestManifest"), self.TEST_MANIFEST_PATH)
        self.assertEqual(test_run_dict.get("DistributionManifest"),
                         os.path.join(self.DATA_DIR, "dist", "opensearch", "manifest.yml"))
        self.assertEqual(test_run_dict.get("TestID"), "123")

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("report_workflow.report_args.ReportArgs")
    @patch("manifests.test_manifest.TestManifest")
    def test_runner_update_test_run_data_url(self, report_args_mock: MagicMock, test_manifest_mock: MagicMock,
                                             bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "https://foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.test_type = "integ-test"

        test_run_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).update_test_run_data()
        self.assertEqual(test_run_dict.get("Command"), " ".join(
            ["./test.sh", "integ-test", self.TEST_MANIFEST_PATH, "--paths", "opensearch=https://foo/bar"]))
        self.assertEqual(test_run_dict.get("TestType"), "integ-test")
        self.assertEqual(test_run_dict.get("TestManifest"), self.TEST_MANIFEST_PATH)
        self.assertEqual(test_run_dict.get("DistributionManifest"),
                         "/".join(["https://foo/bar", "dist", "opensearch", "manifest.yml"]))
        self.assertEqual(test_run_dict.get("TestID"), "123")

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url(self, report_args_mock: MagicMock,
                                        bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.15.0/9971/windows/x64/zip"}
        report_args_mock.test_run_id = 8303
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip"
        report_args_mock.test_type = "integ-test"

        test_run_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "PASS")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"],
                         "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip/test-results/8303/integ-test/geospatial/with-security/geospatial.yml")
        self.assertEqual(test_run_component_dict.get("configs")[0]["test_stdout"], "https://ci.opensearch.org/ci/dbc/integ-test/"
                                                                                   "2.15.0/9971/windows/x64/zip/test-results/8303/integ-test/geospatial/with-security/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[0]["test_stderr"], "https://ci.opensearch.org/ci/dbc/integ-test/"
                                                                                   "2.15.0/9971/windows/x64/zip/test-results/8303/integ-test/geospatial/with-security/stderr.txt")
        self.assertEqual(test_run_component_dict.get("configs")[0]["cluster_stdout"][0], "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip/"
                                                                                         "test-results/8303/integ-test/geospatial/with-security/local-cluster-logs/id-0/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[0]["cluster_stderr"][0], "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip/"
                                                                                         "test-results/8303/integ-test/geospatial/with-security/local-cluster-logs/id-0/stderr.txt")
        self.assertEqual(test_run_component_dict.get("configs")[0]["failed_test"][0], "No Failed Test")
        self.assertEqual(test_run_component_dict.get("configs")[1]["status"], "PASS")
        self.assertEqual(test_run_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_run_component_dict.get("configs")[1]["test_stdout"], "https://ci.opensearch.org/ci/dbc/integ-test/"
                                                                                   "2.15.0/9971/windows/x64/zip/test-results/8303/integ-test/geospatial/without-security/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["test_stderr"], "https://ci.opensearch.org/ci/dbc/integ-test/"
                                                                                   "2.15.0/9971/windows/x64/zip/test-results/8303/integ-test/geospatial/without-security/stderr.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["cluster_stdout"][0], "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip/"
                                                                                         "test-results/8303/integ-test/geospatial/without-security/local-cluster-logs/id-1/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["cluster_stderr"][0], "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip/"
                                                                                         "test-results/8303/integ-test/geospatial/without-security/local-cluster-logs/id-1/stderr.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["failed_test"][0], "No Failed Test")

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url_failed_test(self, report_args_mock: MagicMock,
                                                    bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.15.0/9971/windows/x64/zip"}
        report_args_mock.test_run_id = 8303
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/integ-test/2.15.0/9971/windows/x64/zip"
        report_args_mock.test_type = "integ-test"

        test_run_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).component_entry("index-management")
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "FAIL")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["failed_test"][0], "org.opensearch.indexmanagement.indexstatemanagement.action.CloseActionIT#test already closed index")
        self.assertEqual(test_run_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_run_component_dict.get("configs")[1]["failed_test"][0], "org.opensearch.indexmanagement.IndexManagementIndicesIT#test update management index history "
                                                                                      "mappings with new schema version")

    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"

        test_run_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "PASS")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "with-security", "geospatial.yml"))
        self.assertEqual(test_run_component_dict.get("configs")[0]["cluster_stdout"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "with-security", "local-cluster-logs", "id-0", "stdout.txt"))
        self.assertEqual(test_run_component_dict.get("configs")[0]["cluster_stderr"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "with-security", "local-cluster-logs", "id-0", "stderr.txt"))
        self.assertEqual(test_run_component_dict.get("configs")[0]["test_stdout"],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "with-security", "stdout.txt"))
        self.assertEqual(test_run_component_dict.get("configs")[0]["failed_test"][0], "No Failed Test")
        self.assertEqual(test_run_component_dict.get("configs")[1]["status"], "PASS")
        self.assertEqual(test_run_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_run_component_dict.get("configs")[1]["yml"],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "without-security", "geospatial.yml"))
        self.assertEqual(test_run_component_dict.get("configs")[1]["cluster_stdout"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "without-security", "local-cluster-logs", "id-1", "stdout.txt"))
        self.assertEqual(test_run_component_dict.get("configs")[1]["cluster_stderr"][0],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "without-security", "local-cluster-logs", "id-1", "stderr.txt"))
        self.assertEqual(test_run_component_dict.get("configs")[1]["test_stdout"],
                         os.path.join(self.DATA_DIR, "test-results", "123", "integ-test", "geospatial", "without-security", "stdout.txt"))
        self.assertEqual(test_run_component_dict.get("configs")[1]["failed_test"][0], "No Failed Test")

    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local_failed_test(self, report_args_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": self.DATA_DIR}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = self.DATA_DIR
        report_args_mock.test_type = "integ-test"

        test_run_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).component_entry("index-management")
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "FAIL")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["failed_test"][0], "org.opensearch.indexmanagement.indexstatemanagement.action.CloseActionIT#test already closed index")
        self.assertEqual(test_run_component_dict.get("configs")[1]["name"], "without-security")
        self.assertEqual(test_run_component_dict.get("configs")[1]["failed_test"][0], "org.opensearch.indexmanagement.IndexManagementIndicesIT#test update management index history "
                                                                                      "mappings with new schema version")

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("yaml.safe_load")
    @patch("validators.url")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_url_invalid(self, report_args_mock: MagicMock, validators_mock: MagicMock,
                                                yaml_safe_load_mock: MagicMock, bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/mock"
        report_args_mock.test_type = "integ-test"

        validators_mock.return_value = True

        test_run_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "Not Available")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"], "URL not available")
        self.assertEqual(test_run_component_dict.get("configs")[0]["test_stdout"], "https://ci.opensearch.org/ci"
                                                                                   "/dbc/mock/test-results/123/integ-test/geospatial/with-security/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["test_stdout"], "https://ci.opensearch.org/ci"
                                                                                   "/dbc/mock/test-results/123/integ-test/geospatial/without-security/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[0]["cluster_stdout"][0], "https://ci.opensearch.org/ci"
                                                                                         "/dbc/mock/test-results/123/integ-test/geospatial/with-security/local-cluster-logs/id-0/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["cluster_stdout"][0], "https://ci.opensearch.org/ci"
                                                                                         "/dbc/mock/test-results/123/integ-test/geospatial/without-security/local-cluster-logs/id-1/stdout.txt")

    @patch("manifests.bundle_manifest.BundleManifest.from_urlpath")
    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("validators.url")
    @patch("report_workflow.report_args.ReportArgs")
    def test_runner_component_entry_local_invalid(self, report_args_mock: MagicMock, validators_mock: MagicMock,
                                                  mock_open: MagicMock, yaml_safe_load_mock: MagicMock,
                                                  bundle_manifest_mock: MagicMock) -> None:
        report_args_mock.test_manifest_path = self.TEST_MANIFEST_PATH
        report_args_mock.artifact_paths = {"opensearch": "foo/bar"}
        report_args_mock.test_run_id = 123
        report_args_mock.base_path = "https://ci.opensearch.org/ci/dbc/mock"
        report_args_mock.test_type = "integ-test"

        validators_mock.return_value = False
        yaml_safe_load_mock.return_value = {"test_result": "PASS"}
        mock_open.side_effect = FileNotFoundError

        test_run_component_dict = TestReportRunner(report_args_mock, self.TEST_MANIFEST).component_entry("geospatial")
        mock_open.assert_has_calls([call(
            'https://ci.opensearch.org/ci/dbc/mock/test-results/123/integ-test/geospatial/with-security/geospatial.yml',
            'r', encoding='utf8')])
        self.assertEqual(test_run_component_dict.get("configs")[0]["status"], "Not Available")
        self.assertEqual(test_run_component_dict.get("configs")[0]["name"], "with-security")
        self.assertEqual(test_run_component_dict.get("configs")[0]["yml"], "URL not available")
        self.assertEqual(test_run_component_dict.get("configs")[0]["test_stdout"], "https://ci.opensearch.org/ci"
                                                                                   "/dbc/mock/test-results/123/integ-test/geospatial/with-security/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["test_stdout"], "https://ci.opensearch.org/ci"
                                                                                   "/dbc/mock/test-results/123/integ-test/geospatial/without-security/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[0]["cluster_stdout"][0], "https://ci.opensearch.org/ci"
                                                                                         "/dbc/mock/test-results/123/integ-test/geospatial/with-security/local-cluster-logs/id-0/stdout.txt")
        self.assertEqual(test_run_component_dict.get("configs")[1]["cluster_stdout"][0], "https://ci.opensearch.org/ci"
                                                                                         "/dbc/mock/test-results/123/integ-test/geospatial/without-security/local-cluster-logs/id-1/stdout.txt")
