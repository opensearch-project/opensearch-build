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

from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from release_notes_workflow.release_notes_component import ReleaseNotesComponents
from system.temporary_directory import TemporaryDirectory


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
        from release_notes_workflow.ai_release_notes_generator import AIReleaseNotesGenerator
        
        # Store original working directory before changing to temp dir
        original_cwd = os.getcwd()
        
        # Extract manifest name from manifest path if provided
        manifest_name = "opensearch"  # Default
        if manifest_path:
            # Extract from path like "manifests/3.2.0/opensearch-3.2.0.yml" -> "opensearch"
            # or "manifests/3.2.0/opensearch-dashboards-3.2.0.yml" -> "opensearch-dashboards"
            manifest_filename = os.path.basename(manifest_path)
            if '-' in manifest_filename:
                # Split by '-' and remove the version part (last part that contains digits)
                parts = manifest_filename.split('-')
                # Find the last part that's not a version (contains digits and dots)
                manifest_parts = []
                for part in parts:
                    if not any(char.isdigit() for char in part) or part in ['dashboards']:
                        manifest_parts.append(part)
                    else:
                        break
                manifest_name = '-'.join(manifest_parts) if manifest_parts else "opensearch"
        
        with TemporaryDirectory(chdir=True) as work_dir:
            with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory,
                    fetch_depth=0  # Fetch full history for commit analysis
            ) as repo:
                logging.debug(f"Checked out {component.name} into {repo.dir}")
                
                # Check if release notes already exist
                release_notes = ReleaseNotesComponents.from_component(component, build_version, build_qualifier, repo.dir)
                
                if not release_notes.exists():
                    logging.info(f"Generating AI release notes for {component.name}")
                    
                    # Initialize AI generator (no token needed - uses git commands)
                    ai_generator = AIReleaseNotesGenerator(
                        github_token=None,  # Not needed for git-based access
                        version=build_version,
                        baseline_date=self.date
                    )
                    
                    # Generate AI release notes using existing repository directory
                    ai_result = ai_generator.process_repository(component, existing_repo_dir=repo.dir)
                    
                    if ai_result.get('success'):
                        logging.info(f"✅ AI release notes generated for {component.name}")
                        
                        # Save the AI result to local file (outside the temporary directory)
                        if ai_result.get('ai_result'):
                            repo_name = component.repository.rstrip('/').split('/')[-1].replace('.git', '').lower()
                            
                            # Generate filename in format: opensearch-sql.release-notes-3.2.0.md
                            local_filename = f"{manifest_name}-{repo_name}.release-notes-{build_version}.md"
                            
                            # Write file to original working directory
                            output_path = os.path.join(original_cwd, local_filename)
                            with open(output_path, 'w') as f:
                                f.write(f"# {component.name} {build_version} Release Notes\n\n")
                                f.write(ai_result['ai_result'])
                            
                            logging.info(f"📄 Saved release notes to {output_path}")
                    else:
                        logging.warning(f"❌ AI release notes failed for {component.name}: {ai_result.get('error')}")
                else:
                    logging.info(f"Release notes already exist for {component.name}")
