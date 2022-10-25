# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import subprocess

from ci_workflow.ci_check_list import CiCheckList


class CiCheckListSourceRef(CiCheckList):
    class MissingRefError(Exception):
        def __init__(self, url: str, ref: str) -> None:
            super().__init__(f"Missing {url}@{ref}.")

    def checkout(self, work_dir: str) -> None:
        return super().checkout(work_dir)

    def check(self) -> None:
        logging.info(f"Checking {self.component.repository} at {self.component.ref}.")
        results = subprocess.check_output(f"git ls-remote {self.component.repository} {self.component.ref}", shell=True).decode().strip().split("\t")
        if len(results) != 2:
            raise CiCheckListSourceRef.MissingRefError(self.component.repository, self.component.ref)
        else:
            logging.info(f"Found {self.component.repository} at {self.component.ref} ({results[0]}).")
