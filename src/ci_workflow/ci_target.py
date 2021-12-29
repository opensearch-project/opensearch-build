# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


class CiTarget:
    version: str
    name: str
    snapshot: bool

    def __init__(self, version, name, snapshot=True):
        self.version = version
        self.name = name
        self.snapshot = snapshot

    @property
    def opensearch_version(self):
        return self.version + "-SNAPSHOT" if self.snapshot else self.version

    @property
    def component_version(self):
        # BUG: the 4th digit is dictated by the component, it's not .0, this will break for 1.1.0.1
        return self.version + ".0-SNAPSHOT" if self.snapshot else f"{self.version}.0"
