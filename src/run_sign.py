#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from sign_workflow.sign_args import SignArgs
from sign_workflow.sign_artifacts import SignArtifacts
from system import console


def main() -> int:
    args = SignArgs()

    console.configure(level=args.logging_level)

    sign = SignArtifacts.from_path(
        path=args.target,
        components=args.components,
        artifact_type=args.type,
        signature_type=args.sigtype,
        platform=args.platform
    )

    sign.sign()
    return 0


if __name__ == "__main__":
    sys.exit(main())
