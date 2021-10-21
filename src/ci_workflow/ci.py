# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from ci_workflow.ci_check_gradle_dependencies_opensearch import CiCheckGradleDependenciesOpenSearchVersion
from ci_workflow.ci_check_gradle_properties_version import CiCheckGradlePropertiesVersion
from ci_workflow.ci_check_gradle_publish_to_maven_local import CiCheckGradlePublishToMavenLocal

"""
This class is responsible for sanity checking the OpenSearch bundle.
"""


class Ci:
    CHECKS = {
        "gradle:properties:version": CiCheckGradlePropertiesVersion,
        "gradle:dependencies:opensearch.version": CiCheckGradleDependenciesOpenSearchVersion,
        "gradle:publish": CiCheckGradlePublishToMavenLocal,
    }

    class InvalidCheckError(Exception):
        def __init__(self, check):
            self.check = check
            super().__init__(f"Invalid check {check}, must be one of {Ci.CHECKS.keys()}.")

    def __init__(self, component, git_repo, target):
        """
        Construct a new instance of Ci.
        :param component: The component to sanity-check.
        :param git_repo: A GitRepository instance containing the checked-out code.
        :param target: Ci target.
        """

        self.component = component
        self.git_repo = git_repo
        self.target = target

    def check(self):
        for check in self.component.checks:
            klass = Ci.CHECKS[check.name]
            if klass is None:
                raise Ci.InvalidCheckError(check)
            instance = klass(self.component, self.git_repo, self.target, check.args)
            instance.check()
