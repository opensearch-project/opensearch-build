# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import re
from typing import List, Tuple

from pytablewriter import MarkdownTableWriter

from git.git_commit_processor import GitHubCommitsProcessor
from git.git_repository import GitRepository
from llms.ai_release_notes_generator import AIReleaseNotesGenerator
from llms.prompts import AI_RELEASE_NOTES_PROMPT_CHANGELOG, AI_RELEASE_NOTES_PROMPT_COMMIT, AI_RELEASE_NOTES_PROMPT_COMMIT_OPENSEARCH
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
        self.filter_commits = ['flaky-test', 'testing', 'skip-changelog']

    @staticmethod
    def _clean_message(text: str) -> str:
        """Strip Signed-off-by / Co-authored-by tags from flattened commit messages."""
        text = re.sub(r'\s*(Signed-off-by|Co-authored-by):\s*\S+.*?(?=\s*(?:Signed-off-by|Co-authored-by):|\s*$)', '', text)
        return re.sub(r'\s{2,}', ' ', text).strip()

    @staticmethod
    def _clean_pr_body(text: str) -> str:
        """Strip HTML comments, Check List sections, and DCO boilerplate from PR body."""
        # Remove HTML/markdown comments <!-- ... -->
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        # Remove Check List section (### Check List ... until next ### or end)
        text = re.sub(r'###?\s*Check\s*List.*?(?=###|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove Related Issues section (### Related Issues ... until next ### or end)
        text = re.sub(r'###?\s*Related\s*Issues.*?(?=###|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove DCO boilerplate paragraph
        text = re.sub(r'By submitting this pull request.*?Apache 2\.0 license\.?.*?(?=\n\n|\n#|\Z)', '', text, flags=re.DOTALL)
        return text.strip()

    @staticmethod
    def _extract_borderline_calls(raw: str) -> Tuple[str, str]:
        """Extract borderline calls HTML comment from LLM output, returning (release_notes, borderline_calls)."""
        match = re.search(r'<!-- BORDERLINE_CALLS\s*\n(.*?)-->', raw, re.DOTALL)
        if match:
            borderline = match.group(1).strip()
            release_notes = raw[:match.start()].rstrip() + "\n"
            return release_notes, borderline
        return raw, ""

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

                if (release_notes.exists()):
                    releasenote = os.path.basename(release_notes.full_path)
                    repo_name = component.repository.split("/")[-1].split('.')[0]
                    repo_ref = component.ref.split("/")[-1]
                    url = f"https://raw.githubusercontent.com/opensearch-project/{repo_name}/{repo_ref}/release-notes/{releasenote}"
                    results.append(url)
                else:
                    results.append(None)
        return results

    def generate(self, args: ReleaseNotesCheckArgs, component: InputComponentFromSource, build_version: str, build_qualifier: str, product: str) -> None:
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
                repo_name = component.repository.split("/")[-1].split('.')[0]
                filename: str = f"{product}{release_notes.filename}" if component.name in ['OpenSearch', 'OpenSearch-Dashboards'] else f"opensearch-{repo_name}{release_notes.filename}"

                if not args.skip_changelog and os.path.isfile(changelog_path):
                    with open(changelog_path, 'r') as f:
                        changelog_content = f.read()

                    logging.info(f"Using CHANGELOG.md for {component.name}")
                    prompt = AI_RELEASE_NOTES_PROMPT_CHANGELOG.format(
                        component_name=component.name,
                        version=build_version,
                        repository_url=component.repository.removesuffix('.git'),
                        changelog_content=changelog_content
                    )
                    release_notes_raw = ai_generator.generate_release_notes(prompt)
                else:
                    logging.info(f"Either --skip-changelog enabled or No CHANGELOG.md found for {component.name}, will use GitHub API to get commits since {self.date}")
                    github_commits = GitHubCommitsProcessor(baseline_date, component, self.token)
                    commits = github_commits.get_commit_details()

                    if len(commits) > 0:
                        final_commits = [doc for doc in commits if not set(doc['Labels']) & set(self.filter_commits)]
                        commits_text = ""
                        for i, commit in enumerate(final_commits, 1):
                            message = self._clean_message(commit.get("Message", ""))
                            labels = commit.get("Labels", [])
                            pr_subject = commit.get("PullRequestSubject", "")
                            pr_body = self._clean_pr_body(commit.get("PullRequestBody", ""))

                            commits_text += f"{i}. PR Subject: {pr_subject}\n"
                            commits_text += f"   Message: {message}\n"
                            commits_text += f"   Labels: {', '.join(labels) if labels else 'None'}\n"
                            # dependabot PRs have a lot of unneeded details in PR bodies
                            if pr_body and 'dependabot' not in labels:
                                # Truncate very long PR bodies to avoid exceeding token limits
                                truncated_body = pr_body[:2000] + "..." if len(pr_body) > 2000 else pr_body
                                commits_text += f"   PR Description: {truncated_body}\n"
                            commits_text += "\n"
                        commit_prompt = AI_RELEASE_NOTES_PROMPT_COMMIT_OPENSEARCH if component.name == 'OpenSearch' else AI_RELEASE_NOTES_PROMPT_COMMIT
                        prompt = commit_prompt.format(
                            component_name=component.name,
                            version=build_version,
                            repository_url=component.repository.removesuffix('.git'),
                            commits_text=commits_text
                        )
                        release_notes_raw = ai_generator.generate_release_notes(prompt)
                    else:
                        logging.warning(f"No commits found for {component.name} since {baseline_date}")

        if release_notes_raw:
            release_notes_content, borderline_calls = self._extract_borderline_calls(release_notes_raw)
            with open(os.path.join(os.getcwd(), 'release-notes', filename), 'w') as f:
                f.write(release_notes_content)
            if borderline_calls:
                borderline_filename = filename.replace('.md', '-borderline.md')
                with open(os.path.join(os.getcwd(), 'release-notes', borderline_filename), 'w') as f:
                    f.write(borderline_calls)
