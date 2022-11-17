# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import sys

from system import console
from validation_workflow.validation_args import ValidationArgs


def main() -> int:

    args = ValidationArgs()

    console.configure(level=args.logging_level)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    dist = args.DISTRIBUTION_MAP.get(args.distribution, None)
    dist.download_artifacts(projects=args.projects, version=args.version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
