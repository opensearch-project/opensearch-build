# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import argparse
import logging


class TestArgs:
    manifest: str
    component: str
    keep: bool

    def __init__(self):
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
        parser.add_argument(
            "manifest", type=argparse.FileType("r"), help="Manifest file."
        )
        parser.add_argument("--component", help="Test a specific component")
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
        self.component = args.component
        self.keep = args.keep
