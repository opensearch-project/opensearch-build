# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import json
import requests
from typing import List
from pytablewriter import MarkdownTableWriter
from git.git_repository import GitRepository
from git.git_commit_processor import GitHubCommitProcessor
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from system.temporary_directory import TemporaryDirectory
from llms.ai_release_notes_generator import AIReleaseNotesGenerator


class ReleaseNotes:

    def __init__(self, input_manifests: List[InputManifest], date: str, action_type: str) -> None:
        self.manifests = input_manifests  # type: ignore[assignment]
        self.date = date
        self.action_type = action_type

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

    def generate(self, component: InputComponentFromSource, build_version: str, manifest_path: str = None) -> None:
        """Generate AI-powered release notes for a component."""
        baseline_date = self.date
        env_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-API-Client/1.0"
        }

        if env_token:
            headers["Authorization"] = f"token {env_token}"
        if self.date:
            logging.info(f"Using user-provided date as baseline: {baseline_date}")
        else:
            try:
                latest_release_url = "https://api.github.com/repos/opensearch-project/opensearch-build/releases/latest"
                
                response = requests.get(latest_release_url, headers=headers)
                response.raise_for_status()
                release_data = response.json()
                release_date = release_data.get("published_at")
                if release_date:
                    baseline_date = release_date
                    logging.info(f"Using latest release date from GitHub API as baseline: {baseline_date}")
            except Exception as e:
                logging.warning(f"Failed to get last tag date from GitHub API: {e}")
        with TemporaryDirectory(chdir=True) as work_dir:
            # Initialize AI generator
            ai_generator = AIReleaseNotesGenerator(
                version=build_version,
                baseline_date=baseline_date
            )

            with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory
            ) as repo:
                changelog_path = os.path.join(repo.dir, 'CHANGELOG.md')
                logging.info(f"Using baseline date: {baseline_date}")
                
                if os.path.isfile(changelog_path):
                    with open(changelog_path, 'r') as f:
                        changelog_content = f.read()
                    
                    logging.info(f"Using CHANGELOG.md for {component.name}")
                    ai_generator.process(changelog_content, component.name, manifest_path, repo, component)
                else:
                    logging.info(f"No CHANGELOG.md found for {component.name}, will use GitHub API to get commits since {baseline_date}")
                    commits = GitHubCommitProcessor(baseline_date, component, headers).get_commit_details()
                    
                    if commits:
                        formatted_commits = json.dumps(commits, indent=2)
                        ai_generator.process(formatted_commits, component.name, manifest_path, repo, component)
                    else:
                        logging.warning(f"No commits found for {component.name} since {baseline_date}")
