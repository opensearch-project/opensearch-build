# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from assemble_workflow.bundle import Bundle
from manifests.build_manifest import BuildComponent
from system.os import current_platform


class BundleOpenSearch(Bundle):
    @property
    def install_plugin_script(self) -> str:
        return "opensearch-plugin.bat" if current_platform() == "windows" else "opensearch-plugin"

    def install_plugin(self, plugin: BuildComponent) -> None:
        tmp_path = self._copy_component(plugin, "plugins")
        cli_path = os.path.join(self.min_dist.archive_path, "bin", self.install_plugin_script)
        self._execute(f"{cli_path} install --batch file:{tmp_path}")
        super().install_plugin(plugin)
