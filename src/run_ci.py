#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import re
import sys

from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_input_manifest import CiInputManifest
from ci_workflow.ci_test_manifest import CiTestManifest
from system import console


def main():
    args = CiArgs()
    console.configure(level=args.logging_level)

    if __is_test_manifest(args.manifest.name):
        CiTestManifest(args.manifest).check()
    else:
        CiInputManifest(args.keep, args.snapshot, args.component, args.manifest, args.component_command).check()


def __is_test_manifest(path):
    return re.search("-test.yml$", path)


if __name__ == "__main__":
    sys.exit(main())
