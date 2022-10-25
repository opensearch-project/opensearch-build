# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, Mock, call, patch

from assemble_workflow.bundle_opensearch_dashboards import BundleOpenSearchDashboards
from manifests.build_manifest import BuildManifest
from paths.script_finder import ScriptFinder
from system.os import current_platform


class TestBundleOpenSearchDashboards(unittest.TestCase):
    def test_bundle_opensearch_dashboards(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-dashboards-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearchDashboards(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())
        self.assertEqual(bundle.min_dist.name, "OpenSearch-Dashboards")
        self.assertEqual(len(bundle.components), 2)
        self.assertEqual(bundle.artifacts_dir, artifacts_path)
        self.assertIsNotNone(bundle.bundle_recorder)
        self.assertEqual(bundle.installed_plugins, [])
        self.assertTrue(bundle.min_dist.path.endswith("opensearch-dashboards-min-1.1.0-linux-x64.tar.gz"))

    def test_bundle_install_min(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-dashboards-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts")
        bundle = BundleOpenSearchDashboards(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())

        with patch("subprocess.check_call") as mock_check_call:
            bundle.install_min()

            self.assertEqual(mock_check_call.call_count, 1)

            mock_check_call.assert_has_calls(
                [
                    call(
                        " ".join(
                            [
                                "bash",
                                ScriptFinder.find_install_script("OpenSearch-Dashboards"),
                                "-v 1.1.0",
                                "-p linux",
                                "-a x64",
                                "-f",
                                artifacts_path,
                                "-o",
                                bundle.min_dist.archive_path,
                            ]
                        ),
                        cwd=bundle.min_dist.archive_path,
                        shell=True,
                    ),
                ]
            )

    @patch("os.path.isfile", return_value=True)
    def test_bundle_install_plugin(self, path_isfile: Mock) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-dashboards-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearchDashboards(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())

        plugin = bundle.components['alertingDashboards']

        with patch("shutil.copyfile") as mock_copyfile:
            with patch("subprocess.check_call") as mock_check_call:
                bundle.install_plugin(plugin)

                self.assertEqual(mock_copyfile.call_count, 1)
                self.assertEqual(mock_check_call.call_count, 2)

                script = "opensearch-dashboards-plugin.bat" if current_platform() == "windows" else "opensearch-dashboards-plugin"
                install_plugin_bin = os.path.join(bundle.min_dist.archive_path, "bin", script)
                mock_check_call.assert_has_calls(
                    [
                        call(
                            f'{install_plugin_bin} --allow-root install file:{os.path.join(bundle.tmp_dir.name, "alertingDashboards-1.1.0.zip")}',
                            cwd=bundle.min_dist.archive_path,
                            shell=True,
                        ),
                        call(
                            " ".join(
                                [
                                    "bash",
                                    ScriptFinder.find_install_script("alertingDashboards"),
                                    "-v 1.1.0",
                                    "-p linux",
                                    "-a x64",
                                    "-f",
                                    artifacts_path,
                                    "-o",
                                    bundle.min_dist.archive_path,
                                ]
                            ),
                            cwd=bundle.min_dist.archive_path,
                            shell=True,
                        ),
                    ]
                )
        self.assertEqual(path_isfile.call_count, 2)
