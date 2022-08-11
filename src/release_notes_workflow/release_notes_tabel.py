# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import IO, Any, List

from pytablewriter import MarkdownTableWriter

from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes import ReleaseNotes


class ReleaseNotesTabel:

    @classmethod
    def tabel(self, manifest: IO, date: str, save: bool) -> int:
        value_matrix = []  # type: List[Any]
        manifest_file = InputManifest.from_file(manifest)
        for component in manifest_file.components.select():
            if type(component) is InputComponentFromSource:
                changes = ReleaseNotes(component, manifest_file, date)
                value_matrix.append(changes.check())
        writer = MarkdownTableWriter(
            table_name=f"{manifest_file.build.name} CommitID(after {date}) & Release Notes info",
            headers=["Repo", "Branch", "CommitID", "Commit Date", "Release Notes"],
            value_matrix=value_matrix
        )
        writer.write_table()
        if save:
            writer.dump("table.md")
        return 0
