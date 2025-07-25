# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import List

from pytablewriter import MarkdownTableWriter

from git.git_commit_processor import GitHubCommitsProcessor
from git.git_repository import GitRepository
from llms.ai_release_notes_generator import AIReleaseNotesGenerator
from llms.prompts import AI_RELEASE_NOTES_PROMPT_CHANGELOG, AI_RELEASE_NOTES_PROMPT_COMMIT
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from system.temporary_directory import TemporaryDirectory


class ReleaseNotes:

    def __init__(self, input_manifests: List[InputManifest], date: str, action_type: str) -> None:
        self.manifests = input_manifests  # type: ignore[assignment]
        self.date = date
        self.action_type = action_type
        self.token = os.getenv('GITHUB_TOKEN')
        self.filter_commits = ['flaky-test', 'testing']

    def table(self) -> MarkdownTableWriter:
        table_result = []
        for manifest in self.manifests:
            for component in manifest.components.select():
                if (component.name == 'OpenSearch' or component.name == 'OpenSearch-Dashboards' or component.name == 'notifications-core') and self.action_type == 'compile':
                    continue
                if hasattr(component, "repository"):
                    table_result.append(self.check(component, manifest.build.version, manifest.build.qualifier))  # type: ignore[arg-type]

        # Sort table_result based on Repo column
        table_result.sort(key=lambda x: (x[0], x[1]) if len(x) > 1 else x[0])

        if self.action_type == "check":
            headers = ["Repo", "Branch", "CommitID", "Commit Date", "Release Notes Exists"]
        elif self.action_type == "compile":
            headers = ["Repo", "Branch", "CommitID", "Commit Date", "Release Notes Exists", "URL"]
        else:
            raise ValueError("Invalid action_type. Use 'check' or 'compile'.")

        writer = MarkdownTableWriter(
            table_name=f"Core Components CommitID(after {self.date}) & Release Notes info",
            headers=headers,
            value_matrix=table_result
        )
        return writer

    def check(self, component: InputComponentFromSource, build_version: str, build_qualifier: str) -> List:
        results = []
        with TemporaryDirectory(chdir=True) as work_dir:
            results.append(component.name)
            results.append(f"[{component.ref}]")
            with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory
            ) as repo:
                logging.debug(f"Checked out {component.name} into {repo.dir}")
                release_notes = ReleaseNotesComponents.from_component(component, build_version, build_qualifier, repo.dir)
                commits = repo.log(self.date)
                if len(commits) > 0:
                    last_commit = commits[-1]
                    results.append(last_commit.id)
                    results.append(last_commit.date)
                else:
                    results.append(None)
                    results.append(None)
                results.append(release_notes.exists())

                if(release_notes.exists()):
                    releasenote = os.path.basename(release_notes.full_path)
                    repo_name = component.repository.split("/")[-1].split('.')[0]
                    repo_ref = component.ref.split("/")[-1]
                    url = f"https://raw.githubusercontent.com/opensearch-project/{repo_name}/{repo_ref}/release-notes/{releasenote}"
                    results.append(url)
                else:
                    results.append(None)
        return results

    def generate(self, args: ReleaseNotesCheckArgs, component: InputComponentFromSource, build_version: str, build_qualifier: str) -> None:
        """Generate AI-powered release notes for a component."""
        release_notes_raw = ""
        with TemporaryDirectory(chdir=True) as work_dir:
            with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory
            ) as repo:
                release_notes = ReleaseNotesComponents.from_component(component, build_version, build_qualifier, repo.dir)
                baseline_date = self.date
                changelog_path = os.path.join(repo.dir, 'CHANGELOG.md')
                logging.info(f"Using baseline date: {self.date}")

                # Initialize AI generator
                ai_generator = AIReleaseNotesGenerator(
                    args=args,
                )

                if os.path.isfile(changelog_path):
                    with open(changelog_path, 'r') as f:
                        changelog_content = f.read()

                    logging.info(f"Using CHANGELOG.md for {component.name}")
                    prompt = AI_RELEASE_NOTES_PROMPT_CHANGELOG.format(
                        component_name=component.name,
                        version=build_version,
                        repository_url=f"https://github.com/opensearch-project/{component.name}",
                        changelog_content=changelog_content
                    )
                    print(f"PROMPT:\n{prompt}")
                    release_notes_raw = ai_generator.generate_release_notes(prompt)
                else:
                    logging.info(f"No CHANGELOG.md found for {component.name}, will use GitHub API to get commits since {self.date}")
                    github_commits = GitHubCommitsProcessor(baseline_date, component, self.token)
                    commits = github_commits.get_commit_details()

                    if len(commits) > 0:
                        final_commits = [doc for doc in commits if not set(doc['Labels']) & set(self.filter_commits)]
                        commits_text = ""
                        for i, commit in enumerate(final_commits, 1):
                            message = commit.get("Message", "")
                            labels = commit.get("Labels", [])
                            pr_subject = commit.get("PullRequestSubject", "")

                            commits_text += f"{i}. PR Subject: {pr_subject}\n"
                            commits_text += f"   Message: {message}\n"
                            commits_text += f"   Labels: {', '.join(labels) if labels else 'None'}\n\n"
                        prompt = AI_RELEASE_NOTES_PROMPT_COMMIT.format(
                            component_name=component.name,
                            version=build_version,
                            repository_url=f"https://github.com/opensearch-project/{component.name}",
                            commits_text=commits_text
                        )
                        release_notes_raw = ai_generator.generate_release_notes(prompt)
                    else:
                        logging.warning(f"No commits found for {component.name} since {baseline_date}")

        if release_notes_raw:
            with open(os.path.join(os.getcwd(), 'release-notes', f"opensearch-{component.name}{release_notes.filename}"), 'w') as f:
                f.write(release_notes_raw)
