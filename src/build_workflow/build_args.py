# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
import sys


class BuildArgs:
    manifest: str
    snapshot: bool
    component: str
    keep: bool
    platform: str
    arch: str

    def __init__(self):
        parser = argparse.ArgumentParser(description="Build an OpenSearch Bundle")
        parser.add_argument(
            "manifest", type=argparse.FileType("r"), help="Manifest file."
        )
        parser.add_argument(
            "-s",
            "--snapshot",
            action="store_true",
            default=False,
            help="Build snapshot.",
        )
        parser.add_argument(
            "-c", "--component", type=str, help="Rebuild a single component."
        )
        parser.add_argument(
            "--keep",
            dest="keep",
            action="store_true",
            help="Do not delete the working temporary directory.",
        )
        parser.add_argument(
            "-p", "--platform", type=str, help="Platform to build."
        )
        parser.add_argument(
            "-a", "--arch", type=str, help="Architecture to build."
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
        self.snapshot = args.snapshot
        self.component = args.component
        self.keep = args.keep
        self.platform = args.platform
        self.arch = args.arch
        self.script_path = sys.argv[0].replace("/src/run_build.py", "/build.sh")

    def component_command(self, name):
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
