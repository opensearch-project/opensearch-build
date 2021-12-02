# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import re
from zipfile import ZipFile

from build_workflow.build_artifact_check import BuildArtifactCheck
from system.config_file import ConfigFile


class BuildArtifactOpenSearchDashboardsCheckPlugin(BuildArtifactCheck):
    def check(self, path):
        if os.path.splitext(path)[1] != ".zip":
            raise BuildArtifactCheck.BuildArtifactInvalidError(path, "Not a zip file.")

        match = re.search(r"^(\w+)-[\d\.]*.*.zip$", os.path.basename(path))
        if not match:
            raise BuildArtifactCheck.BuildArtifactInvalidError(path, "Expected filename to be in the format of pluginName-1.1.0.zip.")

        plugin_name = match.group(1)
        valid_filenames = self.__valid_paths(plugin_name)
        if not os.path.basename(path) in valid_filenames:
            raise BuildArtifactCheck.BuildArtifactInvalidError(path, f"Expected filename to to be one of {valid_filenames}.")

        with ZipFile(path, "r") as zip:
            data = zip.read(f"opensearch-dashboards/{plugin_name}/opensearch_dashboards.json").decode("UTF-8")
            config = ConfigFile(data)
            try:
                config.check_value_in("version", self.target.compatible_component_versions)
                config.check_value_in("opensearchDashboardsVersion", self.target.compatible_versions)
            except ConfigFile.CheckError as e:
                raise BuildArtifactCheck.BuildArtifactInvalidError(path, e.__str__())
            logging.info(f'Checked {path} ({config.get_value("version", "N/A")})')

    def __valid_paths(self, pluginName):
        return list(map(lambda version: f"{pluginName}-{version}.zip", self.target.compatible_versions))
