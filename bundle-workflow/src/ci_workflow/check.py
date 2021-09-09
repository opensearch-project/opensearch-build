# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class Check(ABC):
    def __init__(self, component, git_repo, version, arch, snapshot):
        self.component = component
        self.git_repo = git_repo
        self.version = version
        self.arch = arch
        self.snapshot = snapshot
        self.opensearch_version = version + "-SNAPSHOT" if snapshot else version
        self.component_version = version + ".0-SNAPSHOT" if snapshot else f"{version}.0"
        if self.component.name == "OpenSearch":
            # HACK: OpenSearch version is 3-digits
            self.component_version = self.opensearch_version

    @abstractmethod
    def check(self):
        pass
