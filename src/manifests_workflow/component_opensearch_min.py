# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from git.git_repository import GitRepository
from manifests_workflow.component import Component
from manifests_workflow.component_opensearch import ComponentOpenSearch
from system.properties_file import PropertiesFile


class ComponentOpenSearchMin(Component):
    def __init__(self, repo, snapshot=False):
        super().__init__(
            "OpenSearch",
            repo,
            snapshot,
            ["gradle:publish", "gradle:properties:version"],
        )

    @classmethod
    def branches(self):
        return Component.branches("https://github.com/opensearch-project/OpenSearch.git")

    @classmethod
    def versions(self, work_dir=None):
        return Component.versions(
            "OpenSearch",
            "https://github.com/opensearch-project/OpenSearch.git",
            work_dir,
        )

    @classmethod
    def checkout(self, path, branch="main", snapshot=False):
        return ComponentOpenSearchMin(
            GitRepository("https://github.com/opensearch-project/OpenSearch.git", branch, path),
            snapshot,
        )

    def publish_to_maven_local(self):
        cmd = ComponentOpenSearch.gradle_cmd("publishToMavenLocal", {"build.snapshot": str(self.snapshot).lower()})
        self.git_repo.execute_silent(cmd)

    @property
    def properties(self):
        cmd = ComponentOpenSearch.gradle_cmd("properties", {"build.snapshot": str(self.snapshot).lower()})
        return PropertiesFile(self.git_repo.output(cmd))

    @property
    def version(self):
        self.publish_to_maven_local()
        return self.properties.get_value("version")
