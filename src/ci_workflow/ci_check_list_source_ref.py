# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

from ci_workflow.ci_check_list import CiCheckList
from git.git_repository import GitRepository


class CiCheckListSourceRef(CiCheckList):
    class MissingRefError(Exception):
        def __init__(self, url: str, ref: str) -> None:
            super().__init__(f"Missing {url}@{ref}.")

    def checkout(self, work_dir: str) -> None:

        # If ref is commit id, checkout the repository instead, as ls-remote does not allow non-branch/non-tag to be checked
        if self.component_ref_is_sha1:
            self.git_repo = GitRepository(
                self.component.repository, self.component.ref, os.path.join(work_dir, self.component.name), self.component.working_directory
            )

        return super().checkout(work_dir)

    def check(self) -> None:
        logging.info(f"Checking {self.component.repository} at {self.component.ref}.")

        if self.component_ref_is_sha1:
            logging.info(f"Detect {self.component.name} with ref {self.component.ref} in sha1 format, treat as commit.")
            results = subprocess.check_output(f"git cat-file -t {self.component.ref}", shell=True, cwd=self.git_repo.working_directory).decode().strip().split("\t")
            check_failure = False if len(results) == 1 and results[0] == 'commit' else True
        else:
            logging.info(f"Treat {self.component.name} with ref {self.component.ref} as branch/tag since it is not sha1 commit")
            results = subprocess.check_output(f"git ls-remote {self.component.repository} {self.component.ref}", shell=True).decode().strip().split("\t")
            check_failure = True if len(results) != 2 else False

        if check_failure:
            raise CiCheckListSourceRef.MissingRefError(self.component.repository, self.component.ref)
        else:
            if self.component_ref_is_sha1:
                logging.info(f"Found {self.component.repository} at {self.component.ref}.")
            else:
                logging.info(f"Found {self.component.repository} at {self.component.ref} ({results[0]}).")
