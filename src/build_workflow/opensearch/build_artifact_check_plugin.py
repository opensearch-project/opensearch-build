# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from zipfile import ZipFile

from build_workflow.build_artifact_check import BuildArtifactCheck
from system.properties_file import PropertiesFile


class BuildArtifactOpenSearchCheckPlugin(BuildArtifactCheck):
    def check(self, path):
        if os.path.splitext(path)[1] != ".zip":
            raise BuildArtifactCheck.BuildArtifactInvalidError(path, "Not a zip file.")
        if not path.endswith(f"-{self.target.component_version}.zip"):
            raise BuildArtifactCheck.BuildArtifactInvalidError(path, f"Expected filename to include {self.target.component_version}.")
        with ZipFile(path, "r") as zip:
            data = zip.read("plugin-descriptor.properties").decode("UTF-8")
            properties = PropertiesFile(data)
            try:
                properties.check_value("version", self.target.component_version)
                properties.check_value("opensearch.version", self.target.version)
            except PropertiesFile.CheckError as e:
                raise BuildArtifactCheck.BuildArtifactInvalidError(path, e.__str__())
            logging.info(f'Checked {path} ({properties.get_value("version", "N/A")})')
