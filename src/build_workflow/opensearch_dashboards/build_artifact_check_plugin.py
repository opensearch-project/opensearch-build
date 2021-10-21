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
        opensearch_dashboards_version = re.sub(r"-SNAPSHOT$", "", self.target.opensearch_version)
        match = re.search(rf"^(\w+)-{opensearch_dashboards_version}.zip$", os.path.basename(path))
        if not match:
            raise BuildArtifactCheck.BuildArtifactInvalidError(
                path,
                f"Expected filename to be in the format of pluginName-{opensearch_dashboards_version}.zip.",
            )
        plugin_name = match.group(1)
        with ZipFile(path, "r") as zip:
            data = zip.read(f"opensearch-dashboards/{plugin_name}/opensearch_dashboards.json").decode("UTF-8")
            config = ConfigFile(data)
            try:
                component_version = re.sub(r"-SNAPSHOT$", "", self.target.component_version)
                config.check_value("version", component_version)
                config.check_value("opensearchDashboardsVersion", opensearch_dashboards_version)
            except ConfigFile.CheckError as e:
                raise BuildArtifactCheck.BuildArtifactInvalidError(path, e.__str__())
            logging.info(f'Checked {path} ({config.get_value("version", "N/A")})')
