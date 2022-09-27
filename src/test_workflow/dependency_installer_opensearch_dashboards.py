# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer import DependencyInstaller


class DependencyInstallerOpenSearchDashboards(DependencyInstaller):

    def __init__(self, root_url: str, build_manifest: BuildManifest, bundle_manifest: BundleManifest) -> None:
        super().__init__(root_url, build_manifest, bundle_manifest)
