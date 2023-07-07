#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import platform
from pathlib import Path

from sign_workflow.signer import Signer

"""
This class is responsible for signing macos artifacts using the OpenSearch-signer-client and verifying its signature.
"""


class SignerMac(Signer):
    ACCEPTED_FILE_TYPES = [".pkg", ".dmg", ".dylib"]

    def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signed_filename = filename if self.overwrite else os.path.join(basepath, "signed_" + artifact)
        self.sign(artifact, basepath, signature_type)
        self.verify(signed_filename)

    def is_valid_file_type(self, file_name: str) -> bool:
        return any(
            file_name.endswith(x) for x in SignerMac.ACCEPTED_FILE_TYPES
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
            "mac",
            "-r",
            str(self.overwrite)
        ]
        self.git_repo.execute(" ".join(signing_cmd))

    def verify(self, filename: str) -> None:
        if platform.system() != 'Darwin':
            raise OSError(f"Cannot verify mac artifacts on non-Darwin system, {platform.system()}")
        else:
            if (filename.endswith('.pkg')):
                verify_cmd = ["pkgutil", "--check-signature", filename]
            else:
                verify_cmd = ["codesign", "--verify", "--deep", "--verbose=4", "--display", filename]
            self.git_repo.execute(" ".join(verify_cmd))
