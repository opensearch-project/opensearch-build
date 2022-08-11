# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import Any, List

from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_component import ComponentReleaseNotes
from release_notes_workflow.release_notes_gitlog import GitLog
from system.temporary_directory import TemporaryDirectory


class ReleaseNotes:

    def __init__(self, component: InputComponentFromSource, manifest: InputManifest, date: str) -> None:
        self.component = component
        self.manifest = manifest
        self.date = date

    def checkout(self, work_dir: TemporaryDirectory) -> Any:
        logging.info(f"Checking out into {work_dir.name}")
        logging.info(f"Checking out {self.component.name}")
        if type(self.component) is InputComponentFromSource:
            with GitRepository(
                    self.component.repository,
                    self.component.ref,
                    os.path.join(work_dir.name, self.component.name),
                    self.component.working_directory,
            )as repo:
                logging.debug(f"Checked out {self.component.name} into {repo.dir}")
        return repo.dir

    def check(self) -> List:
        results = []
        with TemporaryDirectory(chdir=True) as work_dir:
            logging.info(f"Checking out into {work_dir.name}")
            results.append(self.component.name)
            results.append(self.component.ref)
            repo_dir = ReleaseNotes.checkout(self, work_dir)
            manifest_check = ComponentReleaseNotes(self.component.name, self.manifest.build.version, repo_dir)
            manifest_check.from_component()
            gitHistory = GitLog(repo_dir, self.date)
            results.append(gitHistory.commitID)
            results.append(gitHistory.commitDate)
            results.append(manifest_check.check())
        return results
