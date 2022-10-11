# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
from abc import ABC, abstractmethod


class Validation(ABC):
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Download Artifacts.")
        parser.add_argument("version", help="Enter Version.")
        args = parser.parse_args()
        self.version = args.version

    @classmethod
    @abstractmethod
    def get_architectures(cls) -> list:
        pass

    @classmethod
    @abstractmethod
    def download_urls(cls, projects: list, version: str, platform: str) -> None:
        pass
