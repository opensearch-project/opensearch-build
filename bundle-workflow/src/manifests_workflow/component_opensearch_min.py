# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import re
import subprocess

from git.git_repository import GitRepository
from manifests_workflow.component import Component
from system.properties_file import PropertiesFile


class ComponentOpenSearchMin(Component):
    def __init__(self, repo, snapshot=False):
        super().__init__("OpenSearch", repo, snapshot)

    @classmethod
    def get_root_branches(self):
        branches = ["main"]
        remote_branches = (
            subprocess.check_output(
                "git ls-remote https://github.com/opensearch-project/OpenSearch.git refs/heads/* | cut -f2 | cut -d/ -f3",
                shell=True,
            )
            .decode()
            .split("\n")
        )
        branches.extend(filter(lambda b: re.match(r"[\d]+.[\dx]*", b), remote_branches))
        return branches

    @classmethod
    def checkout(self, path, branch="main", snapshot=False):
        return ComponentOpenSearchMin(
            GitRepository(
                "https://github.com/opensearch-project/OpenSearch.git", branch, path
            ),
            snapshot,
        )

    def publish_to_maven_local(self):
        cmd = self.gradle_cmd(
            "publishToMavenLocal", {"build.snapshot": str(self.snapshot).lower()}
        )
        self.git_repo.execute_silent(cmd)

    def get_properties(self):
        cmd = self.gradle_cmd(
            "properties", {"build.snapshot": str(self.snapshot).lower()}
        )
        return PropertiesFile(self.git_repo.output(cmd))

    @property
    def version(self):
        return self.get_properties().get_value("version")
