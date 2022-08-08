# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os


class ReleaseNotesOpenSearch:

    def __init__(self, buildversion: str) -> None:
        self.buildversion = buildversion

    @property
    def filename(self) -> str:
        return f'.release-notes-{self.buildversion}.md'


class ReleaseNotesOpenSearchPlugins:

    def __init__(self, buildversion: str) -> None:
        self.buildversion = buildversion

    @property
    def filename(self) -> str:
        return f'.release-notes-{self.buildversion}.0.md'


class ReleaseNotesCheck:

    def __init__(self, component: str, buildversion: str, path: str) -> None:
        self.component = component
        self.buildversion = buildversion
        self.path = path

    def releaseNotes(self, filename: str) -> str:
        release_notes = "NO"
        try:
            if any(fname.endswith(filename) for fname in os.listdir(f'{self.path}/release-notes/')):
                release_notes = "YES"
        except FileNotFoundError:
            print("No such release-notes file or directory")
            release_notes = "NULL"
        return release_notes

    def check(self) -> str:
        if self.component == 'OpenSearch' or self.component == 'OpenSearch-Dashboards':
            release_notes_opensearch = ReleaseNotesOpenSearch(self.buildversion)
            release_notes_file = release_notes_opensearch.filename
        else:
            release_notes_opensearch_plugins = ReleaseNotesOpenSearchPlugins(self.buildversion)
            release_notes_file = release_notes_opensearch_plugins.filename
        return self.releaseNotes(release_notes_file)
