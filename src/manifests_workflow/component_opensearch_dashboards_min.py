# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from git.git_repository import GitRepository
from manifests_workflow.component import Component
from system.config_file import ConfigFile


class ComponentOpenSearchDashboardsMin(Component):
    def __init__(self, repo, snapshot=False):
        super().__init__("OpenSearch-Dashboards", repo, snapshot, [])

    @classmethod
    def branches(self):
        return Component.branches("https://github.com/opensearch-project/OpenSearch-Dashboards.git")

    @classmethod
    def checkout(self, path, branch="main", snapshot=False):
        with GitRepository(
            "https://github.com/opensearch-project/OpenSearch-Dashboards.git",
            branch,
            path,
        ) as repo:
            return ComponentOpenSearchDashboardsMin(
                repo,
                snapshot,
            )

    @property
    def properties(self):
        path = os.path.join(self.git_repo.working_directory, "package.json")
        return ConfigFile.from_file(path)

    @property
    def version(self):
        return self.properties.get_value("version")
