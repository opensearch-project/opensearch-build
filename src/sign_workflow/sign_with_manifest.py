#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from manifests.build_manifest import BuildManifest
from sign_workflow.signer import Signer


class SignWithManifest:

    def __init__(self, manifest_path, component, artifact_type, signature_type):
        self.manifest = BuildManifest.from_file(manifest_path.open("r"))
        self.component = component
        self.artifact_type = artifact_type
        self.signature_type = signature_type

    def sign_using_manifest(self):
        basepath = os.path.dirname(os.path.abspath(self.manifest.name))
        signer = Signer()

        for component in self.manifest.components.select(focus=self.component):
            logging.info(f"Signing {component.name}")

            for component_artifact_type in component.artifacts:
                if self.artifact_type and self.artifact_type != component_artifact_type:
                    continue

                signer.sign_artifacts(component.artifacts[component_artifact_type], basepath, self.signature_type)

        logging.info("Done.")
