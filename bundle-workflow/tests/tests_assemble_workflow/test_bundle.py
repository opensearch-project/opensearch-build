# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from assemble_workflow.bundle import Bundle
from manifests.build_manifest import BuildManifest
from paths.script_finder import ScriptFinder


class TestBundle(unittest.TestCase):
    def test_bundle(self):
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts")
            bundle = Bundle(BuildManifest.from_file(f), artifacts_path, MagicMock())
            self.assertEqual(bundle.min_tarball.name, "OpenSearch")
            self.assertEqual(len(bundle.plugins), 12)
            self.assertEqual(bundle.artifacts_dir, artifacts_path)
            self.assertIsNotNone(bundle.bundle_recorder)
            self.assertEqual(bundle.installed_plugins, [])
            self.assertTrue(
                bundle.min_tarball_path.endswith(
                    "/opensearch-min-1.1.0-linux-x64.tar.gz"
                )
            )
            self.assertIsNotNone(bundle.archive_path)

    @patch.object(Bundle, "install_plugin")
    def test_bundle_install_plugins(self, mocks_bundle):
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            bundle = Bundle(
                BuildManifest.from_file(f),
                os.path.join(os.path.dirname(__file__), "data/artifacts"),
                MagicMock(),
            )

            bundle.install_plugins()
            self.assertEqual(mocks_bundle.call_count, 12)

    def test_bundle_install_plugin(self):
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts")
            bundle = Bundle(BuildManifest.from_file(f), artifacts_path, MagicMock())

            plugin = bundle.plugins[0]  # job-scheduler
            with patch("os.path.isfile", return_value=True):
                with patch("shutil.copyfile") as mock_copyfile:
                    with patch("subprocess.check_call") as mock_check_call:
                        bundle.install_plugin(plugin)
                        self.assertEqual(mock_copyfile.call_count, 1)
                        self.assertEqual(mock_check_call.call_count, 2)
                        install_plugin_bin = os.path.join(
                            bundle.archive_path, "bin/opensearch-plugin"
                        )
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
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            artifacts_path = os.path.join(os.path.dirname(__file__), "data/artifacts")
            bundle = Bundle(
                BuildManifest.from_file(f),
                artifacts_path,
                MagicMock(tar_name="opensearch.tar"),
            )

            with patch("tarfile.open") as mock_tarfile_open:
                mock_tarfile_add = MagicMock()
                mock_tarfile_open.return_value.__enter__.return_value.add = (
                    mock_tarfile_add
                )
                with patch("shutil.copyfile") as mock_copyfile:
                    bundle.build_tar(os.path.dirname(__file__))
                    mock_tarfile_open.assert_called_with("opensearch.tar", "w:gz")
                    mock_tarfile_add.assert_called_with(
                        os.path.join(bundle.tmp_dir.name, "bundle"), arcname="bundle"
                    )
                    self.assertEqual(mock_copyfile.call_count, 1)

    def test_bundle_does_not_exist_raises_error(self):
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            with self.assertRaisesRegex(
                FileNotFoundError,
                "does-not-exist/bundle/opensearch-min-1.1.0-linux-x64.tar.gz",
            ):
                Bundle(
                    BuildManifest.from_file(f),
                    os.path.join(os.path.dirname(__file__), "data/does-not-exist"),
                    MagicMock(),
                )

    def test_bundle_invalid_archive_raises_error(self):
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            with self.assertRaisesRegex(FileNotFoundError, "(/*)$"):
                Bundle(
                    BuildManifest.from_file(f),
                    os.path.join(os.path.dirname(__file__), "data/invalid"),
                    MagicMock(),
                )
