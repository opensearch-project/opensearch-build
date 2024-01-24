# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from build_workflow.build_incremental import BuildIncremental
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputManifest
from run_build import main


class TestRunBuild(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_build.py", "--help"])
    def test_usage(self) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    MANIFESTS = os.path.join(
        os.path.dirname(__file__),
        "..",
        "manifests",
    )

    OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(MANIFESTS, "templates", "opensearch", "2.x", "os-template-2.11.0.yml"))
    OPENSEARCH_MANIFEST_2_12 = os.path.realpath(os.path.join(MANIFESTS, "templates", "opensearch", "2.x", "os-template-2.12.0.yml"))
    NON_OPENSEARCH_MANIFEST = os.path.realpath(os.path.join(MANIFESTS, "templates", "opensearch", "1.x", "non-os-template-1.1.0.yml"))

    INPUT_MANIFEST_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "tests_build_workflow", "data", "opensearch-input-2.12.0.yml"))
    INPUT_MANIFEST = InputManifest.from_path(INPUT_MANIFEST_PATH)
    BUILD_MANIFEST = BuildManifest.from_path(
        os.path.join(os.path.dirname(__file__), "tests_build_workflow", "data", "opensearch-build-tar-2.12.0.yml"))
    BUILD_MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "tests_build_workflow", "data", "opensearch-build-tar-2.12.0.yml")
    INPUT_MANIFEST_DASHBOARDS = InputManifest.from_path(
        os.path.join(os.path.dirname(__file__), "tests_build_workflow", "data", "opensearch-dashboards-input-2.12.0.yml"))
    BUILD_MANIFEST_DASHBOARDS = BuildManifest.from_path(
        os.path.join(os.path.dirname(__file__), "tests_build_workflow", "data", "opensearch-dashboards-build-tar-2.12.0.yml"))
    buildIncremental = BuildIncremental(INPUT_MANIFEST, "tar")

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "linux"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_linux(self, mock_temp: Mock, mock_recorder: Mock, mock_builder: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertNotEqual(mock_builder.return_value.build.call_count, 0)
        self.assertEqual(mock_builder.return_value.build.call_count, mock_builder.return_value.export_artifacts.call_count)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "darwin"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_darwin(self, mock_temp: Mock, mock_recorder: Mock, mock_builder: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertNotEqual(mock_builder.return_value.build.call_count, 0)
        self.assertEqual(mock_builder.return_value.build.call_count, mock_builder.return_value.export_artifacts.call_count)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "windows"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_windows(self, mock_temp: Mock, mock_recorder: Mock, mock_builder: Mock, *mocks: Any) -> None:
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
            "templates",
            "opensearch-dashboards",
            "1.x",
            "osd-template-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-a", "x64"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_main_with_architecture(self, mock_temp: Mock, mock_recorder: Mock, mock_builder: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        main()
        self.assertEqual(mock_builder.return_value.build.call_count, 11)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, 11)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-p", "invalidplatform", "-a", "x64"])
    def test_main_with_invalid_platform(self, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-p", "linux", "-a", "invalidarchitecture"])
    def test_main_with_invalid_architecture(self, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

    @patch("os.path.exists", return_value=True)
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--lock"])
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("manifests.input.input_manifest_1_0.InputManifest_1_0.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("run_build.InputManifest.to_file")
    @patch("logging.info")
    def test_main_manifest_lock_without_changes(self, mock_logging: Mock, mock_to_file: Mock, mock_stable: Mock, *mocks: Any) -> None:
        main()
        mock_stable.assert_called_with()
        mock_to_file.assert_not_called()
        mock_logging.assert_called_with(f"No changes since {self.OPENSEARCH_MANIFEST}.lock")

    @patch("os.path.exists", return_value=True)
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--lock"])
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("manifests.input.input_manifest_1_0.InputManifest_1_0.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST_2_12))
    @patch("run_build.InputManifest.to_file")
    @patch("logging.info")
    def test_main_manifest_lock_with_changes(self, mock_logging: Mock, mock_to_file: Mock, mock_stable: Mock, *mocks: Any) -> None:
        main()
        mock_stable.assert_called_with()
        mock_to_file.assert_called_with(self.OPENSEARCH_MANIFEST + ".lock")
        mock_logging.assert_called_with(f"Updating {self.OPENSEARCH_MANIFEST}.lock")

    @patch("os.path.exists", return_value=False)
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--lock"])
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("manifests.input.input_manifest_1_0.InputManifest_1_0.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST_2_12))
    @patch("run_build.InputManifest.to_file")
    @patch("logging.info")
    def test_main_manifest_new_lock(self, mock_logging: Mock, mock_to_file: Mock, mock_stable: Mock, *mocks: Any) -> None:
        main()
        mock_stable.assert_called_with()
        mock_to_file.assert_called_with(self.OPENSEARCH_MANIFEST + ".lock")
        mock_logging.assert_called_with(f"Creating {self.OPENSEARCH_MANIFEST}.lock")

    @patch("os.path.exists", return_value=False)
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--lock", "--architecture", "arm64", "--platform", "windows", "--snapshot"])
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST))
    @patch("manifests.input.input_manifest_1_0.InputManifest_1_0.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST_2_12))
    @patch("run_build.InputManifest.to_file")
    @patch("logging.info")
    def test_main_manifest_new_lock_with_overrides(self, mock_logging: Mock, mock_to_file: Mock, mock_stable: Mock, *mocks: Any) -> None:
        main()
        mock_stable.assert_called_with()
        mock_to_file.assert_called_with(self.OPENSEARCH_MANIFEST + ".lock")
        mock_logging.assert_called_with(f"Creating {self.OPENSEARCH_MANIFEST}.lock")

    @patch("os.path.exists", return_value=True)
    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST_2_12, "--lock"])
    @patch("run_build.InputManifest.from_path", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST_2_12))
    @patch("run_build.InputManifest.stable", return_value=InputManifest.from_path(OPENSEARCH_MANIFEST_2_12))
    @patch("run_build.InputManifest.to_file")
    @patch("logging.info")
    def test_main_manifest_lock_without_changes_input_schema_1_1(self, mock_logging: Mock, mock_to_file: Mock, mock_stable: Mock, *mocks: Any) -> None:
        main()
        mock_stable.assert_called_with()
        mock_to_file.assert_not_called()
        mock_logging.assert_called_with(f"No changes since {self.OPENSEARCH_MANIFEST_2_12}.lock")

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "linux", "--continue-on-error"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    @patch("run_build.logging.error")
    def test_fail_core_component_continue_on_error(self, mock_logging_error: Mock, mock_temp: Mock, mock_recorder: Mock, mock_builder_from: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_builder = Mock()
        mock_builder.build.side_effect = Exception("Error during build")
        mock_builder_from.return_value = mock_builder
        with pytest.raises(Exception, match="Error during build"):
            main()
        mock_logging_error.assert_called_with(f"Error building OpenSearch, retry with: run_build.py {self.OPENSEARCH_MANIFEST} --component OpenSearch")

    @patch("argparse._sys.argv", ["run_build.py", NON_OPENSEARCH_MANIFEST, "-p", "linux", "--continue-on-error"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    @patch("run_build.logging.error")
    def test_common_utils_failure_continue_on_error(self, mock_logging_error: Mock, mock_temp: Mock, mock_recorder: Mock, mock_builder_from: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_builder = Mock()
        mock_builder.build.side_effect = Exception("Error building")
        mock_builder_from.return_value = mock_builder
        with pytest.raises(Exception, match="Error building"):
            main()
        mock_logging_error.assert_called_with(f"Error building common-utils, retry with: run_build.py {self.NON_OPENSEARCH_MANIFEST} --component common-utils")

    @patch("argparse._sys.argv", ["run_build.py", NON_OPENSEARCH_MANIFEST, "-p", "linux", "--continue-on-error", "--component", "sql", "alerting"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    @patch("run_build.logging.error")
    def test_fail_plugins_continue_on_error(self, mock_logging_error: Mock, mock_temp: Mock, mock_recorder: Mock, mock_builder_from: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_builder = Mock()
        mock_builder.build.side_effect = Exception("Error during build")
        mock_builder_from.return_value = mock_builder

        main()
        mock_logging_error.assert_called_with("Failed plugins are ['sql', 'alerting']")

    @patch("argparse._sys.argv", ["run_build.py", NON_OPENSEARCH_MANIFEST, "-p", "linux"])
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    @patch("run_build.logging.error")
    def test_failed_plugins_default(self, mock_logging_error: Mock, mock_temp: Mock, mock_recorder: Mock, mock_builder_from: Mock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_builder = Mock()
        mock_builder.build.side_effect = Exception("Error during build")
        mock_builder_from.return_value = mock_builder
        with pytest.raises(Exception, match="Error during build"):
            main()
        mock_logging_error.assert_called_with(f"Error building common-utils, retry with: run_build.py {self.NON_OPENSEARCH_MANIFEST} --component common-utils")

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "--incremental"])
    @patch("os.path.exists")
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("run_build.TemporaryDirectory")
    @patch("run_build.BuildIncremental")
    def test_main_incremental(self, mock_build_incremental: MagicMock, mock_temp: MagicMock,
                              mock_build_manifest: MagicMock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        main()
        self.assertEqual(mock_build_incremental.call_count, 1)
        mock_build_incremental.return_value.commits_diff.assert_called()
        mock_build_incremental.return_value.rebuild_plugins.assert_called()

    @patch.dict(os.environ, {"BUILD_NUMBER": "1234"})
    @patch("argparse._sys.argv", ["run_build.py", INPUT_MANIFEST_PATH, "--incremental", "-p", "linux"])
    @patch("run_build.BuildIncremental.commits_diff", return_value=MagicMock())
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("run_build.BuildIncremental.rebuild_plugins", return_value=MagicMock())
    @patch("run_build.logging.info")
    def test_build_incremental_no_change(self, mock_logging_info: MagicMock,
                                         mock_build_incremental: MagicMock, mock_build_manifest: MagicMock,
                                         *mocks: Any) -> None:
        mock_build_incremental.return_value = []
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        main()
        mock_logging_info.assert_has_calls([
            call("No commit difference found between any components. Skipping the build.")
        ], any_order=True)
        mock_logging_info.assert_has_calls([
            call("Updating the build ID in the build manifest to 1234.")
        ], any_order=True)

    @patch("argparse._sys.argv", ["run_build.py", INPUT_MANIFEST_PATH, "--incremental"])
    @patch("run_build.BuildIncremental", return_value=MagicMock())
    @patch("os.path.exists")
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_build_incremental_no_prebuild_manifest(self, mock_temp: MagicMock, mock_recorder: MagicMock,
                                                    mock_builder: MagicMock, mock_path_exists: MagicMock,
                                                    *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_path_exists.return_value = False
        try:
            main()
            self.assertRaises(FileNotFoundError)
        except FileNotFoundError:
            pass

    @patch("argparse._sys.argv", ["run_build.py", INPUT_MANIFEST_PATH, "--incremental", "-p", "linux"])
    @patch("run_build.BuildIncremental.commits_diff", return_value=MagicMock())
    @patch("run_build.BuildIncremental.rebuild_plugins", return_value=MagicMock())
    @patch("run_build.logging.info")
    @patch("run_build.BuildOutputDir")
    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_build_incremental_with_prebuild_manifest(self, mock_temp: MagicMock, mock_recorder: MagicMock,
                                                      mock_builder: MagicMock, mock_build_manifest: MagicMock,
                                                      mock_path_exist: MagicMock, mock_build_output_dir: MagicMock,
                                                      mock_logging_info: MagicMock, mock_build_incremental: MagicMock,
                                                      *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_path_exist.return_value = True
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_build_incremental.return_value = ["common-utils", "opensearch-observability"]
        main()
        mock_build_manifest.assert_called_once()
        mock_build_manifest.assert_called_with(os.path.join("tar", "builds", "opensearch", "manifest.yml"))
        self.assertNotEqual(mock_builder.return_value.build.call_count, 0)
        self.assertEqual(mock_builder.return_value.build.call_count, 2)
        self.assertEqual(mock_builder.return_value.build.call_count, mock_builder.return_value.export_artifacts.call_count)

        mock_logging_info.assert_has_calls([
            call('Building common-utils'),
            call('Building opensearch-observability'),
        ], any_order=True)

        mock_recorder.assert_called_once()
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", INPUT_MANIFEST_PATH, "--incremental", "-p", "linux", "--continue-on-error"])
    @patch("run_build.BuildIncremental.commits_diff", return_value=MagicMock())
    @patch("run_build.BuildIncremental.rebuild_plugins", return_value=MagicMock())
    @patch("run_build.logging.error")
    @patch("run_build.logging.info")
    @patch("run_build.BuildOutputDir")
    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_build_incremental_continue_on_fail_core(self, mock_temp: MagicMock, mock_recorder: MagicMock,
                                                     mock_builder_from: MagicMock, mock_build_manifest: MagicMock,
                                                     mock_path_exist: MagicMock, mock_build_output_dir: MagicMock,
                                                     mock_logging_info: MagicMock, mock_logging_error: MagicMock,
                                                     mock_build_incremental: MagicMock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_path_exist.return_value = True
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_builder = MagicMock()
        mock_builder.build.side_effect = Exception("Error building")
        mock_builder_from.return_value = mock_builder
        mock_build_incremental.return_value = ["common-utils", "opensearch-observability"]

        with pytest.raises(Exception, match="Error building"):
            main()

        mock_logging_error.assert_called_with(f"Error building common-utils, retry with: run_build.py {self.INPUT_MANIFEST_PATH} --component common-utils")
        mock_build_manifest.assert_called_once()
        mock_build_manifest.assert_called_with(os.path.join("tar", "builds", "opensearch", "manifest.yml"))
        self.assertNotEqual(mock_builder.build.call_count, 0)
        self.assertEqual(mock_builder.build.call_count, 1)

        mock_logging_info.assert_has_calls([
            call('Building common-utils')
        ], any_order=True)

        mock_recorder.assert_called_once()
        mock_recorder.return_value.write_manifest.assert_not_called()

    @patch("argparse._sys.argv", ["run_build.py", INPUT_MANIFEST_PATH, "--incremental", "-p", "linux", "--continue-on-error"])
    @patch("run_build.BuildIncremental.commits_diff", return_value=MagicMock())
    @patch("run_build.BuildIncremental.rebuild_plugins", return_value=MagicMock())
    @patch("run_build.logging.error")
    @patch("run_build.logging.info")
    @patch("run_build.BuildOutputDir")
    @patch("os.path.exists")
    @patch("manifests.build_manifest.BuildManifest.from_path")
    @patch("run_build.Builders.builder_from", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.TemporaryDirectory")
    def test_build_incremental_continue_on_fail_plugin(self, mock_temp: MagicMock, mock_recorder: MagicMock,
                                                       mock_builder_from: MagicMock, mock_build_manifest: MagicMock,
                                                       mock_path_exist: MagicMock, mock_build_output_dir: MagicMock,
                                                       mock_logging_info: MagicMock, mock_logging_error: MagicMock,
                                                       mock_build_incremental: MagicMock, *mocks: Any) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_path_exist.return_value = True
        mock_build_manifest.return_value = self.BUILD_MANIFEST
        mock_builder = MagicMock()
        mock_builder.build.side_effect = Exception("Error build")
        mock_builder_from.return_value = mock_builder
        mock_build_incremental.return_value = ["ml-commons", "opensearch-observability"]

        main()

        mock_logging_error.assert_called_with("Failed plugins are ['ml-commons', 'opensearch-observability']")
        mock_build_manifest.assert_called_once()
        mock_build_manifest.assert_called_with(os.path.join("tar", "builds", "opensearch", "manifest.yml"))
        self.assertNotEqual(mock_builder.build.call_count, 0)
        self.assertEqual(mock_builder.build.call_count, 2)

        mock_logging_info.assert_has_calls([
            call('Building ml-commons'),
            call('Building opensearch-observability')
        ], any_order=True)

        mock_recorder.assert_called_once()
        mock_recorder.return_value.write_manifest.assert_called()
