# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from ci_workflow.check import Check
from system.properties_file import PropertiesFile


class CheckGradleProperties(Check):
    def __init__(self, component, git_repo, version, arch, snapshot):
        super().__init__(component, git_repo, version, arch, snapshot)
        self.properties = self.__get_properties()

    def __get_properties(self):
        cmd = " ".join(
            [
                "./gradlew properties",
                f"-Dopensearch.version={self.opensearch_version}",
                f"-Dbuild.snapshot={str(self.snapshot).lower()}",
            ]
        )

        return PropertiesFile(self.git_repo.output(cmd))
