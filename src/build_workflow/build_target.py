# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import uuid
from typing import List

from system.os import current_architecture, current_platform


class BuildTarget:
    build_id: str
    name: str
    version: str
    platform: str
    architecture: str
    snapshot: bool
    output_dir: str

    def __init__(
        self,
        version: str,
        patches: List[str] = [],
        platform: str = None,
        architecture: str = None,
        name: str = None,
        snapshot: bool = True,
        build_id: str = None,
        output_dir: str = "artifacts",
    ):
        self.build_id = os.getenv("BUILD_NUMBER") or build_id or uuid.uuid4().hex
        self.name = name
        self.version = version
        self.patches = patches
        self.snapshot = snapshot
        self.architecture = architecture or current_architecture()
        self.platform = platform or current_platform()
        self.output_dir = output_dir

    @property
    def opensearch_version(self) -> str:
        return self.version + "-SNAPSHOT" if self.snapshot else self.version

    @property
    def compatible_opensearch_versions(self) -> List[str]:
        return (
            [self.version + "-SNAPSHOT" if self.snapshot else self.version]
            + self.patches
            + list(map(lambda version: version + "-SNAPSHOT", self.patches))
        )

    @property
    def component_version(self) -> str:
        # BUG: the 4th digit is dictated by the component, it's not .0, this will break for 1.1.0.1
        return self.version + ".0-SNAPSHOT" if self.snapshot else f"{self.version}.0"

    @property
    def compatible_component_versions(self) -> List[str]:
        return (
            [self.version + ".0-SNAPSHOT" if self.snapshot else f"{self.version}.0"]
            + list(map(lambda version: version + ".0", self.patches))
            + list(map(lambda version: version + ".0-SNAPSHOT", self.patches))
        )

    @property
    def compatible_versions(self) -> List[str]:
        versions = [self.version]
        versions.extend(self.patches)
        return versions
