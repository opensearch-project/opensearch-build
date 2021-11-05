# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from test_workflow.integ_test.integ_test_suite import IntegTestSuite, InvalidTestConfigError, ScriptFinder


@patch("os.makedirs")
@patch("os.chdir")
@patch.object(GitRepository, "__checkout__")
class TestIntegSuite(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "build_manifest.yml")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")
    TEST_MANIFEST = os.path.join(DATA, "test_manifest.yml")

    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        self.bundle_manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.build_manifest = BuildManifest.from_path(self.BUILD_MANIFEST)
        self.test_manifest = TestManifest.from_path(self.TEST_MANIFEST)

    @patch("os.path.exists", return_value=True)
    @patch.object(ScriptFinder, "find_integ_test_script")
    @patch("test_workflow.integ_test.integ_test_suite.execute")
    @patch("test_workflow.integ_test.integ_test_suite.LocalTestCluster")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_multiple_test_configs(self, mock_test_recorder, mock_local_test_cluster, mock_system_execute, mock_script_finder, *mock):
        test_config, component = self.__get_test_config_and_bundle_component("job-scheduler")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuite(dependency_installer, component, test_config, self.bundle_manifest, self.build_manifest, "tmpdir", mock_test_recorder)
        mock_system_execute.return_value = 200, "success", "failure"
        mock_local_test_cluster.create().__enter__.return_value = "localhost", "9200"
        mock_script_finder.return_value = "integtest.sh"
        test_results = integ_test_suite.execute()
        self.assertEqual(len(test_results), 2)
        self.assertTrue(test_results.failed)
        mock_system_execute.assert_has_calls(
            [
                call("integtest.sh -b localhost -p 9200 -s true -v 1.1.0", os.path.join("tmpdir", "job-scheduler"), True, False),
                call("integtest.sh -b localhost -p 9200 -s false -v 1.1.0", os.path.join("tmpdir", "job-scheduler"), True, False),
            ]
        )

    @patch.object(IntegTestSuite, "_IntegTestSuite__setup_cluster_and_execute_test_config")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_build_dependencies(self, mock_test_recorder, *mock):
        dependency_installer = MagicMock()
        test_config, component = self.__get_test_config_and_bundle_component("index-management")
        integ_test_suite = IntegTestSuite(dependency_installer, component, test_config, self.bundle_manifest, self.build_manifest, "tmpdir", mock_test_recorder)
        integ_test_suite.execute()
        dependency_installer.install_build_dependencies.assert_called_with(
            {"opensearch-job-scheduler": "1.1.0.0"}, os.path.join("tmpdir", "index-management", "src", "test", "resources", "job-scheduler")
        )

    @patch.object(IntegTestSuite, "_IntegTestSuite__setup_cluster_and_execute_test_config")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_without_build_dependencies(self, mock_test_recorder, *mock):
        dependency_installer = MagicMock()
        test_config, component = self.__get_test_config_and_bundle_component("job-scheduler")
        integ_test_suite = IntegTestSuite(dependency_installer, component, test_config, self.bundle_manifest, self.build_manifest, "tmpdir", mock_test_recorder)
        integ_test_suite.execute()
        dependency_installer.install_build_dependencies.assert_not_called()

    @patch.object(IntegTestSuite, "_IntegTestSuite__setup_cluster_and_execute_test_config")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_unsupported_build_dependencies(self, mock_test_recorder, *mock):
        dependency_installer = MagicMock()
        test_config, component = self.__get_test_config_and_bundle_component("anomaly-detection")
        integ_test_suite = IntegTestSuite(dependency_installer, component, test_config, self.bundle_manifest, self.build_manifest, "tmpdir", mock_test_recorder)
        with self.assertRaises(InvalidTestConfigError):
            integ_test_suite.execute()
        dependency_installer.install_build_dependencies.assert_not_called()

    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_missing_job_scheduler(self, mock_test_recorder, mock_install_build_dependencies, *mock):
        invalid_build_manifest = BuildManifest.from_path("data/build_manifest_missing_components.yml")
        test_config, component = self.__get_test_config_and_bundle_component("index-management")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuite(
            dependency_installer, component, test_config, self.bundle_manifest, invalid_build_manifest, "tmpdir", mock_test_recorder
        )
        with self.assertRaises(KeyError) as ctx:
            integ_test_suite.execute()

        self.assertEqual(str(ctx.exception), "'job-scheduler'")
        dependency_installer.install_build_dependencies.assert_not_called()

    def __get_test_config_and_bundle_component(self, component_name):
        component = self.bundle_manifest.components[component_name]
        test_config = self.test_manifest.components[component.name]
        return test_config, component

    @patch("os.path.exists", return_value=True)
    @patch.object(ScriptFinder, "find_integ_test_script")
    @patch("test_workflow.integ_test.integ_test_suite.execute")
    @patch("test_workflow.integ_test.integ_test_suite.LocalTestCluster")
    @patch("test_workflow.test_recorder.test_recorder.TestRecorder")
    def test_execute_with_working_directory(self, mock_test_recorder, mock_local_test_cluster, mock_system_execute, mock_script_finder, *mock):
        test_config, component = self.__get_test_config_and_bundle_component("dashboards-reports")
        dependency_installer = MagicMock()
        integ_test_suite = IntegTestSuite(dependency_installer, component, test_config, self.bundle_manifest, self.build_manifest, "tmpdir", mock_test_recorder)
        mock_system_execute.return_value = 200, "success", "failure"
        mock_local_test_cluster.create().__enter__.return_value = "localhost", "9200"
        mock_script_finder.return_value = "integtest.sh"
        integ_test_suite.execute()
        mock_script_finder.assert_has_calls([call("dashboards-reports", os.path.join("tmpdir", "dashboards-reports", "reports-scheduler"))])
