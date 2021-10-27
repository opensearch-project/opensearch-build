# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

import pytest

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

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "manifests",
            "1.1.0",
            "opensearch-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "linux"])
    @patch("run_build.Builder", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.GitRepository")
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_linux(self, mock_temp, mock_repo, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        repo = MagicMock(name="dummy")
        mock_repo.return_value.__enter__.return_value = repo

        main()

        # each repository is checked out locally
        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "OpenSearch"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/common-utils.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "common-utils"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/dashboards-reports.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "dashboards-reports"),
                    "reports-scheduler",
                ),
            ],
            any_order=True,
        )

        self.assertEqual(mock_repo.call_count, 15)

        # each component is built and its artifacts exported
        mock_builder.assert_has_calls(
            [
                call("OpenSearch", repo, mock_recorder.return_value),
                call("common-utils", repo, mock_recorder.return_value),
                call(
                    "dashboards-reports",
                    repo,
                    mock_recorder.return_value,
                ),
            ],
            any_order=True,
        )

        self.assertEqual(mock_builder.call_count, 15)
        self.assertEqual(mock_builder.return_value.build.call_count, 15)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, 15)

        # the output manifest is written
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "darwin"])
    @patch("run_build.Builder", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.GitRepository")
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_darwin(self, mock_temp, mock_repo, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_repo.return_value.__enter__.return_value = MagicMock(name="dummy")
        main()
        self.assertEqual(mock_repo.call_count, 15)
        self.assertEqual(mock_builder.call_count, 15)
        self.assertEqual(mock_builder.return_value.build.call_count, 15)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, 15)
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST, "-p", "windows"])
    @patch("run_build.BuildTarget", return_value=MagicMock(output_dir="artifacts"))
    @patch("run_build.Builder", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.GitRepository")
    @patch("run_build.TemporaryDirectory")
    def test_main_platform_windows(self, mock_temp, mock_repo, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_repo.return_value.__enter__.return_value = MagicMock(name="dummy")
        main()
        # excludes performance analyzer and k-nn
        self.assertEqual(mock_repo.call_count, 13)
        self.assertEqual(mock_builder.call_count, 13)
        self.assertEqual(mock_builder.return_value.build.call_count, 13)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, 13)
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
    @patch("run_build.BuildTarget", return_value=MagicMock(output_dir="artifacts"))
    @patch("run_build.Builder", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.GitRepository")
    @patch("run_build.TemporaryDirectory")
    def test_main_with_architecture(self, mock_temp, mock_repo, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        repo = MagicMock(name="dummy")
        mock_repo.return_value.__enter__.return_value = repo

        main()

        # each repository is checked out locally
        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch-Dashboards.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "OpenSearch-Dashboards"),
                    None,
                ),
            ],
            any_order=True,
        )

        # each component is built and its artifacts exported
        mock_builder.assert_has_calls(
            [
                call("OpenSearch-Dashboards", repo, mock_recorder.return_value),
            ],
            any_order=True,
        )

        # the output manifest is written
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-a", "arm64"])
    @patch("run_build.Builder", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.GitRepository")
    @patch("run_build.TemporaryDirectory")
    def test_main_with_architecture_arm64(self, mock_temp, mock_repo, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        repo = MagicMock(name="dummy")
        mock_repo.return_value.__enter__.return_value = repo

        main()

        # each repository is checked out locally
        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch-Dashboards.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "OpenSearch-Dashboards"),
                    None,
                ),
            ],
            any_order=True,
        )

        # each component is built and its artifacts exported
        mock_builder.assert_has_calls(
            [
                call("OpenSearch-Dashboards", repo, mock_recorder.return_value),
            ],
            any_order=True,
        )

        # the output manifest is written
        mock_recorder.return_value.write_manifest.assert_called()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-p", "invalidplatform", "-a", "x64"])
    def test_main_with_invalid_platform(self, *mocks):
        with self.assertRaises(SystemExit):
            main()

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_DASHBOARDS_MANIFEST, "-p", "linux", "-a", "invalidarchitecture"])
    def test_main_with_invalid_architecture(self, *mocks):
        with self.assertRaises(SystemExit):
            main()
