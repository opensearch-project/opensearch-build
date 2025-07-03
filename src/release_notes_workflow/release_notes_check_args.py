# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import datetime
import logging
import os
from typing import IO, List


class ReleaseNotesCheckArgs:
    action: str
    manifest: List[IO]
    date: str
    output: str

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
        
        # AI-powered release notes options
        parser.add_argument(
            "--ai",
            action="store_true",
            help="Generate AI-powered release notes using AWS Bedrock"
        )
        parser.add_argument(
            "--ai-model",
            default="claude-3-7-sonnet",
            help="AI model to use for analysis (default: claude-3-7-sonnet)"
        )
        parser.add_argument(
            "--baseline-date",
            help="Baseline date for commit analysis (format: YYYY-MM-DD)"
        )
        parser.add_argument(
            "--test-mode",
            action="store_true",
            help="Test mode: only read from GitHub, no write operations (branches, commits, PRs)"
        )
        parser.add_argument(
            "--component",
            help="Process only a specific component (optional)"
        )
        
        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.action = args.action
        self.manifest = args.manifest
        self.date = args.date
        self.output = args.output
        
        # AI options
        self.ai = args.ai
        self.ai_model = args.ai_model
        self.baseline_date = args.baseline_date
        self.test_mode = args.test_mode
        self.component = args.component
        
        # GitHub access using existing OpenSearch build system pattern
        self.github_token = os.environ.get('GITHUB_TOKEN')
        if not self.github_token:
            logging.warning("GITHUB_TOKEN environment variable not set. GitHub API calls may fail.")
        
        if self.action == "check" and self.date is None:
            parser.error("check option requires --date argument")
