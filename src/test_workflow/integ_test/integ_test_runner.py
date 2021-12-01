# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch


class IntegTestRunner(abc.ABC):
    def __init__(self, args, test_manifest):
        self.args = args
        self.test_manifest = test_manifest

        self.bundle_manifest = BundleManifest.from_urlpath("/".join([self.args.path.rstrip("/"), "dist/opensearch/manifest.yml"]))
        self.build_manifest = BuildManifest.from_urlpath("/".join([self.args.path.rstrip("/"), "builds/opensearch/manifest.yml"]))
        self.dependency_installer = DependencyInstallerOpenSearch(self.args.path, self.build_manifest, self.bundle_manifest)

    @abc.abstractmethod
    def run(self):
        pass
