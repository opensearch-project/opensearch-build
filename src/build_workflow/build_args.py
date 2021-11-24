# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
import sys


class BuildArgs:
    SUPPORTED_PLATFORMS = ["linux", "darwin", "windows"]
    SUPPORTED_ARCHITECTURES = [
        "x64",
        "arm64",
    ]

    manifest: str
    snapshot: bool
    component: str
    keep: bool
    platform: str
    architecture: str

    def __init__(self):
        parser = argparse.ArgumentParser(description="Build an OpenSearch Bundle")
        parser.add_argument("manifest", type=argparse.FileType("r"), help="Manifest file.")
        parser.add_argument(
            "-l",
            "--lock",
            dest="lock",
            action="store_true",
            default=False,
            help="Generate a stable reference manifest."
        )
        parser.add_argument(
            "-s",
            "--snapshot",
            action="store_true",
            default=False,
            help="Build snapshot.",
        )
        parser.add_argument("-c", "--component", type=str, help="Rebuild a single component.")
        parser.add_argument(
            "--keep",
            dest="keep",
            action="store_true",
            help="Do not delete the working temporary directory.",
        )
        parser.add_argument("-p", "--platform", type=str, choices=self.SUPPORTED_PLATFORMS, help="Platform to build.")
        parser.add_argument("-a", "--architecture", type=str, choices=self.SUPPORTED_ARCHITECTURES, help="Architecture to build.")
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
        self.ref_manifest = args.manifest.name + ".lock" if args.lock else None
        self.snapshot = args.snapshot
        self.component = args.component
        self.keep = args.keep
        self.platform = args.platform
        self.architecture = args.architecture
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
