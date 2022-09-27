#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import sys

from manifests_workflow.manifests_args import ManifestsArgs
from system import console


def main() -> int:
    args = ManifestsArgs()
    console.configure(level=args.logging_level)

    if args.action == "list":
        for klass in args.manifests:
            for manifest in klass().values():
                logging.info(f"{manifest.build.name} {manifest.build.version}")
    elif args.action == "update":
        for klass in args.manifests:
            klass().update(keep=args.keep)

    logging.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
