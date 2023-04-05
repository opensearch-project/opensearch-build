# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
import textwrap


class ValidationArgs:
    SUPPORTED_PLATFORMS = ["linux"]
    DOCKER_SOURCE = ["dockerhub", "ecr"]

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Validation Framework for Validation Workflow.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''\
                Example :   ./validation.sh --version 2.3.0 --distribution rpm --platform linux
                            ./validation.sh --version 2.3.0 --distribution docker --os_build_number 6039 --osd_build_number 4104
        '''))
        parser.add_argument(
            "--version",
            type=str,
            required=True,
            help="(manadatory) Product version to validate"
        )
        parser.add_argument(
            "-d",
            "--distribution",
            type=str,
            help="(optional) Distribution to validate.",
            default="tar",
            dest="distribution"
        )
        parser.add_argument(
            "-p",
            "--platform",
            type=str,
            choices=self.SUPPORTED_PLATFORMS,
            help="(optional) Platform to validate.",
            default="linux"
        )
        parser.add_argument(
            "--os_build_number",
            type=str,
            required=False,
            help="(optional) The opensearchstaging OpenSearch image build number if required, for example : 6039\n",
            default="",
            dest="os_build_number",
        )
        parser.add_argument(
            "--osd_build_number",
            type=str,
            required=False,
            help="(optional) The opensearchstaging OpenSearchDashboard image build number if required, for example : 4104\n",
            default="",
            dest="osd_build_number",
        )
        parser.add_argument(
            "--docker_source",
            type=str,
            required=False,
            choices=self.DOCKER_SOURCE,
            help="(optional) Where to pull the docker image from, either DockerHub or ECR\n",
            default="dockerhub",
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
        parser.add_argument(
            "-a",
            "--arch",
            help="Choose the architecture.",
            choices=["x64", "arm64"],
            default="x64"
        )

        args = parser.parse_args()
        self.version = args.version
        self.logging_level = args.logging_level
        self.distribution = args.distribution
        self.platform = args.platform
        self.projects = ["opensearch", "opensearch-dashboards"]
        self.arch = args.arch
        self.OS_image = 'opensearchproject/opensearch'
        self.OSD_image = 'opensearchproject/opensearch-dashboards'
        self.os_build_number = args.os_build_number
        self.osd_build_number = args.osd_build_number
        self.docker_source = args.docker_source

    def stg_tag(self, image_type: str) -> str:
        return " ".join(
            filter(
                None,
                [
                    self.version,
                    "." + self.os_build_number if (self.os_build_number != "") and (image_type == "opensearch") else None,
                    "." + self.osd_build_number if (self.osd_build_number != "") and (image_type == "opensearch_dashboards") else None,
                ],
            )
        )
