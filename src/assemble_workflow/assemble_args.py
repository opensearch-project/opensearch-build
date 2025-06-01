# Copyright OpenSearch Contributors
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
    dry_run: bool
    generate_manifest: str
    version: str
    platform: str
    arch: str
    dist: str
    component: str
    
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Assemble an OpenSearch Distribution")
        parser.add_argument("manifest", type=argparse.FileType("r"), help="Manifest file.")
        parser.add_argument("-b", "--base-url", dest="base_url", help="The base url to download the artifacts.")
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
        parser.add_argument(
            "--dry-run",
            dest="dry_run",
            action="store_true",
            help="Run assemble logic without actually downloading or extracting.",
        )
        parser.add_argument(
            "--generate-manifest",
            nargs="?",
            const="manifest.yml",
            help="Generate a manifest file dynamically. Default filename is manifest.yml",
        )
        parser.add_argument("--version", help="Version of OpenSearch to include in the manifest.")
        parser.add_argument("--platform", help="Target platform (linux, windows, macos).")
        parser.add_argument("--arch", help="Target architecture (x64, arm64).")
        parser.add_argument("--dist", help="Distribution type (tar, zip, rpm).")
        parser.add_argument("--component", help="Component name (default: opensearch).")
        

        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.manifest = args.manifest
        self.keep = args.keep
        self.base_url = args.base_url
        self.dry_run = args.dry_run
        self.generate_manifest = args.generate_manifest
        self.version = args.version
        self.platform = args.platform
        self.arch = args.arch
        self.dist = args.dist
        self.component = args.component