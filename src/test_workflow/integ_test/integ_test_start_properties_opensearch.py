# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.integ_test.integ_test_start_properties import IntegTestStartProperties


class IntegTestStartPropertiesOpenSearch(IntegTestStartProperties):
    def __init__(self, path):
        super().__init__(path, "builds/opensearch/manifest.yml", "dist/opensearch/manifest.yml")
        self.dependency_installer = DependencyInstallerOpenSearch(self.path, self.build_manifest, self.bundle_manifest)
