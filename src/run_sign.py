#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
import sys
from pathlib import Path

from sign_workflow.sign_artifacts import SignArtifacts
from sign_workflow.signer import Signer
from system import console

ACCEPTED_SIGNATURE_FILE_TYPES = [".sig"]


def main():
    parser = argparse.ArgumentParser(description="Sign artifacts")
    parser.add_argument("target", type=Path, help="Path to local manifest file or artifact directory.")
    parser.add_argument("--component", nargs="?", help="Component name")
    parser.add_argument("--type", nargs="?", help="Artifact type")
    parser.add_argument("--sigtype", choices=ACCEPTED_SIGNATURE_FILE_TYPES, help="Type of Signature file", default=".asc")
    parser.add_argument("--platform", nargs="?", help="The distribution platform", default="linux")
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

    console.configure(level=args.logging_level)

    sign = SignArtifacts.from_path(path=args.target,
                                   component=args.component,
                                   artifact_type=args.type,
                                   signature_type=args.sigtype,
                                   signer=Signer())

    sign.sign()


if __name__ == "__main__":
    sys.exit(main())
