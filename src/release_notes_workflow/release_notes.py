# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys
import json
from typing import Any, Dict, List
from pytablewriter import MarkdownTableWriter
from git.git_repository import GitRepository
from git.git_commit_processor import GitHubCommitProcessor
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from system.temporary_directory import TemporaryDirectory
from llms.ai_release_notes_generator import AIReleaseNotesGenerator


class ReleaseNotes:

    def __init__(self, input_manifests: List[InputManifest], date: str, action_type: str, test_mode: bool = False) -> None:
        self.manifests = input_manifests  # type: ignore[assignment]
        self.date = date
        self.action_type = action_type
        self.test_mode = test_mode

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

    def generate(self, component: InputComponentFromSource, build_version: str, build_qualifier: str, manifest_path: str = None) -> None:
        """Generate AI-powered release notes for a component."""
        with TemporaryDirectory(chdir=True) as work_dir:
            baseline_date = self.date
            if self.date:
                logging.info(f"Using user-provided date as baseline: {baseline_date}")
            else:
                try:
                    with GitRepository(
                            "https://github.com/opensearch-project/opensearch-build.git",
                            "main",
                            os.path.join(work_dir.name, "opensearch-build")
                    ) as build_repo:
                        cmd = "git fetch --tags > /dev/null 2>&1 && git for-each-ref --sort=-creatordate --format='%(creatordate:iso8601)' refs/tags --count 1"
                        last_tag_date = build_repo.output(cmd)
                        if last_tag_date:
                            baseline_date = last_tag_date
                            logging.info(f"Using last tag date as baseline: {baseline_date}")
                except Exception as e:
                    logging.warning(f"Failed to get last tag date from opensearch-build: {e}")

            # Initialize AI generator
            ai_generator = AIReleaseNotesGenerator(
                github_token=None,
                version=build_version,
                baseline_date=baseline_date,
                test_mode=self.test_mode
            )

            with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory
            ) as repo:
                changelog_path = os.path.join(repo.dir, 'CHANGELOG.md')
                changelog_exist = os.path.isfile(changelog_path)
                last_tag_date = baseline_date
                commit_processor = GitHubCommitProcessor(last_tag_date, component)
                logging.info(f"Using baseline date: {last_tag_date}")
                
                if changelog_exist:
                    with open(changelog_path, 'r') as f:
                        changelog_content = f.read()
                    
                    logging.info(f"Using CHANGELOG.md for {component.name}")
                    ai_generator.process(changelog_content, component.name, manifest_path)
                else:
                    logging.info(f"No CHANGELOG.md found for {component.name}, will use GitHub API to get commits since {last_tag_date}")
                    commits = commit_processor.get_commit_details()
                    
                    if commits:
                        formatted_commits = json.dumps(commits, indent=2)
                        ai_generator.process(formatted_commits, component.name, manifest_path)
                    else:
                        logging.warning(f"No commits found for {component.name} since {last_tag_date}")
