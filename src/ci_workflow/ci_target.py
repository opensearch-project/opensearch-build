# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


class CiTarget:
    version: str
    name: str
    snapshot: bool

    def __init__(self, version: str, name: str, qualifier: str, snapshot: bool = True) -> None:
        self.version = version
        self.name = name
        self.qualifier = qualifier
        self.snapshot = snapshot

    @property
    def opensearch_version(self) -> str:
        os_version = self.version + f"-{self.qualifier}" if self.qualifier else self.version
        return os_version + "-SNAPSHOT" if self.snapshot else os_version

    @property
    def component_version(self) -> str:
        # BUG: the 4th digit is dictated by the component, it's not .0, this will break for 1.1.0.1
        comp_version = f"{self.version}.0" + f"-{self.qualifier}" if self.qualifier else f"{self.version}.0"
        return comp_version + "-SNAPSHOT" if self.snapshot else comp_version
