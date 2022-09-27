# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from abc import abstractmethod

from manifests.input_manifest import InputComponentFromSource


class ReleaseNotesComponent:

    def __init__(self, component: InputComponentFromSource, build_version: str, root: str) -> None:
        self.component = component
        self.build_version = build_version
        self.root = root

    @property
    @abstractmethod
    def filename(self) -> str:
        pass

    @property
    def path(self) -> str:
        return os.path.join(self.root, "release-notes")

    def path_exists(self) -> bool:
        return os.path.exists(self.path)

    def exists(self) -> bool:
        return self.path_exists() and any(fname.endswith(self.filename) for fname in os.listdir(self.path))


class ReleaseNotesOpenSearch(ReleaseNotesComponent):

    @property
    def filename(self) -> str:
        return f'.release-notes-{self.build_version}.md'


class ReleaseNotesOpenSearchPlugin(ReleaseNotesComponent):

    @property
    def filename(self) -> str:
        return f'.release-notes-{self.build_version}.0.md'


class ReleaseNotesComponents:

    @classmethod
    def from_component(self, component: InputComponentFromSource, build_version: str, root: str) -> ReleaseNotesComponent:
        if component.name == 'OpenSearch' or component.name == 'OpenSearch-Dashboards':
            return ReleaseNotesOpenSearch(component, build_version, root)
        else:
            return ReleaseNotesOpenSearchPlugin(component, build_version, root)
