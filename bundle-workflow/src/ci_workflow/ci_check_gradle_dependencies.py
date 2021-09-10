# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import re

from ci_workflow.ci_check import CiCheck
from system.properties_file import PropertiesFile


class CiCheckGradleDependencies(CiCheck):
    def __init__(self, component, git_repo, target, gradle_project=None):
        super().__init__(component, git_repo, target)
        self.gradle_project = gradle_project
        self.dependencies = self.__get_dependencies()

    def __get_dependencies(self):
        cmd = " ".join(
            [
                f"./gradlew {self.gradle_project or ''}:dependencies",
                f"-Dopensearch.version={self.target.opensearch_version}",
                f"-Dbuild.snapshot={str(self.target.snapshot).lower()}",
                '| grep -e "---"',
            ]
        )

        lines = self.git_repo.output(cmd)
        stack = ["root"]
        props = PropertiesFile("")
        for line in lines.split("\n"):
            # e.g. "|    +--- org.opensearch:opensearch-core:1.1.0-SNAPSHOT"
            # see job_scheduler_dependencies.txt in tests for an example
            match = re.search(r"---\s(.*):([0-9,\w,.-]*)[\s]*", line)
            if match:
                levels = line.count("   ") + line.count("---")

                while levels < len(stack):
                    del stack[-1]

                if levels == len(stack):
                    stack[-1] = match.group(1).strip()
                elif levels > len(stack):
                    stack.append(match.group(1).strip())

                key = "/".join(stack)
                value = match.group(2).strip()
                logging.debug(f"{key}={value}")
                props[key] = value

        return props
