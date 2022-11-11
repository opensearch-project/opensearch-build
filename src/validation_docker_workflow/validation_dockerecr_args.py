# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging


class DockerEcrArgs():

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description='Validating OpenSearch(OS) & OpenSearchDashboard(OSD) distribution build between opensearchproject and opensearchstaging at dockerHub/ECR\n',
            epilog='Example : ./checkdocker.sh 2.3.0 2.3.0 --stgosbuild 6039 --stgosdbuild 4104\n'
        )
        parser.add_argument(
            "OS_image_version",
            type=str,
            help="The opensearchproject OpenSearch image <version> that we want to validate, for example : 2.3.0 \n",
        )
        parser.add_argument(
            "OSD_image_version",
            type=str,
            help="The opensearchproject OpenSearchDashboard image <version> that we want to validate, for example : 2.3.0 \n",
        )
        parser.add_argument(
            "--stgosbuild",
            type=str,
            default="",
            required=False,
            help="The opensearchstaging OpenSearch image build number if required, for example : 6039\n",
            dest="stgosbuild",
        )
        parser.add_argument(
            "--stgosdbuild",
            type=str,
            default="",
            required=False,
            help="The opensearchstaging OpenSearchDashboard image build number if required, for example : 4104\n",
            dest="stgosdbuild",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="Show more verbose output. The default is 'logging.INFO', another option is 'logging.DEBUG'",
            action="store_const",
            default=logging.INFO,
            const=logging.DEBUG,
            dest="logging_level",
        )

        args = parser.parse_args()
        self.logging_level = args.logging_level
        self.OS_image = 'opensearchproject/opensearch'
        self.OSD_image = 'opensearchproject/opensearch-dashboards'
        self.OS_image_version = args.OS_image_version
        self.OSD_image_version = args.OSD_image_version
        self.stgosbuild = args.stgosbuild
        self.stgosdbuild = args.stgosdbuild

    def stg_tag(self, image_type: str) -> str:
        return " ".join(
            filter(
                None,
                [
                    self.OS_image_version if image_type == "OS" else self.OSD_image_version,
                    "." + self.stgosbuild if (self.stgosbuild != "") and (image_type == "OS") else None,
                    "." + self.stgosdbuild if (self.stgosdbuild != "") and (image_type == "OSD") else None,
                ],
            )
        )
