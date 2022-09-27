# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import datetime
import logging
from typing import IO


class ReleaseNotesCheckArgs:
    action: str
    manifest: IO
    date: str
    output: str

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Checkout an OpenSearch Bundle and check for CommitID and Release Notes")
        parser.add_argument("action", choices=["check"], help="Operation to perform.")
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
        parser.add_argument(
            "--date",
            type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
            dest="date",
            help="Date to retrieve the commit (in format yyyy-mm-dd, example 2022-07-26)."
        )
        parser.add_argument(
            "--output",
            help="Output file."
        )
        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.action = args.action
        self.manifest = args.manifest
        self.date = args.date
        self.output = args.output
        if self.action == "check" and self.date is None:
            parser.error("check option requires --date argument")
