# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.input_manifest import InputManifest
from release_notes_workflow.release_notes import ReleaseNotes
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from system import console


def main() -> int:
    args = ReleaseNotesCheckArgs()
    console.configure(level=args.logging_level)
    manifest_file = InputManifest.from_file(args.manifest)
    release_notes = ReleaseNotes(manifest_file, args.date)
    if args.action == "check":
        table_output = release_notes.table()
        table_output.write_table()
        if args.output is not None:
            table_output.dump(args.output)
    return 0


if __name__ == "__main__":
    main()
