# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging

from validation_workflow.validation_rpm import ValidationRpm
from validation_workflow.validation_tar import ValidationTar
from validation_workflow.validation_yum import ValidationYum


class ValidationArgs:
    SUPPORTED_DISTRIBUTIONS = [
        "tar",
        "yum",
        "rpm"
    ]
    SUPPORTED_PLATFORMS = ["linux"]
    SUPPORTED_ARCHITECTURES = [
        "x64",
        "arm64",
    ]
    DISTRIBUTION_MAP = {
        "tar": ValidationTar,
        "yum": ValidationYum,
        "rpm": ValidationRpm
    }

    version: str

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Download Artifacts.")
        parser.add_argument(
            "version",
            type=str,
            help="Product version to validate"
        )
        parser.add_argument(
            "-d",
            "--distribution",
            type=str,
            choices=self.SUPPORTED_DISTRIBUTIONS,
            help="Distribution to validate.",
            default="tar",
            dest="distribution"
        )
        parser.add_argument(
            "-p",
            "--platform",
            type=str,
            choices=self.SUPPORTED_PLATFORMS,
            help="Platform to validate.",
            default="linux"
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
        self.version = args.version
        self.logging_level = args.logging_level
        self.distribution = args.distribution
        self.platform = args.platform
        self.projects = ["opensearch", "opensearch-dashboards"]
