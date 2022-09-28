# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import re
from typing import Any

from ci_workflow.ci_check import CiCheckSource
from ci_workflow.ci_target import CiTarget
from git.git_repository import GitRepository
from manifests.input_manifest import InputComponent
from system.properties_file import PropertiesFile


class CiCheckGradleDependencies(CiCheckSource):
    def __init__(self, component: InputComponent, git_repo: GitRepository, target: CiTarget, args: Any) -> None:
        super().__init__(component, git_repo, target, args)
        self.gradle_project = args if args else None
        self.dependencies = self.__get_dependencies()

    def __get_dependencies(self) -> PropertiesFile:
        cmd = " ".join(
            filter(
                None,
                [
                    f"./gradlew {self.gradle_project or ''}:dependencies",
                    f"-Dopensearch.version={self.target.opensearch_version}",
                    f"-Dbuild.snapshot={str(self.target.snapshot).lower()}",
                    f"-Dbuild.version_qualifier={str(self.target.qualifier)}" if self.target.qualifier else None,
                    "--configuration compileOnly",
                    '| grep -e "---"',
                ]
            )
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
