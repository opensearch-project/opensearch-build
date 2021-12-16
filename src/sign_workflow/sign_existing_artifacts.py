#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
from pathlib import Path

from sign_workflow.signer import Signer


class SignExistingArtifacts:

    def __init__(self, artifact_path, signature_type):
        self.artifact_path = artifact_path
        self.signature_type = signature_type

    def __setattr__(self, name, value):
        if name == 'artifact_path' and not isinstance(value, Path):
            raise TypeError('SignExistingArtifacts.artifact_path must of type Path')
        super().__setattr__(name, value)

    def sign_using_manifest(self):

        if self.artifact_path.is_file():
            artifacts = [self.artifact_path.name]
            basename = self.artifact_path.parent
        else:
            artifacts = [artifact.name for artifact in self.artifact_path.iterdir() if artifact.is_file()]
            basename = self.artifact_path

        signer = Signer()

        signer.sign_artifacts(artifacts, basename, self.signature_type)

        logging.info("Done.")
