# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc


class BundleLocation(abc.ABC):
    def __init__(self, path: str, filename: str) -> None:
        self.path = path
        self.filename = filename

    @abc.abstractmethod
    def join(self, *args: str) -> str:
        pass

    def get_build_location(self, target_name: str) -> str:
        return self.join("builds", self.filename, target_name)

    def get_bundle_location(self, target_name: str) -> str:
        return self.join("dist", self.filename, target_name)
