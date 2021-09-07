# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.check_gradle_properties import CheckGradleProperties


class CheckGradlePropertiesVersion(CheckGradleProperties):
    def check(self):
        self.properties.check_value("version", self.component_version)
        logging.info(f"Checked {self.component.name} ({self.component_version}).")
