# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
from typing import IO


class CheckoutArgs:
    manifest: IO

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Checkout an OpenSearch Bundle")
        parser.add_argument("manifest", type=argparse.FileType("r"), help="Manifest file.")
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
        self.manifest = args.manifest
