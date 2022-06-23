#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any, List, Type, Union

from sign_workflow.signer_pgp import SignerPGP
from sign_workflow.signer_windows import SignerWindows
from sign_workflow.signer import Signer

"""
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the same location as the original artifacts.
"""


class Signers:
    TYPES = {
        "windows": SignerWindows,
        "linux": SignerPGP,
    }

    @classmethod
    def from_platform(cls, platform: str) -> Signer:
        klass = cls.TYPES.get(platform, None)
        if not klass:
            raise ValueError(f"Unsupported type of platform for signing: {platform}")
        return klass  # type: ignore[return-value]

    @classmethod
    def create(cls, platform: str) -> Signer:
        klass = cls.from_platform(platform)
        return klass()  # type: ignore[no-any-return, operator]
