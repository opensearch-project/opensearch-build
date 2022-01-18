# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.ci_check_package import CiCheckPackage


class CiCheckNpmPackageVersion(CiCheckPackage):
    @property
    def checked_version(self):
        if self.component.name == "OpenSearch-Dashboards":
            return self.target.opensearch_version.replace('-SNAPSHOT', '')
        else:
            return self.target.component_version.replace('-SNAPSHOT', '')

    def check(self):
        self.properties.check_value("version", self.checked_version)
        logging.info(f"Checked {self.component.name} ({self.checked_version}).")
