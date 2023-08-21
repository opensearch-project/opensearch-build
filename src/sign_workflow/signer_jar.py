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
This class is responsible for signing jar and taco files using the OpenSearch-signer-client and verifying its signature.
"""


class SignerJar(Signer):
    ACCEPTED_FILE_TYPES = [".jar", ".taco"]

    def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signed_filename = filename if self.overwrite else os.path.join(basepath, "signed_" + artifact)
        self.sign(artifact, basepath, signature_type)
        self.verify(signed_filename)

    def is_valid_file_type(self, file_name: str) -> bool:
        return any(
            file_name.endswith(x) for x in SignerJar.ACCEPTED_FILE_TYPES
        )

    def sign(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signed_filename = filename if self.overwrite else os.path.join(basepath, "signed_" + artifact)
        signing_cmd = [
            "./opensearch-signer-client",
            "-i",
            filename,
            "-o",
            signed_filename,
            "-p",
            "jar_signer",
            "-r",
            str(self.overwrite)
        ]
        self.git_repo.execute(" ".join(signing_cmd))

    def verify(self, filename: str) -> None:
        verify_cmd = ["jarsigner", "-verify", filename, "-verbose", "-certs", "-strict"]
        signature = self.git_repo.output(" ".join(verify_cmd))
        if signature.find('jar verified') == -1:
            raise ValueError(f"Cannot verify the signature for {filename}")
