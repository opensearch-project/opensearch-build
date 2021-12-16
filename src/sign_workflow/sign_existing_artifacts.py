#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from pathlib import Path

from sign_workflow.signer import Signer


class SignExistingArtifacts:

    def __init__(self, artifact_path: Path, signature_type):
        self.artifact_path = artifact_path
        self.signature_type = signature_type

    def sign_existing_manifest(self):
        if self.artifact_path.is_file():
            self.sign_single_artifacts()
        else:
            self.sign_all_artifacts_in_dir()
        logging.info("Done.")

    def sign_single_artifacts(self):
        signer = Signer()
        artifacts = [self.artifact_path.name]
        basename = self.artifact_path.parent
        signer.sign_artifacts(artifacts, basename, self.signature_type)

    def sign_all_artifacts_in_dir(self):
        signer = Signer()
        files_map = {}
        for subdir, dirs, files in os.walk(self.artifact_path):
            for file in files:
                if subdir in files_map:
                    files_map[subdir].append(file)
                else:
                    files_map[subdir] = [file]

        for basename, artifact_list in files_map.items():
            signer.sign_artifacts(artifact_list, basename, self.signature_type)
