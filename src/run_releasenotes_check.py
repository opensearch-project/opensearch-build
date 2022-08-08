import logging
import os
import subprocess
import sys
from typing import Any, List

from pytablewriter import MarkdownTableWriter

from checkout_workflow.checkout_args import CheckoutArgs
from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory

# in format yyyy-mm-dd, example 2022-07-26
gitLogDate = os.getenv('GIT_LOG_DATE')
# Github issue to add the generated markdown table as a new comment
gitIssueNumber = os.getenv('GIT_ISSUE_NUMBER')
# Boolen if set to null, just prints on the console.
addComment = os.getenv('ADD_COMMENT', default="true")
# Token used to add comment on an issue
userToken = os.getenv('GITHUB_TOKEN')


def main(gitLogDate: str, addComment: str) -> int:
    if gitLogDate is None:
        print("No GIT_LOG_DATE environmental value passed")
        sys.exit()
    value_matrix = []  # type: List[Any]
    args = CheckoutArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)
    writer = MarkdownTableWriter(
        table_name=f"{manifest.build.name} CommitID(after {gitLogDate}) & Release Notes info",
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
                    gitLogCmd = f'git log --after={gitLogDate} --pretty=format:"%h"'
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
        if addComment == "true":
            if gitIssueNumber is not None:
                comment_under_issue(gitIssueNumber, f'{work_dir.name}/table.txt', userToken)
            else:
                print("No GIT_ISSUE_NUMBER environmental value passed")
                sys.exit()
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
    main(gitLogDate, addComment)
