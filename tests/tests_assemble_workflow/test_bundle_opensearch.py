# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
import zipfile
from unittest.mock import MagicMock, Mock, call, patch

from assemble_workflow.bundle_opensearch import BundleOpenSearch
from manifests.build_manifest import BuildManifest
from paths.script_finder import ScriptFinder
from system.os import current_platform


class TestBundleOpenSearch(unittest.TestCase):
    def test_bundle_opensearch(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())
        self.assertEqual(bundle.min_dist.name, "OpenSearch")
        self.assertEqual(len(bundle.plugins), 12)
        self.assertEqual(bundle.artifacts_dir, artifacts_path)
        self.assertIsNotNone(bundle.bundle_recorder)
        self.assertEqual(bundle.installed_plugins, [])
        self.assertTrue(bundle.min_dist.path.endswith("opensearch-min-1.1.0-linux-x64.tar.gz"))
        self.assertIsNotNone(bundle.min_dist.archive_path)

    def test_bundle_install_min(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())

        with patch("subprocess.check_call") as mock_check_call:
            bundle.install_min()

            self.assertEqual(mock_check_call.call_count, 1)

            mock_check_call.assert_has_calls(
                [
                    call(
                        " ".join(
                            [
                                "bash",
                                ScriptFinder.find_install_script("OpenSearch"),
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

    @patch.object(BundleOpenSearch, "install_plugin")
    def test_bundle_install_plugins(self, bundle_install_plugin: Mock) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        bundle = BundleOpenSearch(
            BuildManifest.from_path(manifest_path),
            os.path.join(os.path.dirname(__file__), "data", "artifacts"),
            MagicMock(),
        )

        bundle.install_plugins()
        self.assertEqual(bundle_install_plugin.call_count, 12)

    @patch("os.path.isfile", return_value=True)
    def test_bundle_install_plugin(self, path_isfile: Mock) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())

        plugin = bundle.plugins[0]  # job-scheduler

        with patch("shutil.copyfile") as mock_copyfile:
            with patch("subprocess.check_call") as mock_check_call:
                bundle.install_plugin(plugin)

                self.assertEqual(mock_copyfile.call_count, 1)
                self.assertEqual(mock_check_call.call_count, 2)

                script = "opensearch-plugin.bat" if current_platform() == "windows" else "opensearch-plugin"
                install_plugin_bin = os.path.join(bundle.min_dist.archive_path, "bin", script)
                mock_check_call.assert_has_calls(
                    [
                        call(
                            f'{install_plugin_bin} install --batch file:{os.path.join(bundle.tmp_dir.name, "opensearch-job-scheduler-1.1.0.0.zip")}',
                            cwd=bundle.min_dist.archive_path,
                            shell=True,
                        ),
                        call(
                            " ".join(
                                [
                                    "bash",
                                    ScriptFinder.find_install_script("opensearch-job-scheduler"),
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

    def test_bundle_package_tar(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(
            BuildManifest.from_path(manifest_path),
            artifacts_path,
            MagicMock(package_name="opensearch.tar"),
        )

        with patch("tarfile.open") as mock_tarfile_open:
            mock_tarfile_add = MagicMock()
            mock_tarfile_open.return_value.__enter__.return_value.add = mock_tarfile_add
            with patch("shutil.copyfile") as mock_copyfile:
                bundle.package(os.path.dirname(__file__))
                mock_tarfile_open.assert_called_with("opensearch.tar", "w:gz")
                mock_tarfile_add.assert_called_with(os.path.join(bundle.tmp_dir.name, "bundle"), arcname="bundle")
                self.assertEqual(mock_copyfile.call_count, 1)

    def test_bundle_package_zip(self) -> None:
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-windows-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(
            BuildManifest.from_path(manifest_path),
            artifacts_path,
            MagicMock(package_name="opensearch.zip"),
        )

        with patch("assemble_workflow.dist.ZipFile") as mock_zipfile_open:
            mock_zipfile_write = MagicMock()
            mock_zipfile_open.return_value.__enter__.return_value.write = mock_zipfile_write
            with patch("shutil.copyfile") as mock_copyfile:
                bundle.package(os.path.dirname(__file__))
                mock_zipfile_open.assert_called_with("opensearch.zip", "w", zipfile.ZIP_DEFLATED)
                mock_zipfile_write.assert_called_with(os.path.join(bundle.tmp_dir.name, "dist", "opensearch.txt"), "opensearch.txt")
                self.assertEqual(mock_copyfile.call_count, 1)
