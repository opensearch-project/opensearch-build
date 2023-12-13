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
        release_notes_path = os.path.join(self.root, "release-notes")
        return release_notes_path

    # combine path with the file in files_in_path such that it ends with the filename
    @property
    def full_path(self) -> str:
        files_in_path = os.listdir(self.path)
        for fname in files_in_path:
            if fname.endswith(self.filename):
                release_notes_full_path = os.path.join(self.path, fname)
                return release_notes_full_path
        return None

    def path_exists(self) -> bool:
        path_exists = os.path.exists(self.path)
        return path_exists

    def exists(self) -> bool:
        if not os.path.exists(self.path):
            return False
        files_in_path = os.listdir(self.path)
        return self.path_exists() and any(fname.endswith(self.filename) for fname in files_in_path)


class ReleaseNotesOpenSearch(ReleaseNotesComponent):

    @property
    def filename(self) -> str:
        release_notes_filename = f'.release-notes-{self.build_version}.md'
        return release_notes_filename


class ReleaseNotesOpenSearchPlugin(ReleaseNotesComponent):

    @property
    def filename(self) -> str:
        release_notes_filename = f'.release-notes-{self.build_version}.0.md'
        return release_notes_filename


class ReleaseNotesComponents:

    @classmethod
    def from_component(self, component: InputComponentFromSource, build_version: str, root: str) -> ReleaseNotesComponent:
        if component.name == 'OpenSearch' or component.name == 'OpenSearch-Dashboards':
            return ReleaseNotesOpenSearch(component, build_version, root)
        else:
            return ReleaseNotesOpenSearchPlugin(component, build_version, root)
