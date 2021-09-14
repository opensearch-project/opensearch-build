# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import uuid

from system.arch import current_arch


class BuildTarget:
    build_id: str
    name: str
    version: str
    arch: str
    snapshot: bool
    output_dir: str

    def __init__(
        self,
        version,
        arch=None,
        name=None,
        snapshot=True,
        build_id=None,
        output_dir="artifacts",
    ):
        self.build_id = os.getenv("OPENSEARCH_BUILD_ID") or build_id or uuid.uuid4().hex
        self.name = name
        self.version = version
        self.snapshot = snapshot
        self.arch = arch or current_arch()
        self.output_dir = output_dir

    @property
    def opensearch_version(self):
        return self.version + "-SNAPSHOT" if self.snapshot else self.version

    @property
    def component_version(self):
        # BUG: the 4th digit is dictated by the component, it's not .0, this will break for 1.1.0.1
        return self.version + ".0-SNAPSHOT" if self.snapshot else f"{self.version}.0"
