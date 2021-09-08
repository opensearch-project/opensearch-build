# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from ci_workflow.check_gradle_dependencies_open_search import (
    CheckGradleDependenciesOpenSearchVersion,
    CheckGradlePluginDependenciesOpenSearchVersion)
from ci_workflow.check_gradle_properties_version import \
    CheckGradlePropertiesVersion
from ci_workflow.check_gradle_publish_to_maven_local import \
    CheckGradlePublishToMavenLocal

"""
This class is responsible for sanity checking the OpenSearch bundle.
"""


class Ci:
    CHECKS = {
        "gradle:properties:version": CheckGradlePropertiesVersion,
        "gradle:dependencies:opensearch.version": CheckGradleDependenciesOpenSearchVersion,
        "gradle:plugin.dependencies:opensearch.version": CheckGradlePluginDependenciesOpenSearchVersion,
        "gradle:publish": CheckGradlePublishToMavenLocal,
    }

    class InvalidCheckError(Exception):
        def __init__(self, check):
            self.check = check
            super().__init__(
                f"Invalid check {check}, must be one of {Ci.CHECKS.keys()}."
            )

    def __init__(self, component, git_repo):
        """
        Construct a new instance of Ci.
        :param component: The component to sanity-check.
        :param git_repo: A GitRepository instance containing the checked-out code.
        """

        self.component = component
        self.git_repo = git_repo

    def check(self, version, arch, snapshot):
        for check in self.component.checks:
            klass = Ci.CHECKS[check]
            if klass is None:
                raise Ci.InvalidCheckError(check)
            instance = klass(self.component, self.git_repo, version, arch, snapshot)
            instance.check()
