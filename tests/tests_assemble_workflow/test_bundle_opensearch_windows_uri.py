# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import types
from pathlib import Path
from typing import Any, List, cast
from unittest.mock import patch

from assemble_workflow.bundle_opensearch import BundleOpenSearch
from assemble_workflow.dist import Dist
from manifests.build_manifest import BuildComponent, BuildManifest
from system.temporary_directory import TemporaryDirectory


class DummyBundle(BundleOpenSearch):
    """
    Minimal stub to exercise install_plugin() without running full Bundle initialization.
    Captures executed commands for assertions.
    """

    def __init__(self, archive_path: str, tmp_dir: Path):
        # Only set attributes used by install_plugin() and super().install_plugin()
        self.min_dist = cast(Dist, types.SimpleNamespace(archive_path=archive_path))
        self.build = cast(
            BuildManifest.Build,
            types.SimpleNamespace(
                version="3.3.0",
                platform="windows",
                architecture="x64",
                distribution="zip",
            ),
        )
        self.tmp_dir = cast(TemporaryDirectory, types.SimpleNamespace(name=str(tmp_dir)))
        self.artifacts_dir = str(tmp_dir)
        self._commands: List[str] = []

    def _copy_component(self, plugin: Any, subdir: str) -> str:
        # Simulate copied plugin zip path
        return str(Path(self.tmp_dir.name) / "opensearch-ltr-3.3.0.0.zip")

    def _execute(self, cmd: str) -> None:
        # Capture any command invoked by install_plugin() and super().install_plugin()
        self._commands.append(cmd)


def test_install_plugin_converts_windows_path_to_file_uri(tmp_path: Path) -> None:
    # Force windows behavior for this test to validate .bat and file:/// URI usage.
    with patch("assemble_workflow.bundle_opensearch.current_platform", return_value="windows"):
        archive_path = r"C:\0p8tp1m4\opensearch-3.3.0"
        b = DummyBundle(archive_path, tmp_path)

        plugin = BuildComponent({
            "name": "opensearch-learning-to-rank-base",
            "repository": "https://example.com/repo.git",
            "ref": "main",
            "commit_id": "deadbeef",
            "artifacts": {},
            "version": "0.0.0",
        })
        b.install_plugin(plugin)

        assert b._commands, "Expected at least one command to be executed"
        cmd = b._commands[0]

        # Must use .bat launcher on Windows
        assert "opensearch-plugin.bat install --batch" in cmd

        # Must pass a file: URI with forward slashes for the zip path (command path may use backslashes on Windows)
        assert "file:///" in cmd
        uri = cmd.split("--batch", 1)[1].strip()
        assert uri.startswith("file:///")
        assert "\\" not in uri

        # Sanity: ends with expected filename
        assert cmd.endswith("opensearch-ltr-3.3.0.0.zip")
