# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
import textwrap

from test_workflow.test_kwargs import TestKwargs


class ValidationArgs:
    SUPPORTED_PLATFORMS = ["linux"]
    DOCKER_SOURCE = ["dockerhub", "ecr"]

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Validation Framework for Validation Workflow.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''\
                Example :   ./validation.sh --version 2.3.0 --distribution rpm --platform linux
                            ./validation.sh --version 2.3.0 --distribution docker --os-build-number 6039 --osd-build-number 4104 --using-staging-artifact-only
                            ./validation.sh --version 2.3.0 --projects opensearch opensearch-dashboards --artifact-type staging
                            ./validation.sh --file-path https://artifacts.opensearch.org/releases/bundle/opensearch/2.3.0/opensearch-2.3.0-linux-x64.tar.gz
        '''))
        parser.add_argument(
            "--version",
            type=str,
            required=False,
            help="(manadatory for production) Product version to validate",
            default=""
        )
        parser.add_argument(
            "--file-path",
            nargs='*',
            action=TestKwargs,
            help="(manadatory for production) Product URL or file-path to validate",
            default={},
            dest="file_path"
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
            "--platform",
            type=str,
            choices=self.SUPPORTED_PLATFORMS,
            help="(optional) Platform to validate.",
            default="linux"
        )
        parser.add_argument(
            "--os-build-number",
            type=str,
            required=False,
            help="(optional) The opensearchstaging OpenSearch image build number if required, for example : 6039\n",
            default="latest",
            dest="os_build_number",
        )
        parser.add_argument(
            "--osd-build-number",
            type=str,
            required=False,
            help="(optional) The opensearchstaging OpenSearchDashboard image build number if required, for example : 4104\n",
            default="latest",
            dest="osd_build_number",
        )
        parser.add_argument(
            "--docker-source",
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
        parser.add_argument(
            "-p",
            "--projects",
            nargs='+',
            help="Enter type of projects to be validated",
            choices=["opensearch", "opensearch-dashboards"],
            default=["opensearch"]
        )
        parser.add_argument(
            "--artifact-type",
            help="Enter type of artifacts that needs to be validated",
            choices=["staging", "production"],
            default="production",
            dest="artifact_type",
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "--validate-digest-only",
            action="store_true",
            default=False,
            help="(optional) Validate digest only; will not run docker to test API")
        group.add_argument(
            "--using-staging-artifact-only",
            action="store_true",
            default=False,
            help="(optional) Use only staging artifact to run docker and API test, will not validate digest")

        args = parser.parse_args()

        if (not (args.version or args.file_path)):
            raise Exception("Provide either version number or File Path")
        if(args.file_path):
            args.distribution = self.get_distribution_type(args.file_path)
            args.projects = args.file_path.keys()
        if (('opensearch' not in args.projects)):
            raise Exception("Missing OpenSearch OpenSearch artifact details! Please provide the same along with OpenSearch-Dashboards to validate")

        self.version = args.version
        self.file_path = args.file_path
        self.artifact_type = args.artifact_type
        self.logging_level = args.logging_level
        self.distribution = args.distribution
        self.platform = args.platform
        self.projects = args.projects
        self.arch = args.arch
        self.OS_image = 'opensearchproject/opensearch'
        self.OSD_image = 'opensearchproject/opensearch-dashboards'
        self.build_number = {"opensearch": args.os_build_number, "opensearch-dashboards": args.osd_build_number}
        self.os_build_number = args.os_build_number
        self.osd_build_number = args.osd_build_number
        self.docker_source = args.docker_source
        self.validate_digest_only = args.validate_digest_only
        self.using_staging_artifact_only = args.using_staging_artifact_only

    def get_distribution_type(self, file_path: dict) -> str:
        if (any("tar" in value for value in file_path.values())):
            return 'tar'
        elif (any("repo" in value for value in file_path.values())):
            return 'yum'
        elif (any("rpm" in value for value in file_path.values())):
            return 'rpm'
        else:
            raise Exception("Provided distribution is not supported")

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
