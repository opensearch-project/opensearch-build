# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse

from .rpm import Rpm
from .tar import Tar
from .yum import Yum


class ValidationArgs:
    SUPPORTED_DISTRIBUTIONS = ["tar", "yum", "rpm"]
    SUPPORTED_PLATFORMS = ["linux"]
    DISTRIBUTION_MAP = {"tar": Tar, "yum": Yum, "rpm": Rpm}

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Download Artifacts.")
        parser.add_argument(
            "version",
            type=str,
            help="Enter the Version"
        )
        parser.add_argument(
            "-d",
            "--distribution",
            type=str,
            choices=self.SUPPORTED_DISTRIBUTIONS,
            help="Distribution to build.",
            default="tar",
            dest="distribution"
        )
        parser.add_argument(
            "-p",
            "--platform",
            type=str,
            choices=self.SUPPORTED_PLATFORMS,
            help="Platform to build.",
            default="linux"
        )
        args = parser.parse_args()
        self.version = args.version
        self.distribution = args.distribution
        self.platform = args.platform
        self.projects = ["opensearch", "opensearch-dashboards"]

        dist_class = self.DISTRIBUTION_MAP.get(self.distribution, None)
        dist_class.download_urls(projects=self.projects, version=self.version, platform=self.platform)
