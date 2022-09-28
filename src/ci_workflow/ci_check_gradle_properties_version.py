# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.ci_check_gradle_properties import CiCheckGradleProperties


class CiCheckGradlePropertiesVersion(CiCheckGradleProperties):
    @property
    def checked_version(self) -> str:
        if self.component.name == "OpenSearch":
            return self.target.opensearch_version
        else:
            return self.target.component_version

    def check(self) -> None:
        self.properties.check_value("version", self.checked_version)
        logging.info(f"Checked {self.component.name} ({self.checked_version}).")
