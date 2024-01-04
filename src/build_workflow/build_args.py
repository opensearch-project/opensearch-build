# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
import sys
from typing import IO, List


class BuildArgs:
    SUPPORTED_PLATFORMS = ["linux", "darwin", "windows"]
    SUPPORTED_ARCHITECTURES = [
        "x64",
        "arm64",
    ]
    SUPPORTED_DISTRIBUTIONS = ["tar", "zip", "rpm", "deb"]

    manifest: IO
    snapshot: bool
    components: List[str]
    keep: bool
    platform: str
    architecture: str
    distribution: str
    continue_on_error: bool
    incremental: bool

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Build an OpenSearch Distribution")
        parser.add_argument(
            "manifest",
            type=argparse.FileType("r"),
            help="Manifest file."
        )
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
        parser.add_argument(
            "--keep",
            dest="keep",
            action="store_true",
            help="Do not delete the working temporary directory.",
        )
        parser.add_argument(
            "-p",
            "--platform",
            type=str,
            choices=self.SUPPORTED_PLATFORMS,
            help="Platform to build."
        )
        parser.add_argument(
            "-a",
            "--architecture",
            type=str,
            choices=self.SUPPORTED_ARCHITECTURES,
            help="Architecture to build."
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
        parser.add_argument(
            "-d",
            "--distribution",
            type=str,
            choices=self.SUPPORTED_DISTRIBUTIONS,
            help="Distribution to build.",
            default="tar",
            dest="distribution"
        )
        parser.add_argument(
            "--continue-on-error",
            dest="continue_on_error",
            default=False,
            action="store_true",
            help="Do not fail the distribution build on any plugin component failure.",
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-c",
            "--component",
            dest="components",
            nargs='*',
            type=str,
            help="Rebuild one or more components."
        )
        group.add_argument(
            "-i",
            "--incremental",
            dest="incremental",
            default=False,
            action="store_true",
            help="Given previous build artifacts are present, build incrementally.",
        )

        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.manifest = args.manifest
        self.ref_manifest = args.manifest.name + ".lock" if args.lock else None
        self.snapshot = args.snapshot
        self.components = args.components
        self.keep = args.keep
        self.platform = args.platform
        self.architecture = args.architecture
        self.distribution = args.distribution
        self.script_path = sys.argv[0].replace("/src/run_build.py", "/build.sh")
        self.continue_on_error = args.continue_on_error
        self.incremental = args.incremental

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
