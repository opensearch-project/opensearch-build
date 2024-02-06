# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from paths.script_finder import ScriptFinder
from test_workflow.integ_test.integ_test_suite import InvalidTestConfigError
from test_workflow.integ_test.integ_test_suite_opensearch_dashboards import IntegTestSuiteOpenSearchDashboards
from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards


class TestIntegSuiteOpenSearchDashboards(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST_OSD = os.path.join(DATA, "bundle_manifest_osd.yml")
    BUILD_MANIFEST = os.path.join(DATA, "build_manifest.yml")
    BUILD_MANIFEST_OSD = os.path.join(DATA, "build_manifest_osd.yml")

    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.dependency_installer_opensearch = MagicMock()
        self.dependency_installer_opensearch_dashboards = MagicMock()

        self.component = MagicMock()
        self.component.name = "sql"

        self.test_config = MagicMock()
        self.test_config.working_directory = "test_working_directory"
        self.test_config.integ_test = {"test-configs": ['with-security', 'without-security']}

        self.test_config_additional_config = MagicMock()
        self.test_config_additional_config.working_directory = "test_working_directory"
        self.test_config_additional_config.integ_test = {"test-configs": ['with-security', 'without-security'], "additional-cluster-configs": {'server.host': '0.0.0.0'}}

        self.bundle_manifest_opensearch = MagicMock()
        self.bundle_manifest_opensearch.build.version = "1.2.0"

        self.bundle_manifest_opensearch_dashboards = BundleManifest.from_path(self.BUNDLE_MANIFEST_OSD)
        self.build_manifest_opensearch = BuildManifest.from_path(self.BUILD_MANIFEST)
        self.build_manifest_opensearch_dashboards = BuildManifest.from_path(self.BUILD_MANIFEST_OSD)
        self.work_dir = Path("test_dir")

        self.test_recorder = MagicMock()
        self.save_logs = MagicMock()
        self.test_recorder.test_results_logs = self.save_logs

    @patch("os.chdir")
    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.execute", return_value=True)
    def test_execute_tests(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock, mock_makedirs: Mock, mock_path_exists: Mock, mock_chdir: Mock) -> None:
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_execute.return_value = ("test_status", "test_stdout", "")

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        mock_path_exists.return_value = True

        mock_create = MagicMock()
        mock_create.return_value.__enter__.return_value = ("test_endpoint", 1234)
        LocalTestClusterOpenSearchDashboards.create = mock_create  # type: ignore

        suite = IntegTestSuiteOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.component,
            self.test_config,
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            self.build_manifest_opensearch,
            self.build_manifest_opensearch_dashboards,
            self.work_dir,
            self.test_recorder
        )

        self.assertEqual(suite.repo.url, "https://github.com/opensearch-project/opensearch-dashboards-functional-test.git")
        self.assertEqual(suite.repo.ref, "2.x")

        mock_execute_integtest_sh = MagicMock()
        suite.execute_integtest_sh = mock_execute_integtest_sh  # type: ignore

        # call the test target
        suite.execute_tests()

        mock_execute_integtest_sh.assert_has_calls([
            call("test_endpoint", 1234, True, "with-security"),
            call("test_endpoint", 1234, False, "without-security")
        ])

        self.assertEqual(str(suite.additional_cluster_config), "{}")

    @patch("os.chdir")
    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.execute", return_value=True)
    def test_execute_tests_additional_config(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock, mock_makedirs: Mock, mock_path_exists: Mock, mock_chdir: Mock) -> None:
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_execute.return_value = ("test_status", "test_stdout", "")

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        mock_path_exists.return_value = True

        mock_create = MagicMock()
        mock_create.return_value.__enter__.return_value = ("test_endpoint", 1234)
        LocalTestClusterOpenSearchDashboards.create = mock_create  # type: ignore

        suite = IntegTestSuiteOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.component,
            self.test_config_additional_config,
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            self.build_manifest_opensearch,
            self.build_manifest_opensearch_dashboards,
            self.work_dir,
            self.test_recorder
        )

        self.assertEqual(suite.repo.url, "https://github.com/opensearch-project/opensearch-dashboards-functional-test.git")
        self.assertEqual(suite.repo.ref, "2.x")

        mock_execute_integtest_sh = MagicMock()
        suite.execute_integtest_sh = mock_execute_integtest_sh  # type: ignore

        # call the test target
        suite.execute_tests()

        mock_execute_integtest_sh.assert_has_calls([
            call("test_endpoint", 1234, True, "with-security"),
            call("test_endpoint", 1234, False, "without-security")
        ])

        self.assertEqual(str(suite.additional_cluster_config), "{'server.host': '0.0.0.0'}")

    # test base class

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.execute", return_value=True)
    def test_execute_integtest_sh(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock, mock_makedirs: Mock, mock_path_exists: Mock) -> None:
        logging.info(locals())

        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_execute.return_value = ("test_status", "test_stdout", "")

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        mock_path_exists.return_value = True

        suite = IntegTestSuiteOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.component,
            self.test_config,
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            self.build_manifest_opensearch,
            self.build_manifest_opensearch_dashboards,
            self.work_dir,
            self.test_recorder
        )

        self.assertEqual(suite.repo.url, "https://github.com/opensearch-project/opensearch-dashboards-functional-test.git")
        self.assertEqual(suite.repo.ref, "2.x")
        suite.repo.dir = "dir"

        # call the test target
        status = suite.execute_integtest_sh("test_endpoint", 1234, True, "with-security")

        self.assertEqual(status, "test_status")
        mock_execute.assert_called_once_with('bash ./integtest.sh -b test_endpoint -p 1234 -s true -t sql -v 1.2.0 -o default -r false', os.path.join("dir", "test_working_directory"), True, False)

        mock_test_result_data.assert_called_once_with(
            "sql",
            "with-security",
            "test_status",
            "test_stdout",
            "",
            {
                "cypress-videos": os.path.join("dir", "test_working_directory", "cypress", "videos"),
                "cypress-screenshots": os.path.join("dir", "test_working_directory", "cypress", "screenshots"),
                "cypress-report": os.path.join("dir", "test_working_directory", "cypress", "results")
            }
        )
        assert(mock_test_result_data.return_value in suite.result_data)
        self.assertEqual(suite.additional_cluster_config, None)

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.execute", return_value=True)
    def test_execute_integtest_sh_script_do_not_exist(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock, mock_makedirs: Mock, mock_path_exists: Mock) -> None:
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_path_exists.return_value = False

        suite = IntegTestSuiteOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.component,
            self.test_config,
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            self.build_manifest_opensearch,
            self.build_manifest_opensearch_dashboards,
            self.work_dir,
            self.test_recorder
        )

        self.assertEqual(suite.repo.url, "https://github.com/opensearch-project/opensearch-dashboards-functional-test.git")
        self.assertEqual(suite.repo.ref, "2.x")

        # call the test target
        status = suite.execute_integtest_sh("test_endpoint", 1234, True, "without-security")

        self.assertEqual(0, status)

        mock_execute.assert_not_called()
        mock_test_result_data.assert_not_called()
        self.save_logs.assert_not_called()
        self.assertEqual(suite.additional_cluster_config, None)

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.execute", return_value=True)
    def test_is_security_enabled(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock, mock_makedirs: Mock, mock_path_exists: Mock) -> None:
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_path_exists.return_value = False

        suite = IntegTestSuiteOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.component,
            self.test_config,
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            self.build_manifest_opensearch,
            self.build_manifest_opensearch_dashboards,
            self.work_dir,
            self.test_recorder
        )

        self.assertEqual(suite.repo.url, "https://github.com/opensearch-project/opensearch-dashboards-functional-test.git")
        self.assertEqual(suite.repo.ref, "2.x")

        self.assertTrue(suite.is_security_enabled("with-security"))
        self.assertFalse(suite.is_security_enabled("without-security"))

        with self.assertRaises(InvalidTestConfigError) as ctx:
            suite.is_security_enabled("random-config")

        self.assertEqual(str(ctx.exception), "Unsupported test config: random-config")

        self.assertEqual(suite.additional_cluster_config, None)

    @patch("test_workflow.integ_test.integ_test_suite.logging")
    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.GitRepository.__checkout__")
    @patch("test_workflow.integ_test.integ_test_suite_opensearch_dashboards.execute", return_value=True)
    def test_pretty_print_message(self, mock_execute: Mock, mock_git: Mock, mock_test_result_data: Mock, mock_makedirs: Mock, mock_path_exists: Mock, mock_logging: Mock) -> None:

        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find  # type: ignore

        mock_path_exists.return_value = False

        suite = IntegTestSuiteOpenSearchDashboards(
            self.dependency_installer_opensearch,
            self.dependency_installer_opensearch_dashboards,
            self.component,
            self.test_config,
            self.bundle_manifest_opensearch,
            self.bundle_manifest_opensearch_dashboards,
            self.build_manifest_opensearch,
            self.build_manifest_opensearch_dashboards,
            self.work_dir,
            self.test_recorder
        )

        self.assertEqual(suite.repo.url, "https://github.com/opensearch-project/opensearch-dashboards-functional-test.git")
        self.assertEqual(suite.repo.ref, "2.x")

        suite.pretty_print_message("test_message")

        mock_logging.info.assert_has_calls([
            call("==============================================="),
            call("test_message"),
            call("==============================================="),
        ])
