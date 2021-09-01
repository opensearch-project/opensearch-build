# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import sys


class BuildArgs:
    manifest: str
    snapshot: bool
    component: str
    keep: bool

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
        args = parser.parse_args()
        self.manifest = args.manifest
        self.snapshot = args.snapshot
        self.component = args.component
        self.keep = args.keep
        self.script_path = sys.argv[0].replace("/src/build.py", "/build.sh")

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
