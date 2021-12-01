
import logging
import os
import unittest
from unittest.mock import MagicMock, call, patch

from paths.script_finder import ScriptFinder
from test_workflow.integ_test.integ_test_suite import InvalidTestConfigError
from test_workflow.integ_test.integ_test_suite_opensearch_dashboards import IntegTestSuiteOpenSearchDashboards
from test_workflow.integ_test.local_test_cluster_opensearch_dashboards import LocalTestClusterOpenSearchDashboards


class TestIntegSuiteOpenSearchDashboards(unittest.TestCase):

    def setUp(self):
        self.dependency_installer_opensearch = MagicMock()
        self.dependency_installer_opensearch_dashboards = MagicMock()

        self.component = MagicMock()
        self.component.name = "sql"

        self.test_config = MagicMock()
        self.test_config.working_directory = "test_working_directory"
        self.test_config.integ_test = {"test-configs": ['with-security', 'without-security']}

        self.bundle_manifest_opensearch = MagicMock()
        self.bundle_manifest_opensearch.build.version = "1.2.0"

        self.bundle_manifest_opensearch_dashboards = MagicMock()
        self.build_manifest_opensearch = MagicMock()
        self.build_manifest_opensearch_dashboards = MagicMock()
        self.work_dir = "test_dir"

        self.test_recorder = MagicMock()
        self.save_logs = MagicMock()
        self.test_recorder.test_results_logs = self.save_logs

    @patch("os.chdir")
    @patch("os.path.exists")
    @patch("test_workflow.integ_test.integ_test_suite.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite.walk")
    @patch("test_workflow.integ_test.integ_test_suite.GitRepository")
    @patch("test_workflow.integ_test.integ_test_suite.execute", return_value=True)
    def test_execute_tests(self, mock_execute, mock_git, mock_walk, mock_test_result_data, mock_path_exists, mock_chdir):

        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find

        mock_git_object = MagicMock()
        mock_git_object.dir = "https://test.github.com"
        mock_git.return_value = mock_git_object

        mock_execute.return_value = ("test_status", "test_stdout", "")

        mock_walk_results = MagicMock()
        mock_walk.return_value = mock_walk_results

        mock_test_result_data_object = MagicMock()
        mock_test_result_data.return_value = mock_test_result_data_object

        mock_path_exists.return_value = True

        mock_create = MagicMock()
        mock_create.return_value.__enter__.return_value = ("test_endpoint", 1234)
        LocalTestClusterOpenSearchDashboards.create = mock_create

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

        mock_execute_integtest_sh = MagicMock()
        suite.execute_integtest_sh = mock_execute_integtest_sh

        # call the test target
        suite.execute_tests()

        mock_execute_integtest_sh.assert_has_calls([
            call("test_endpoint", 1234, True, "with-security"),
            call("test_endpoint", 1234, False, "without-security")
        ])

    # test base class

    @patch("os.path.exists")
    @patch("test_workflow.integ_test.integ_test_suite.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite.walk")
    @patch("test_workflow.integ_test.integ_test_suite.GitRepository")
    @patch("test_workflow.integ_test.integ_test_suite.execute", return_value=True)
    def test_execute_integtest_sh(self, mock_execute, mock_git, mock_walk, mock_test_result_data, mock_path_exists):
        logging.info(locals())

        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find

        mock_git_object = MagicMock()
        mock_git_object.dir = "dir"
        mock_git.return_value = mock_git_object

        mock_execute.return_value = ("test_status", "test_stdout", "")

        mock_walk_results = MagicMock()
        mock_walk.return_value = mock_walk_results

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

        # call the test target
        status = suite.execute_integtest_sh("test_endpoint", 1234, True, ["with-security", "without-security"])

        self.assertEqual(status, "test_status")
        mock_execute.assert_called_once_with('./integtest.sh -b test_endpoint -p 1234 -s true -v 1.2.0',
                                             os.path.join("dir", "test_working_directory"), True, False)
        mock_test_result_data.assert_called_once_with('sql', ['with-security', 'without-security'], 'test_status', 'test_stdout', '', mock_walk_results)
        self.save_logs.save_test_result_data.assert_called_once_with(mock_test_result_data_object)

    @patch("os.path.exists")
    @patch("test_workflow.integ_test.integ_test_suite.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite.walk")
    @patch("test_workflow.integ_test.integ_test_suite.GitRepository")
    @patch("test_workflow.integ_test.integ_test_suite.execute", return_value=True)
    def test_execute_integtest_sh_script_do_not_exist(self, mock_execute, mock_git, mock_walk, mock_test_result_data, mock_path_exists):
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find

        mock_git_object = MagicMock()
        mock_git_object.dir = "https://test.github.com"
        mock_git.return_value = mock_git_object

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

        # call the test target
        status = suite.execute_integtest_sh("test_endpoint", 1234, True, ["with-security", "without-security"])

        self.assertIsNone(status)

        mock_execute.assert_not_called()
        mock_test_result_data.assert_not_called()
        self.save_logs.assert_not_called()

    @patch("os.path.exists")
    @patch("test_workflow.integ_test.integ_test_suite.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite.walk")
    @patch("test_workflow.integ_test.integ_test_suite.GitRepository")
    @patch("test_workflow.integ_test.integ_test_suite.execute", return_value=True)
    def test_is_security_enabled(self, mock_execute, mock_git, mock_walk, mock_test_result_data, mock_path_exists):
        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find

        mock_git_object = MagicMock()
        mock_git_object.dir = "https://test.github.com"
        mock_git.return_value = mock_git_object

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

        self.assertTrue(suite.is_security_enabled("with-security"))
        self.assertFalse(suite.is_security_enabled("without-security"))

        with self.assertRaises(InvalidTestConfigError) as ctx:
            suite.is_security_enabled("random-config")

        self.assertEqual(str(ctx.exception), "Unsupported test config: random-config")

    @patch("test_workflow.integ_test.integ_test_suite.logging")
    @patch("os.path.exists")
    @patch("test_workflow.integ_test.integ_test_suite.TestResultData")
    @patch("test_workflow.integ_test.integ_test_suite.walk")
    @patch("test_workflow.integ_test.integ_test_suite.GitRepository")
    @patch("test_workflow.integ_test.integ_test_suite.execute", return_value=True)
    def test_pretty_print_message(self, mock_execute, mock_git, mock_walk, mock_test_result_data, mock_path_exists, mock_logging):

        mock_find = MagicMock()
        mock_find.return_value = "./integtest.sh"

        ScriptFinder.find_integ_test_script = mock_find

        mock_git_object = MagicMock()
        mock_git_object.dir = "https://test.github.com"
        mock_git.return_value = mock_git_object

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

        suite.pretty_print_message("test_message")

        mock_logging.info.assert_has_calls([
            call("==============================================="),
            call("test_message"),
            call("==============================================="),
        ])
