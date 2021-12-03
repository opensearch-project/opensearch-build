# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards
from test_workflow.integ_test.service_start_properties import ServiceStartProperties


class ServiceStartPropertiesOpenSearchDashboards(ServiceStartProperties):
    def __init__(self, path):
        super().__init__(path, "builds/opensearch-dashboards/manifest.yml", "dist/opensearch-dashboards/manifest.yml")
        self.dependency_installer = DependencyInstallerOpenSearchDashboards(self.path, self.build_manifest, self.bundle_manifest)
