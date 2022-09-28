# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.ci_check_package import CiCheckPackage


class CiCheckNpmPackageVersion(CiCheckPackage):
    @property
    def checked_version(self) -> str:
        if self.component.name == "OpenSearch-Dashboards":
            return self.target.opensearch_version.split("-")[0]
        else:
            return self.target.component_version.split("-")[0]

    def check(self) -> None:
        self.properties.check_value("version", self.checked_version)
        logging.info(f"Checked {self.component.name} ({self.checked_version}).")
