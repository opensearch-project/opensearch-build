#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import sys

from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_manifests import CiManifests
from system import console


def main() -> int:
    args = CiArgs()
    console.configure(level=args.logging_level)
    CiManifests.from_file(args.manifest, args).check()
    return 0


if __name__ == "__main__":
    sys.exit(main())
