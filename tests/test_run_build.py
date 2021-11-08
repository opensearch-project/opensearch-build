# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import pytest

from manifests.input_manifest import InputManifest
from run_build import main


class TestRunBuild(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_build.py", "--help"])
    def test_usage(self):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    MANIFESTS = os.path.join(
        os.path.dirname(__file__),
        "..",
        "manifests",
    )

    OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(MANIFESTS, "1.1.0", "opensearch-1.1.0.yml"))
    OPENSEARCH_MANIFEST_1_2 = os.path.realpath(os.path.join(MANIFESTS, "1.2.0", "opensearch-1.2.0.yml"))

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "linux"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_linux(self, mock_temp, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertNotEqual(mock_builder.return_value.build.call_count, 0)
        self.assertEqual(mock_builder.return_value.build.call_count, mock_builder.return_value.export_artifacts.call_count)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "darwin"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_darwin(self, mock_temp, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertNotEqual(mock_builder.return_value.build.call_count, 0)
        self.assertEqual(mock_builder.return_value.build.call_count, mock_builder.return_value.export_artifacts.call_count)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "windows"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_windows(self, mock_temp, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        # excludes performance analyzer and k-nn
        for call_args in mock_builder.call_args:
            if len(call_args) > 1:
                component = call_args[0]
                self.assertNotIn("k-nn", component.name.lower())
                self.assertNotIn("analyzer", component.name.lower())

        self.assertNotEqual(mock_builder.call_count, 0)
        self.assertEqual(mock_builder.return_value.build.call_count, mock_builder.call_count)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, mock_builder.call_count)
        mock_recorder.return_value.write_manifest.assert_called()

    OPENSEARCH_DASHBOARDS_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "manifests",
            "1.1.0",
            "opensearch-dashboards-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-a", "x64"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_with_architecture(self, mock_temp, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertEqual(mock_builder.return_value.build.call_count, 11)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, 11)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-p", "invalidplatform", "-a", "x64"])
    def test_main_with_invalid_platform(self, *mocks):
        with self.assertRaises(SystemExit):
            main()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-p", "linux", "-a", "invalidarchitecture"])
    def test_main_with_invalid_architecture(self, *mocks):
        with self.assertRaises(SystemExit):
            main()

    @patch("os.path.exists", return_value=True)
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("run_build.InputManifest.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--lock"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    @patch("logging.info")
    def test_main_incremental_without_changes(self, mock_logging, mock_temp, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        with self.assertRaises(SystemExit):
            main()
        self.assertEqual(mock_builder.return_value.build.call_count, 0)
        mock_logging.assert_called_with(f"No changes since {self.OPENSEARCH_MANIFEST}.lock")
        mock_recorder.return_value.write_manifest.assert_not_called()

    @patch("os.path.exists", return_value=True)
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("run_build.InputManifest.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST_1_2))
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--lock"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    @patch("run_build.InputManifest.to_file")
    def test_main_incremental_with_changes(self, mock_to_file, mock_temp, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        mock_to_file.assert_called_with(self.OPENSEARCH_MANIFEST + ".lock")
        mock_recorder.return_value.write_manifest.assert_called()
