# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
from pathlib import Path
from typing import List


class SignArgs:
    ACCEPTED_SIGNATURE_FILE_TYPES = [".sig", ".asc"]
    ACCEPTED_PLATFORM = ["linux", "windows"]

    target: Path
    components: List[str]
    type: str
    sigtype: str
    platform: str

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Sign artifacts")
        parser.add_argument("target", type=Path, help="Path to local manifest file or artifact directory")
        parser.add_argument("-c", "--component", type=str, nargs='*', dest="components", help="Component or components to sign")
        parser.add_argument("--type", help="Artifact type")
        parser.add_argument("--sigtype", choices=self.ACCEPTED_SIGNATURE_FILE_TYPES, help="Type of signature file.", default=".asc")
        parser.add_argument("--platform", choices=self.ACCEPTED_PLATFORM, help="Distribution platform.", default="linux")
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
        self.target = args.target
        self.type = args.type
        self.sigtype = args.sigtype
        self.components = args.components
        self.platform = args.platform
