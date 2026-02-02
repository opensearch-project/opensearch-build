# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import datetime
import logging
from typing import IO, List


class ReleaseNotesCheckArgs:
    action: str
    manifest: List[IO]
    date: str
    output: str
    model_id: str
    max_tokens: int
    ref: str
    skip_changelog: bool

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Checkout an OpenSearch Bundle and check for CommitID and Release Notes")
        parser.add_argument("action", choices=["check", "compile", "generate"], help="Operation to perform.")
        parser.add_argument("manifest", type=argparse.FileType("r"), nargs='+', help="Manifest file.")
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
        parser.add_argument(
            "-c",
            "--component",
            dest="components",
            nargs='*',
            type=str,
            help="Process one or more components."
        )
        parser.add_argument("--model-id",
                            type=str,
                            default="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                            help="AWS Bedrock model ID to use for AI generation.")
        parser.add_argument("--max-tokens",
                            type=int,
                            default=15000,
                            help="Maximum number of tokens to generate in AI response.")
        parser.add_argument("--ref",
                            type=str,
                            help="Override input manifest ref")
        parser.add_argument("--skip-changelog",
                            action="store_true",
                            help="Skip CHANGELOG.md and generate release notes from commits only")

        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.action = args.action
        self.manifest = args.manifest
        self.date = args.date
        self.output = args.output
        self.model_id = args.model_id
        self.max_tokens = args.max_tokens
        self.ref = args.ref
        self.skip_changelog = args.skip_changelog

        # AI options
        self.components = args.components

        if (self.action == "check" or self.action == 'generate') and self.date is None:
            parser.error("check option requires --date argument")
