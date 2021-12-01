# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from test_workflow.dependency_installer import DependencyInstaller


class DependencyInstallerOpenSearchDashboards(DependencyInstaller):

    def __init__(self, root_url, build_manifest, bundle_manifest):
        super().__init__(root_url, build_manifest, bundle_manifest)
