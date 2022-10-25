# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import re
import subprocess
from typing import Any, List

from git.git_repository import GitRepository
from manifests.manifest import Manifest


class Component:
    def __init__(self, name: str, repo: GitRepository, snapshot: bool = False, checks: List = []) -> None:
        self.name = name
        self.git_repo = repo
        self.snapshot = snapshot
        self.checks = checks

    @classmethod
    def branches(self, url: str) -> List[str]:
        """Return main or any x.y branches."""
        branches = ["main"]
        remote_branches = subprocess.check_output(f"git ls-remote {url} refs/heads/* | cut -f2 | cut -d/ -f3", shell=True).decode().split("\n")
        branches.extend(filter(lambda b: re.match(r"[\d]+.[\dx]*", b), remote_branches))
        return branches

    def to_dict(self) -> Any:
        return Manifest.compact({
            "name": self.name,
            "repository": self.git_repo.url,
            "ref": self.git_repo.ref,
            "checks": self.checks
        })
