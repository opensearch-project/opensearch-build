# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import call, patch

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from test_workflow.integ_test.integ_test_suite import (DependencyInstaller,
                                                       IntegTestSuite,
                                                       InvalidTestConfigError,
                                                       ScriptFinder)


@patch("os.makedirs")
@patch("os.chdir")
@patch.object(GitRepository, "__checkout__")
class TestIntegSuite(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        self.bundle_manifest = BundleManifest.from_path("data/bundle_manifest.yml")
        self.build_manifest = BuildManifest.from_path("data/build_manifest.yml")
        self.test_manifest = TestManifest.from_path("data/test_manifest.yml")

    @patch.object(DependencyInstaller, "install_build_dependencies")
    @patch("os.path.exists", return_value=True)
    @patch.object(ScriptFinder, "find_integ_test_script")
    @patch("test_workflow.integ_test.integ_test_suite.execute")
    @patch("test_workflow.integ_test.integ_test_suite.LocalTestCluster")
    def test_execute_with_multiple_test_configs(
        self, mock_local_test_cluster, mock_system_execute, mock_script_finder, *mock
    ):
        test_config, component = self.__get_test_config_and_bundle_component(
            "job-scheduler"
        )
        integ_test_suite = IntegTestSuite(
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            "/tmpdir",
            "s3_bucket_name",
        )
        mock_system_execute.return_value = 200, "success", "failure"
        mock_local_test_cluster.create().__enter__.return_value = "localhost", "9200"
        mock_script_finder.return_value = "integtest.sh"
        integ_test_suite.execute()
        mock_system_execute.assert_has_calls(
            [
                call(
                    "integtest.sh -b localhost -p 9200 -s true -v 1.1.0",
                    "/tmpdir/job-scheduler",
                    True,
                    False,
                )
            ]
        )

    @patch.object(
        IntegTestSuite, "_IntegTestSuite__setup_cluster_and_execute_test_config"
    )
    @patch("test_workflow.integ_test.integ_test_suite.DependencyInstaller")
    def test_execute_with_build_dependencies(self, mock_dependency_installer, *mock):
        test_config, component = self.__get_test_config_and_bundle_component(
            "index-management"
        )
        integ_test_suite = IntegTestSuite(
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            "/tmpdir",
            "s3_bucket_name",
        )
        integ_test_suite.execute()
        mock_dependency_installer.return_value.install_build_dependencies.assert_called_with(
            {"opensearch-job-scheduler": "1.1.0.0"},
            "/tmpdir/index-management/src/test/resources/job-scheduler",
        )

    @patch.object(
        IntegTestSuite, "_IntegTestSuite__setup_cluster_and_execute_test_config"
    )
    @patch.object(DependencyInstaller, "install_build_dependencies")
    def test_execute_without_build_dependencies(
        self, mock_install_build_dependencies, *mock
    ):
        test_config, component = self.__get_test_config_and_bundle_component(
            "job-scheduler"
        )
        integ_test_suite = IntegTestSuite(
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            "/tmpdir",
            "s3_bucket_name",
        )
        integ_test_suite.execute()
        mock_install_build_dependencies.assert_not_called()

    @patch.object(
        IntegTestSuite, "_IntegTestSuite__setup_cluster_and_execute_test_config"
    )
    @patch.object(DependencyInstaller, "install_build_dependencies")
    def test_execute_with_unsupported_build_dependencies(
        self, mock_install_build_dependencies, *mock
    ):
        test_config, component = self.__get_test_config_and_bundle_component(
            "anomaly-detection"
        )
        integ_test_suite = IntegTestSuite(
            component,
            test_config,
            self.bundle_manifest,
            self.build_manifest,
            "/tmpdir",
            "s3_bucket_name",
        )
        with self.assertRaises(InvalidTestConfigError):
            integ_test_suite.execute()
        mock_install_build_dependencies.assert_not_called()

    @patch.object(DependencyInstaller, "install_build_dependencies")
    def test_execute_with_missing_job_scheduler(
        self, mock_install_build_dependencies, *mock
    ):
        invalid_build_manifest = BuildManifest.from_path(
            "data/build_manifest_missing_components.yml"
        )
        test_config, component = self.__get_test_config_and_bundle_component(
            "index-management"
        )
        integ_test_suite = IntegTestSuite(
            component,
            test_config,
            self.bundle_manifest,
            invalid_build_manifest,
            "/tmpdir",
            "s3_bucket_name",
        )
        with self.assertRaises(BuildManifest.ComponentNotFoundError) as context:
            integ_test_suite.execute()
        self.assertEqual(
            str(context.exception), "job-scheduler not found in build manifest.yml"
        )
        mock_install_build_dependencies.assert_not_called()

    def __get_test_config_and_bundle_component(self, component_name):
        for component in self.test_manifest.components:
            if component.name == component_name:
                test_config = component
                break
        for component in self.bundle_manifest.components:
            if component.name == component_name:
                break
        return test_config, component
