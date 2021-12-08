# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from build_workflow.build_args import BuildArgs
from ci_workflow.ci_check import CiCheckDist
from manifests.build_manifest import BuildManifest


class CiCheckManifestComponent(CiCheckDist):
    class MissingComponentError(Exception):
        def __init__(self, component, url):
            super().__init__(f"Missing {component} in {url}.")

    def check(self):
        for architecture in BuildArgs.SUPPORTED_ARCHITECTURES:
            # Since we only have 'linux' builds now we hard code it to 'linux'
            # Once we have all platform builds we can adding a second loop for 'BuildArgs.SUPPORTED_PLATFORMS'
            url = "/".join([self.component.dist, "linux", architecture, "builds", self.target.name, "manifest.yml"])
            self.build_manifest = BuildManifest.from_url(url)
            if self.component.name in self.build_manifest.components:
                logging.info(f"Found {self.component.name} in {url}.")
            else:
                raise CiCheckManifestComponent.MissingComponentError(self.component.name, url)
