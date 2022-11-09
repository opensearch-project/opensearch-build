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
            description='Validating OpenSearch(OS) & OpenSearchDashboard(OSD) distribution build between opensearchproject and opensearchstaging at dockerHub/ECR',
            epilog='Example : ./checkdocker.sh opensearchproject/opensearch:latest opensearchproject/opensearch-dashboards:latest'
            )
        parser.add_argument(
            "OS_image",
            type=str,
            help="The OpenSearch image <name>:<tag> that we want to validate, for example : 'opensearchproject/opensearch:2.4.0' or 'opensearchproject/opensearch:latest'",
        )
        parser.add_argument(
            "OSD_image",
            type=str,
            help="The OpenSearchDashboard image <name>:<tag> that we want to validate, for example : 'opensearchproject/opensearch-dashboards:2.3.0' or 'opensearchproject/opensearch-dashboards:latest'",
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
        self.OS_image = args.OS_image
        self.OSD_image = args.OSD_image

        if (':' not in self.OS_image) or (':' not in self.OSD_image) or ('opensearchproject' not in self.OS_image) or ('opensearchproject' not in self.OSD_image):
            parser.error("The image should be opensearchproject and contain a tag, for example : 'opensearchproject/opensearch:2.4.0 or 'opensearchproject/opensearch-dashboards:latest'")