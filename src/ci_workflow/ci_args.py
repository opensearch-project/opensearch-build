# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import io
import logging
import sys
from typing import List


class CiArgs:
    manifest: io.TextIOWrapper
    snapshot: bool
    components: List[str]

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Sanity test the OpenSearch Bundle")
        parser.add_argument("manifest", type=argparse.FileType("r"), help="Manifest file.")
        parser.add_argument(
            "-s",
            "--snapshot",
            action="store_true",
            default=False,
            help="Build snapshot.",
        )
        parser.add_argument(
            "-c",
            "--component",
            type=str,
            dest="components",
            nargs='*',
            help="Rebuild one or more components."
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
        self.manifest = args.manifest
        self.snapshot = args.snapshot
        self.components = args.components
        self.keep = args.keep
        self.logging_level = args.logging_level
        self.script_path = sys.argv[0].replace("/src/run_ci.py", "/ci.sh")

    def component_command(self, name: str) -> str:
        return " ".join(
            filter(
                None,
                [
                    self.script_path,
                    self.manifest.name,
                    f"--component {name}",
                    "--snapshot" if self.snapshot else None,
                ],
            )
        )
