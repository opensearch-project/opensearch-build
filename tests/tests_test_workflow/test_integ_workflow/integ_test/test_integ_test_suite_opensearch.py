# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from pathlib import Path
from typing import Any, Tuple
from unittest.mock import MagicMock, Mock, call, patch

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleComponent, BundleManifest
from manifests.test_manifest import TestComponent, TestManifest
from test_workflow.integ_test.integ_test_suite_opensearch import IntegTestSuiteOpenSearch, InvalidTestConfigError, ScriptFinder, Topology


@patch("os.makedirs")
@patch("os.chdir")
@patch.object(GitRepository, "__checkout__")
class TestIntegSuiteOpenSearch(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "build_manifest.yml")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")
    TEST_MANIFEST = os.path.join(DATA, "test_manifest.yml")

    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.bundle_manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.build_manifest = BuildManifest.from_path(self.BUILD_MANIFEST)
        self.test_manifest = TestManifest.from_path(self.TEST_MANIFEST)
        self.work_dir = Path("test_dir")

    @patch("os.path.exists", return_value=True)
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.IntegTestSuiteOpenSearch.multi_execute_integtest_sh")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.Topology")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_multiple_test_configs(self, mock_test_recorder: Mock, mock_topology: Mock, mock_multi_execute_integtest_sh: Mock, *mock: Any) -> None:
        test_config, component = self.__get_test_config_and_bundle_component("job-scheduler")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer,
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            self.work_dir,
            mock_test_recorder
        )
        mock_topology.create().__enter__.return_value = [{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}]
        mock_multi_execute_integtest_sh.return_value = "success"

        test_results = integ_test_suite.execute_tests()
        self.assertEqual(len(test_results), 2)
        self.assertTrue(test_results.failed)

        mock_multi_execute_integtest_sh.assert_has_calls([
            call([{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}], True, "with-security"),
            call([{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}], False, "without-security")
        ])

    @patch("test_workflow.integ_test.integ_test_suite_opensearch.IntegTestSuiteOpenSearch.multi_execute_integtest_sh")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.Topology")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_build_dependencies(self, mock_test_recorder: Mock, mock_topology: Mock, mock_multi_execute_integtest_sh: Mock, *mock: Any) -> None:
        dependency_installer = MagicMock()
        test_config, component = self.__get_test_config_and_bundle_component("index-management")
        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer,
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            self.work_dir,
            mock_test_recorder
        )

        mock_topology.create().__enter__.return_value = [{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}]

        mock_multi_execute_integtest_sh.return_value = "success"

        integ_test_suite.execute_tests()
        dependency_installer.install_build_dependencies.assert_called_with(
            {"opensearch-job-scheduler": "1.1.0.0"}, os.path.join(self.work_dir, "index-management", "src", "test", "resources", "job-scheduler")
        )

        mock_multi_execute_integtest_sh.assert_has_calls([call(
            [{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}], False, "without-security")]
        )

    @patch("test_workflow.integ_test.integ_test_suite_opensearch.IntegTestSuiteOpenSearch.multi_execute_integtest_sh")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.execute")
    def test_execute_without_build_dependencies(self, mock_execute: Mock, *mock: Any) -> None:
        dependency_installer = MagicMock()
        test_config, component = self.__get_test_config_and_bundle_component("job-scheduler")
        mock_test_recorder = MagicMock()
        mock_test_results_logs = MagicMock()
        mock_test_recorder.test_results_logs.return_value = mock_test_results_logs

        mock_create = MagicMock()
        mock_create.return_value.__enter__.return_value = [{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "test", "port": 1234, "transport": 4321}], "cluster_manager_nodes": []}]

        Topology.create = mock_create  # type: ignore

        mock_execute.return_value = ("test_status", "test_stdout", "")

        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer,
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            self.work_dir,
            mock_test_recorder)

        integ_test_suite.execute_tests()

        dependency_installer.install_build_dependencies.assert_not_called()

    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_unsupported_build_dependencies(self, mock_test_recorder: Mock, *mock: Any) -> None:
        dependency_installer = MagicMock()
        test_config, component = self.__get_test_config_and_bundle_component("anomaly-detection")
        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer,
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            self.work_dir,
            mock_test_recorder
        )
        with self.assertRaises(InvalidTestConfigError):
            integ_test_suite.execute_tests()
        dependency_installer.install_build_dependencies.assert_not_called()

    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_missing_job_scheduler(self, mock_test_recorder: Mock, mock_install_build_dependencies: Mock, *mock: Any) -> None:
        invalid_build_manifest = BuildManifest.from_path("data/build_manifest_missing_components.yml")
        test_config, component = self.__get_test_config_and_bundle_component("index-management")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer, component, test_config, self.bundle_manifest, invalid_build_manifest, self.work_dir, mock_test_recorder
        )
        with self.assertRaises(KeyError) as ctx:
            integ_test_suite.execute_tests()

        self.assertEqual(str(ctx.exception), "'job-scheduler'")
        dependency_installer.install_build_dependencies.assert_not_called()

    def __get_test_config_and_bundle_component(self, component_name: str) -> Tuple[TestComponent, BundleComponent]:
        component = self.bundle_manifest.components[component_name]
        test_config = self.test_manifest.components[component.name]
        return test_config, component

    @patch("os.path.exists", return_value=True)
    @patch.object(ScriptFinder, "find_integ_test_script")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.IntegTestSuiteOpenSearch.multi_execute_integtest_sh")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.Topology")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_working_directory(self, mock_test_recorder: Mock, mock_topology: Mock, mock_multi_execute_integtest_sh: Mock, mock_script_finder: Mock, *mock: Any) -> None:
        test_config, component = self.__get_test_config_and_bundle_component("dashboards-reports")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer,
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            self.work_dir,
            mock_test_recorder
        )

        mock_topology.create().__enter__.return_value = [{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}]
        mock_script_finder.return_value = "integtest.sh"

        mock_multi_execute_integtest_sh.return_value = "success"

        integ_test_suite.execute_tests()  # type: ignore

        mock_multi_execute_integtest_sh.assert_called_with(
            [{"cluster_name": "cluster1", "data_nodes": [{"endpoint": "localhost", "port": 9200, "transport": 9300}], "cluster_manager_nodes": []}],
            True,
            "with-security"
        )

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch.execute", return_value=True)
    def test_multi_execute_integtest_sh(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock,
                                        mock_test_recorder: Mock, mock_makedirs: Mock, mock_path_exists: Mock, *mock: Any) -> None:
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_execute.return_value = ("test_status", "test_stdout", "")

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object
        mock_path_exists.return_value = True

        test_config, component = self.__get_test_config_and_bundle_component("job-scheduler")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuiteOpenSearch(
            dependency_installer,
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            self.work_dir,
            mock_test_recorder
        )

        self.assertEqual(integ_test_suite.repo.url, "https://github.com/opensearch-project/job-scheduler.git")
        self.assertEqual(integ_test_suite.repo.ref, "4504dabfc67dd5628c1451e91e9a1c3c4ca71525")
        integ_test_suite.repo.dir = "dir"

        # call the test target
        mock_endpoint = MagicMock()
        status = integ_test_suite.multi_execute_integtest_sh([mock_endpoint], True, "with-security")

        mock_find.assert_called()
        self.assertEqual(status, "test_status")
        mock_execute.assert_called()

        mock_test_result_data.assert_called_once_with(
            "job-scheduler",
            "with-security",
            "test_status",
            "test_stdout",
            "",
            {
                "opensearch-integ-test": os.path.join("dir", "build", "reports", "tests", "integTest")
            }
        )

        assert(mock_test_result_data.return_value in integ_test_suite.result_data)
        self.assertEqual(integ_test_suite.additional_cluster_config, None)
