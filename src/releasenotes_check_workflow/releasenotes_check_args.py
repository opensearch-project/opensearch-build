# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
from typing import IO


class ReleaseNotesCheckArgs:
    manifest: IO
    gitlogdate: str
    addcomment: bool
    gitlogdate: str
    gitissuenumber: str
    gittoken: str

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Checkout an OpenSearch Bundle and check for CommitID and Release Notes")
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
            "--gitlogdate",
            type=str,
            required=True,
            dest="gitlogdate",
            help="Date to retrive the commit (in format yyyy-mm-dd, example 2022-07-26)."
        )
        parser.add_argument(
            "--addcomment",
            action='store_true',
            default=False,
            help="Github issue add comment",
        )
        parser.add_argument(
            "--gitissuenumber",
            required=False,
            type=str,
            dest="gitissuenumber",
            help="Build repo Git issue number.",
        )
        parser.add_argument(
            "--gittoken",
            required=False,
            type=str,
            dest="gittoken",
            help="GitHub auth Token.",
        )
        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.manifest = args.manifest
        self.addcomment = args.addcomment
        self.gitlogdate = args.gitlogdate
        self.gitissuenumber = args.gitissuenumber
        self.gittoken  = args.gittoken
        print(self.addcomment, self.gitissuenumber, self.gittoken)
        if self.addcomment==True:
            if args.gitissuenumber==None or args.gittoken==None:
                parser.error('The --addcomment argument requires the --gitissuenumber or --gittoken')

