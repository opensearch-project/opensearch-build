# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from abc import ABC, abstractmethod


class Validation(ABC):
    base_url = "https://artifacts.opensearch.org/releases/bundle/"

    def __init__(self, version: str, distribution: str, platform: str, projects: list) -> None:
        self.version = version
        self.distribution = distribution
        self.platform = platform
        self. projects = projects

    @classmethod
    @abstractmethod
    def download_artifacts(self, projects: list, version: str, platform: str, architectures: list) -> bool:
        pass
