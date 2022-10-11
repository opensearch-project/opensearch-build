# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys

from validation_workflow.validation_args import ValidationArgs


def main() -> int:
    ValidationArgs()
    return 0


if __name__ == "__main__":
    sys.exit(main())
