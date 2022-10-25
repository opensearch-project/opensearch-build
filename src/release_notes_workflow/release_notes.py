# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import List

from pytablewriter import MarkdownTableWriter

from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from system.temporary_directory import TemporaryDirectory


class ReleaseNotes:

    def __init__(self, manifest: InputManifest, date: str) -> None:
        self.manifest = manifest
        self.date = date

    def table(self) -> MarkdownTableWriter:
        table_result = []
        for component in self.manifest.components.select():
            if type(component) is InputComponentFromSource:
                table_result.append(self.check(component))
        writer = MarkdownTableWriter(
            table_name=f" {self.manifest.build.name} CommitID(after {self.date}) & Release Notes info",
            headers=["Repo", "Branch", "CommitID", "Commit Date", "Release Notes"],
            value_matrix=table_result
        )
        return writer

    def check(self, component: InputComponentFromSource) -> List:
        results = []
        with TemporaryDirectory(chdir=True) as work_dir:
            results.append(component.name)
            results.append(component.ref)
            with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory,
            ) as repo:
                logging.debug(f"Checked out {component.name} into {repo.dir}")
                release_notes = ReleaseNotesComponents.from_component(component, self.manifest.build.version, repo.dir)
                commits = repo.log(self.date)
                if len(commits) > 0:
                    last_commit = commits[-1]
                    results.append(last_commit.id)
                    results.append(last_commit.date)
                else:
                    results.append(None)
                    results.append(None)
                results.append(release_notes.exists())
        return results
