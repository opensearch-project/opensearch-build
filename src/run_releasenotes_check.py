import logging
import os
import subprocess
import sys
from typing import Any, List

from pytablewriter import MarkdownTableWriter

from releasenotes_check_workflow.releasenotes_check_args import ReleaseNotesCheckArgs
from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory


def main() -> int:
    value_matrix = []  # type: List[Any]
    args = ReleaseNotesCheckArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)
    writer = MarkdownTableWriter(
        table_name=f"{manifest.build.name} CommitID(after {args.gitlogdate}) & Release Notes info",
        headers=["Repo", "Branch", "CommitID", "Release Notes"],
        value_matrix=value_matrix
    )
    with TemporaryDirectory(chdir=True) as work_dir:
        logging.info(f"Checking out into {work_dir.name}")
        for component in manifest.components.select():
            logging.info(f"Checking out {component.name}")
            repo_list = []  # type: List[Any]
            if type(component) is InputComponentFromSource:
                with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory,
                ) as repo:
                    logging.debug(f"Checked out {component.name} into {repo.dir}")
                    gitLogCmd = f'git log --after={args.gitlogdate} --pretty=format:"%h"'
                    gitLog = subprocess.check_output(gitLogCmd.split(), cwd=repo.dir).decode()
                    repo_list.append(component.name)
                    repo_list.append(component.ref)
                    repo_list.append(gitLog)
                    release_notes = "NO"
                    if component.name == 'OpenSearch' or component.name == 'OpenSearch-Dashboards':
                        release_notes_check = f'.release-notes-{manifest.build.version}.md'
                    else:
                        release_notes_check = f'.release-notes-{manifest.build.version}.0.md'
                    try:
                        if any(fname.endswith(release_notes_check) for fname in os.listdir(f'{repo.dir}/release-notes/')):
                            release_notes = "YES"
                    except FileNotFoundError:
                        print("No such release-notes file or directory")
                        release_notes = "NULL"
                    repo_list.append(release_notes)
                    value_matrix.append(repo_list)
        writer.write_table()
        writer.dump("{}/table.txt".format(work_dir.name))
        if args.addcomment:
                comment_under_issue(args.gitissuenumber, f'{work_dir.name}/table.txt', args.gittoken)
    return 0


def subprocess_cmd(command: str) -> int:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)
    return 0


def comment_under_issue(issue_number: str, comment_text: str, userToken: str) -> int:
    # GITHUB_TOKEN used to add comment, to passed in GH issue, using GIT_ISSUE_NUMBER
    os.environ['GITHUB_TOKEN'] = userToken
    subprocess_cmd('gh auth login')
    subprocess_cmd('gh repo clone https://github.com/opensearch-project/opensearch-build.git; cd opensearch-build')
    subprocess_cmd('gh issue comment {} --body-file {} --repo opensearch-project/opensearch-build'.format(issue_number, comment_text))
    subprocess_cmd('gh auth logout --hostname github.com; cd ..; rm -rf opensearch-build')
    return 0


if __name__ == "__main__":
    main()
