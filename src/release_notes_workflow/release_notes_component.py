# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from typing import Any


class ComponentReleaseNotes:

    def __init__(self, component: str, buildversion: str, root: str) -> None:
        self.component = component
        self.buildversion = buildversion
        self.root = root

    @property
    def path(self) -> str:
        return os.path.join(self.root, "release-notes")

    def path_exists(self) -> bool:
        return os.path.exists(self.path)

    def exists(self) -> bool:
        return self.path_exists() and any(fname.endswith(self.from_component()) for fname in os.listdir(self.path))

    def from_component(self) -> Any:
        if self.component == 'OpenSearch' or self.component == 'OpenSearch-Dashboards':
            return ComponentReleaseNotesOpenSearch(self.component, self.buildversion, self.root).filename
        else:
            return ComponentReleaseNotesOpenSearchPlugin(self.component, self.buildversion, self.root).filename

    def check(self) -> str:
        if self.exists():
            return "YES"
        else:
            return "NO"


class ComponentReleaseNotesOpenSearch(ComponentReleaseNotes):

    @property
    def filename(self) -> str:
        return f'.release-notes-{self.buildversion}.md'


class ComponentReleaseNotesOpenSearchPlugin(ComponentReleaseNotes):

    @property
    def filename(self) -> str:
        return f'.release-notes-{self.buildversion}.0.md'
