# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from assemble_workflow.bundle import Bundle


class BundleOpenSearchDashboards(Bundle):
    def install_plugin(self, plugin):
        tmp_path = self._copy_component(plugin, "plugins")
        cli_path = os.path.join(self.archive_path, "bin/opensearch-dashboards-plugin")
        self._execute(f"{cli_path} --allow-root install file:{tmp_path}")
        super().install_plugin(plugin)

    def copy_default_files(self):
        self.__copy_config()
        return super().copy_default_files()

    def __copy_config(self):
        logging.info(f'Copy opensearch_dashboards.yml to {self.archive_path}')
        super().copy_file(
            "../../config/opensearch_dashboards.yml",
            os.path.join(
                self.archive_path, "config"
            )
        )
