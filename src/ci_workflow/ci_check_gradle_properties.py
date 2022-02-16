# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any

from ci_workflow.ci_check import CiCheckSource
from ci_workflow.ci_target import CiTarget
from git.git_repository import GitRepository
from manifests.input_manifest import Component
from system.properties_file import PropertiesFile


class CiCheckGradleProperties(CiCheckSource):
    def __init__(self, component: Component, git_repo: GitRepository, target: CiTarget, args: Any = None) -> None:
        super().__init__(component, git_repo, target, args)
        self.properties = self.__get_properties()

    def __get_properties(self) -> PropertiesFile:
        cmd = " ".join(
            [
                "./gradlew properties",
                f"-Dopensearch.version={self.target.opensearch_version}",
                f"-Dbuild.snapshot={str(self.target.snapshot).lower()}",
            ]
        )

        return PropertiesFile(self.git_repo.output(cmd))
