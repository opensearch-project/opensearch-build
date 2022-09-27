#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from pathlib import Path

from sign_workflow.signer import Signer

"""
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the same location as the original artifacts.
"""


class SignerPGP(Signer):

    ACCEPTED_FILE_TYPES = [".zip", ".jar", ".war", ".pom", ".module", ".tar.gz", ".whl", ".crate", ".rpm"]

    def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
        location = os.path.join(basepath, artifact)
        self.sign(artifact, basepath, signature_type)
        self.verify(location + signature_type)

    def is_valid_file_type(self, file_name: str) -> bool:
        return any(
            file_name.endswith(x) for x in SignerPGP.ACCEPTED_FILE_TYPES
        )

    def sign(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signature_file = filename + signature_type
        self.__remove_existing_signature__(signature_file)
        signing_cmd = [
            "./opensearch-signer-client",
            "-i",
            filename,
            "-o",
            signature_file,
            "-p",
            "pgp",
        ]
        self.git_repo.execute(" ".join(signing_cmd))

    def verify(self, filename: str) -> None:
        verify_cmd = ["gpg", "--verify-files", filename]
        self.git_repo.execute(" ".join(verify_cmd))
