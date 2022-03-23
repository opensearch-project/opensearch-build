# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc


class BundleLocation(abc.ABC):
    def __init__(self, path: str, filename: str, distribution: str) -> None:
        self.path = path
        self.filename = filename
        self.distribution = distribution

    @abc.abstractmethod
    def join(self, *args: str) -> str:
        pass

    def get_build_location(self, target_name: str) -> str:
        return self.join("builds", self.filename, self.distribution, target_name)

    def get_bundle_location(self, target_name: str) -> str:
        return self.join("dist", self.filename, self.distribution, target_name)
