# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import logging
from typing import Any, Optional

from manifests_workflow.input_manifests_opensearch import InputManifestsOpenSearch
from manifests_workflow.input_manifests_opensearch_dashboards import InputManifestsOpenSearchDashboards


class ManifestsArgs:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Manifest management")
        parser.add_argument("action", choices=["list", "update"], help="Operation to perform.")
        parser.add_argument(
            "--type",
            dest="type",
            choices=["opensearch", "opensearch-dashboards"],
            help="Only list manifests of a specific type.",
        )
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
        self.logging_level = args.logging_level
        self.action = args.action
        self.keep = args.keep
        self.manifests = ManifestsArgs.__get_manifests(args.type)

    @classmethod
    def __get_manifests(self, type: Optional[str]) -> Any:
        if type == "opensearch":
            return [InputManifestsOpenSearch]
        elif type == "opensearch-dashboards":
            return [InputManifestsOpenSearchDashboards]
        elif type is None:
            return [InputManifestsOpenSearch, InputManifestsOpenSearchDashboards]
        else:
            raise ValueError(type)
