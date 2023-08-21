#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from sign_workflow.signer import Signer
from sign_workflow.signer_jar import SignerJar
from sign_workflow.signer_mac import SignerMac
from sign_workflow.signer_pgp import SignerPGP
from sign_workflow.signer_windows import SignerWindows


class Signers:
    TYPES = {
        "windows": SignerWindows,
        "linux": SignerPGP,
        "mac": SignerMac,
        "jar_signer": SignerJar
    }

    @classmethod
    def from_platform(cls, platform: str) -> Signer:
        klass = cls.TYPES.get(platform, None)
        if not klass:
            raise ValueError(f"Unsupported type of platform for signing: {platform}")
        return klass  # type: ignore[return-value]

    @classmethod
    def create(cls, platform: str, overwrite: bool) -> Signer:
        klass = cls.from_platform(platform)
        return klass(overwrite)  # type: ignore[no-any-return, operator]
