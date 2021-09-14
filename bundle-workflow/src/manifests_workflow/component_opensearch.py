# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

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
        return ComponentOpenSearch(
            name,
            GitRepository(
                f"https://github.com/opensearch-project/{name}.git",
                branch,
                path,
                working_directory,
            ),
            opensearch_version,
            snapshot,
        )

    def __init__(self, name, repo, opensearch_version, snapshot=False):
        super().__init__(name, repo, snapshot)
        self.opensearch_version = opensearch_version

    def get_properties(self):
        cmd = self.gradle_cmd(
            "properties",
            {
                "opensearch.version": self.opensearch_version,
                "build.snapshot": str(self.snapshot).lower(),
            },
        )
        return PropertiesFile(self.git_repo.output(cmd))

    @property
    def version(self):
        return self.get_properties().get_value("version")
