# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from release_notes_workflow.release_notes_tabel import ReleaseNotesTabel
from system import console


def main() -> int:
    args = ReleaseNotesCheckArgs()
    console.configure(level=args.logging_level)
    if args.action == "check":
        ReleaseNotesTabel.tabel(args.manifest, args.date, args.save)
    return 0


if __name__ == "__main__":
    main()
