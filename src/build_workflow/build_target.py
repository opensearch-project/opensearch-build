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
    qualifier: str
    platform: str
    architecture: str
    distribution: str
    snapshot: bool
    output_dir: str

    def __init__(
        self,
        version: str,
        qualifier: str = None,
        patches: List[str] = [],
        platform: str = None,
        architecture: str = None,
        distribution: str = None,
        name: str = None,
        snapshot: bool = True,
        build_id: str = None,
        output_dir: str = "artifacts",
    ):
        self.build_id = os.getenv("BUILD_NUMBER") or build_id or uuid.uuid4().hex
        self.name = name
        self.version = version
        self.qualifier = qualifier
        self.patches = patches
        self.snapshot = snapshot
        self.architecture = architecture or current_architecture()
        self.distribution = distribution
        self.platform = platform or current_platform()
        self.output_dir = output_dir

    @property
    def opensearch_version(self) -> str:
        return BuildTarget.__qualify_version(
            self.version,
            self.qualifier,
            self.snapshot
        )

    @property
    def compatible_min_versions(self) -> List[str]:
        return (
            [BuildTarget.__qualify_version(self.version, self.qualifier, self.snapshot)]
            + self.patches
            + list(map(lambda version: BuildTarget.__qualify_version(version, self.qualifier, True), self.patches))
        )

    @property
    def component_version(self) -> str:
        # BUG: the 4th digit is dictated by the component, it's not .0, this will break for 1.1.0.1
        return BuildTarget.__qualify_version(
            self.version + ".0",
            self.qualifier,
            self.snapshot
        )

    @property
    def compatible_component_versions(self) -> List[str]:
        return (
            [BuildTarget.__qualify_version(self.version + ".0", self.qualifier, self.snapshot)]
            + list(map(lambda version: BuildTarget.__qualify_version(version + ".0", self.qualifier, False), self.patches))
            + list(map(lambda version: BuildTarget.__qualify_version(version + ".0", self.qualifier, True), self.patches))
        )

    @property
    def compatible_versions(self) -> List[str]:
        versions = [self.version]
        versions.extend(self.patches)
        return versions

    @classmethod
    def __qualify_version(cls, unqualified_version: str, qualifier: str = None, snapshot: bool = False) -> str:
        version = unqualified_version
        if qualifier:
            version += f"-{qualifier}"
        if snapshot:
            version += "-SNAPSHOT"
        return version
