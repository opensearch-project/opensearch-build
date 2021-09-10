# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.check_gradle_dependencies import CheckGradleDependencies


class CheckGradleDependenciesProjectOpenSearchVersion(CheckGradleDependencies):
    def check(self):
        self.dependencies.check_value(
            "org.opensearch:opensearch", self.opensearch_version
        )
        logging.info(
            f"Checked {self.component.name} OpenSearch dependency ({self.opensearch_version})."
        )


class CheckGradleDependenciesOpenSearchVersion(
    CheckGradleDependenciesProjectOpenSearchVersion
):
    def __init__(self, component, git_repo, version, arch, snapshot):
        super().__init__(
            component, git_repo, version, arch, snapshot, gradle_project=None
        )


class CheckGradlePluginDependenciesOpenSearchVersion(
    CheckGradleDependenciesProjectOpenSearchVersion
):
    def __init__(self, component, git_repo, version, arch, snapshot):
        super().__init__(
            component, git_repo, version, arch, snapshot, gradle_project="plugin"
        )
