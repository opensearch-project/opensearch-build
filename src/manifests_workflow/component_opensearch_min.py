# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any, List

from git.git_repository import GitRepository
from manifests_workflow.component import Component
from manifests_workflow.component_opensearch import ComponentOpenSearch
from system.properties_file import PropertiesFile
import os


class ComponentOpenSearchMin(Component):
    def __init__(self, repo: GitRepository, snapshot: bool = False) -> None:
        super().__init__(
            "OpenSearch",
            repo,
            snapshot,
            ["gradle:publish", "gradle:properties:version"],
        )

    @classmethod
    def branches(self, url: str = "https://github.com/opensearch-project/OpenSearch.git") -> List[str]:
        return Component.branches(url)

    @classmethod
    def checkout(self, path: str, branch: str = "main", snapshot: bool = False) -> 'ComponentOpenSearchMin':
        self.path = path
        return ComponentOpenSearchMin(
            GitRepository("https://github.com/opensearch-project/OpenSearch.git", branch, path),
            snapshot,
        )

    @property
    def properties(self) -> PropertiesFile:
        min_comp_version_path = os.path.join(self.path, "buildSrc", "src", "main", "resources", "minimumCompilerVersion")
        # Trying to read the minimumCompilerVersion file
        # And force gradle to apply java home path defined with env var JAVA<Version>_HOME, i.e. JAVA11_HOME
        # If file is not found then fallback to the default java home defined by host
        with open(min_comp_version_path, "r") as file:
            min_comp_version = file.read().strip()
            java_home_path = os.getenv(f"JAVA{min_comp_version}_HOME", None)
            if java_home_path is None:
                cmd = ComponentOpenSearch.gradle_cmd("properties", {"build.snapshot": str(self.snapshot).lower()})
            else:
                cmd = ComponentOpenSearch.gradle_cmd("properties", {"build.snapshot": str(self.snapshot).lower(), "org.gradle.java.home": java_home_path})
            return PropertiesFile(self.git_repo.output(cmd))

    @property
    def version(self) -> Any:
        return self.properties.get_value("version")
