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
    SUPPORTED_PLATFORMS = ["linux"]
    DISTRIBUTION_MAP = {
        "tar": ValidationTar,
        "yum": ValidationYum,
        "rpm": ValidationRpm
    }

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Validation Framework for Validation Workflow.")
        parser.add_argument(
            "--version",
            type=str,
            required=True,
            help="Product version to validate"
        )
        parser.add_argument(
            "-d",
            "--distribution",
            type=str,
            choices=self.DISTRIBUTION_MAP.keys(),
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
            "--stgosbuild",
            type=str,
            required=False,
            help="The opensearchstaging OpenSearch image build number if required, for example : 6039\n",
            default="",
            dest="stgosbuild",
        )
        parser.add_argument(
            "--stgosdbuild",
            type=str,
            required=False,
            help="The opensearchstaging OpenSearchDashboard image build number if required, for example : 4104\n",
            default="",
            dest="stgosdbuild",
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
