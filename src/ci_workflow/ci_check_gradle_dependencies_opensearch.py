# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.ci_check_gradle_dependencies import CiCheckGradleDependencies


class CiCheckGradleDependenciesOpenSearchVersion(CiCheckGradleDependencies):
    def check(self) -> None:
        self.dependencies.check_value("org.opensearch:opensearch", self.target.opensearch_version)
        logging.info(f"Checked {self.component.name} OpenSearch dependency ({self.target.opensearch_version}).")
