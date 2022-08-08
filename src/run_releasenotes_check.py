# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import Any, List

from pytablewriter import MarkdownTableWriter

from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.releasenotes_check import ReleaseNotesCheck
from release_notes_workflow.releasenotes_check_args import ReleaseNotesCheckArgs
from release_notes_workflow.releasenotes_gitlog import GitLog
from system import console
from system.temporary_directory import TemporaryDirectory


def main() -> int:
    value_matrix = []  # type: List[Any]
    args = ReleaseNotesCheckArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)
    writer = MarkdownTableWriter(
        table_name=f"{manifest.build.name} CommitID(after {args.date}) & Release Notes info",
        headers=["Repo", "Branch", "CommitID", "Commit Date", "Release Notes"],
        value_matrix=value_matrix
    )
    with TemporaryDirectory(chdir=True) as work_dir:
        logging.info(f"Checking out into {work_dir.name}")
        for component in manifest.components.select():
            logging.info(f"Checking out {component.name}")
            repo_list = []  # type: List[Any]
            if type(component) is InputComponentFromSource:
                with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory,
                ) as repo:
                    logging.debug(f"Checked out {component.name} into {repo.dir}")
                    repo_list.append(component.name)
                    repo_list.append(component.ref)
                    gitHistory = GitLog(repo.dir, args.date)
                    repo_list.append(gitHistory.commitID)
                    repo_list.append(gitHistory.commitDate)
                    if args.action == "check":
                        release_notes = ReleaseNotesCheck(component.name, manifest.build.version, repo.dir)
                        repo_list.append(release_notes.check())
                    value_matrix.append(repo_list)

    writer.write_table()
    writer.dump("table.md")
    return 0


if __name__ == "__main__":
    main()
