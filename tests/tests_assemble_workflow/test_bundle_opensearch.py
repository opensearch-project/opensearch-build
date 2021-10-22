# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from assemble_workflow.bundle_opensearch import BundleOpenSearch
from manifests.build_manifest import BuildManifest
from paths.script_finder import ScriptFinder


class TestBundleOpenSearch(unittest.TestCase):
    def test_bundle_opensearch(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())
        self.assertEqual(bundle.min_tarball.name, "OpenSearch")
        self.assertEqual(len(bundle.plugins), 12)
        self.assertEqual(bundle.artifacts_dir, artifacts_path)
        self.assertIsNotNone(bundle.bundle_recorder)
        self.assertEqual(bundle.installed_plugins, [])
        self.assertTrue(bundle.min_tarball_path.endswith("opensearch-min-1.1.0-linux-x64.tar.gz"))
        self.assertIsNotNone(bundle.archive_path)

    def test_bundle_install_min(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts")
        bundle = BundleOpenSearch(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())

        with patch("subprocess.check_call") as mock_check_call:
            bundle.install_min()

            self.assertEqual(mock_check_call.call_count, 1)

            mock_check_call.assert_has_calls(
                [
                    call(
                        f'{ScriptFinder.find_install_script("OpenSearch")} -a "{artifacts_path}" -o "{bundle.archive_path}"',
                        cwd=bundle.archive_path,
                        shell=True,
                    ),
                ]
            )

    @patch.object(BundleOpenSearch, "install_plugin")
    def test_bundle_install_plugins(self, mocks_bundle):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        bundle = BundleOpenSearch(
            BuildManifest.from_path(manifest_path),
            os.path.join(os.path.dirname(__file__), "data", "artifacts"),
            MagicMock(),
        )

        bundle.install_plugins()
        self.assertEqual(mocks_bundle.call_count, 12)

    @patch("os.path.isfile", return_value=True)
    def test_bundle_install_plugin(self, *mocks):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(BuildManifest.from_path(manifest_path), artifacts_path, MagicMock())

        plugin = bundle.plugins[0]  # job-scheduler

        with patch("shutil.copyfile") as mock_copyfile:
            with patch("subprocess.check_call") as mock_check_call:
                bundle.install_plugin(plugin)

                self.assertEqual(mock_copyfile.call_count, 1)
                self.assertEqual(mock_check_call.call_count, 2)

                install_plugin_bin = os.path.join(bundle.archive_path, "bin", "opensearch-plugin")
                mock_check_call.assert_has_calls(
                    [
                        call(
                            f'{install_plugin_bin} install --batch file:{os.path.join(bundle.tmp_dir.name, "opensearch-job-scheduler-1.1.0.0.zip")}',
                            cwd=bundle.archive_path,
                            shell=True,
                        ),
                        call(
                            f'{ScriptFinder.find_install_script("opensearch-job-scheduler")} -a "{artifacts_path}" -o "{bundle.archive_path}"',
                            cwd=bundle.archive_path,
                            shell=True,
                        ),
                    ]
                )

    def test_bundle_build_tar(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        artifacts_path = os.path.join(os.path.dirname(__file__), "data", "artifacts")
        bundle = BundleOpenSearch(
            BuildManifest.from_path(manifest_path),
            artifacts_path,
            MagicMock(tar_name="opensearch.tar"),
        )

        with patch("tarfile.open") as mock_tarfile_open:
            mock_tarfile_add = MagicMock()
            mock_tarfile_open.return_value.__enter__.return_value.add = mock_tarfile_add
            with patch("shutil.copyfile") as mock_copyfile:
                bundle.build_tar(os.path.dirname(__file__))
                mock_tarfile_open.assert_called_with("opensearch.tar", "w:gz")
                mock_tarfile_add.assert_called_with(os.path.join(bundle.tmp_dir.name, "bundle"), arcname="bundle")
                self.assertEqual(mock_copyfile.call_count, 1)
