# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from abc import ABC, abstractmethod

from system.temporary_directory import TemporaryDirectory


class Validation(ABC):
    base_url = "https://artifacts.opensearch.org/releases/bundle/"
    tmp_dir = TemporaryDirectory()

    @classmethod
    @abstractmethod
    def download_artifacts(self, projects: list, version: str) -> bool:
        pass
