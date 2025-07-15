# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys
from typing import Any, Dict, List
from pytablewriter import MarkdownTableWriter
from git.git_repository import GitRepository
from llms.prompts import AI_RELEASE_NOTES_PROMPT_CHANGELOG
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from system.temporary_directory import TemporaryDirectory
from llms.ai_release_notes_generator import AIReleaseNotesGenerator

# Add the parent directory to sys.path to import process.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from process import Processor


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
                    component.working_directory,
                    fetch_depth=0  # Fetch full history for commit analysis
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
            # Initialize processor with initial date
            processor = Processor(build_version, self.date)
            baseline_date = self.date

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
                release_notes = ReleaseNotesComponents.from_component(component, build_version, build_qualifier, repo.dir)
                changelog_exist = os.path.isfile(os.path.join(repo.dir, 'CHANGELOG.md'))
                changelog_path = os.path.join(repo.dir, 'CHANGELOG.md')
                if changelog_exist:
                    with open(changelog_path, 'r') as f:
                        content = f.read()
                    #processed_data = processor.process(content, component.name)
                    prompt = AI_RELEASE_NOTES_PROMPT_CHANGELOG.format(
                        repo_name=component.name,
                        version=build_version,
                        repository_url=component.repository
                    )
                    print(f"Promt is:\n{prompt}")
                    #ai_generator.process(processed_data['formatted_content'], component.name, manifest_path)
                else:
                    # If no CHANGELOG.md found from GitHub, use commit history
                    logging.info(f"No CHANGELOG.md found for {component.name}, will use commit history")
                    content = processor.get_commit_history_content(repo, baseline_date, component.name)
                    if content:
                        processed_data = processor.process(content, component.name)
                        ai_generator.process(processed_data['formatted_content'], component.name, manifest_path)
