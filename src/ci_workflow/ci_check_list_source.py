# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from ci_workflow.ci_check_gradle_dependencies_opensearch import CiCheckGradleDependenciesOpenSearchVersion
from ci_workflow.ci_check_gradle_properties_version import CiCheckGradlePropertiesVersion
from ci_workflow.ci_check_gradle_publish_to_maven_local import CiCheckGradlePublishToMavenLocal
from ci_workflow.ci_check_list import CiCheckList
from git.git_repository import GitRepository


class CiCheckListSource(CiCheckList):
    def checkout(self, work_dir):
        self.git_repo = GitRepository(
            self.component.repository, self.component.ref, os.path.join(work_dir, self.component.name), self.component.working_directory
        )

        return super().checkout(work_dir)

    CHECKS = {
        "gradle:properties:version": CiCheckGradlePropertiesVersion,
        "gradle:dependencies:opensearch.version": CiCheckGradleDependenciesOpenSearchVersion,
        "gradle:publish": CiCheckGradlePublishToMavenLocal,
    }

    class InvalidCheckError(Exception):
        def __init__(self, check):
            self.check = check
            super().__init__(f"Invalid check: {check.name}, must be one of {CiCheckListSource.CHECKS.keys()}.")

    def check(self):
        for check in self.component.checks:
            klass = CiCheckListSource.CHECKS.get(check.name, None)
            if klass is None:
                raise CiCheckListSource.InvalidCheckError(check)
            instance = klass(self.component, self.git_repo, self.target, check.args)
            instance.check()
