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

import semantic_version  # type:ignore


class TestArgs:
    class CheckSemanticVersion(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not semantic_version.validate(values):
                raise ValueError(f"Invalid version number: {values}")
            setattr(namespace, self.dest, values)

    s3_bucket: str
    opensearch_version: str
    build_id: int
    platform: str
    architecture: str
    test_run_id: int
    component: str
    keep: bool
    logging_level: int

    def __init__(self):
        parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
        parser.add_argument("--s3-bucket", type=str, help="S3 bucket name", required=True)
        parser.add_argument(
            "--opensearch-version",
            type=str,
            action=self.CheckSemanticVersion,
            help="OpenSearch version to test",
            required=True,
        )
        parser.add_argument(
            "--build-id",
            type=int,
            help="The build id for the built artifact",
            required=True,
        )
        parser.add_argument(
            "--platform",
            type=str,
            choices=["linux", "darwin", "windows"],
            help="The os name e.g. linux, darwin, windows",
            required=True,
        )
        parser.add_argument(
            "--architecture",
            type=str,
            choices=["x64", "arm64"],
            help="The os architecture e.g. x64, arm64",
            required=True,
        )
        parser.add_argument(
            "--test-run-id",
            type=int,
            help="The unique execution id for the test",
            required=True,
        )
        parser.add_argument("--component", type=str, help="Test a specific component")
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
        self.s3_bucket = args.s3_bucket
        self.opensearch_version = args.opensearch_version
        self.build_id = args.build_id
        self.platform = args.platform
        self.architecture = args.architecture
        self.test_run_id = args.test_run_id
        self.component = args.component
        self.keep = args.keep
        self.logging_level = args.logging_level


TestArgs.__test__ = False  # type:ignore
