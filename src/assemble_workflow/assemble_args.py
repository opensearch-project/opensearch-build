# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
from typing import IO

class AssembleArgs:
    manifest: IO
    keep: bool

    def __init__(self) -> None:

        def check_positive(value) -> int:
            int_value = int(value)
            if int_value <= 0:
                raise argparse.ArgumentTypeError(f"{value} is invalid, you must enter a positive integer")
            return str(int_value)

        parser = argparse.ArgumentParser(description="Assemble an OpenSearch Distribution")
        parser.add_argument("manifest", type=argparse.FileType("r"), help="Manifest file.")
        parser.add_argument("-b", "--base-url", dest="base_url", help="The base url to download the artifacts.")
        parser.add_argument(
            "-r",
            "--release-iteration",
            dest="release_iteration",
            type=check_positive,
            default="1",
            help="The release/iteration number of deb/rpm packages, allow multiple revision of same package version (e.g. 2.0.0-1, 2.0.0-2, 2.0.0-3)"
        )
        parser.add_argument(
            "--keep",
            dest="keep",
            action="store_true",
            help="Do not delete the working temporary directory.",
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
        self.manifest = args.manifest
        self.keep = args.keep
        self.base_url = args.base_url
        self.release_iteration = args.release_iteration
