# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging


class ManifestsArgs:

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Manifest management"
        )
        parser.add_argument(
            "action",
            choices=['list', 'update'],
            help="Operation to perform.",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="Show more verbose output.",
            action="store_const",
            default=logging.INFO,
            const=logging.DEBUG,
            dest="logging_level",
        )
        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.action = args.action
