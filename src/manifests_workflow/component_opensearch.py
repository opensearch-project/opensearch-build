# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import subprocess

from git.git_repository import GitRepository
from manifests_workflow.component import Component
from system.properties_file import PropertiesFile


class ComponentOpenSearch(Component):
    @classmethod
    def checkout(
        self,
        name,
        path,
        opensearch_version,
        branch="main",
        snapshot=False,
        working_directory=None,
    ):
        with GitRepository(
            f"https://github.com/opensearch-project/{name}.git",
            branch,
            path,
            working_directory,
        ) as repo:
            return ComponentOpenSearch(
                name,
                repo,
                opensearch_version,
                snapshot,
            )

    def __init__(self, name, repo, opensearch_version, snapshot=False):
        super().__init__(name, repo, snapshot)
        self.opensearch_version = opensearch_version

    @property
    def properties(self):
        cmd = ComponentOpenSearch.gradle_cmd(
            "properties",
            {
                "opensearch.version": self.opensearch_version,
                "build.snapshot": str(self.snapshot).lower(),
            },
        )
        return PropertiesFile(self.git_repo.output(cmd))

    @property
    def version(self):
        try:
            return self.properties.get_value("version")
        except subprocess.CalledProcessError as err:
            logging.warn(f"Error getting version of {self.name}: {str(err)}, ignored")
            return None

    @classmethod
    def gradle_cmd(self, target, props={}):
        cmd = [f"./gradlew {target}"]
        cmd.extend([f"-D{k}={v}" for k, v in props.items()])
        return " ".join(cmd)
