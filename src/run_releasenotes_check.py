# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import re
import shutil
import subprocess
import sys
import requests
from collections import defaultdict
from typing import List
from manifests.input_manifest import InputManifest
from release_notes_workflow.release_notes import ReleaseNotes
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from system import console
from system.temporary_directory import TemporaryDirectory
try:
    import markdownify
    import mistune
except ImportError:
    markdownify = None
    mistune = None


def main() -> int:
    # Add the src directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    args = ReleaseNotesCheckArgs()
    console.configure(level=args.logging_level)
    manifests: List[InputManifest] = []
    # storing temporary release notes for testing purposes
    BASE_FILE_PATH = "release_notes_workflow/results"

    for input_manifests in args.manifest:
        manifests.append(InputManifest.from_file(input_manifests))

    if len(args.manifest) == 2:
        if manifests[0].build.version != manifests[1].build.version:
            raise ValueError("OS and OSD manifests must be provided for the same release version")
        elif manifests[0].build.name == manifests[1].build.name:
            raise ValueError("Both manifests are for the same product, OS and OSD manifests must be provided")
    if len(args.manifest) > 2:
        raise ValueError("Only two manifests, OS and OSD, can be provided")

    #  Assuming that the OS and OSD manifests will be provided for the same release version
    BUILD_VERSION = manifests[0].build.version

    table_filename = f"{BASE_FILE_PATH}/release_notes_table-{BUILD_VERSION}.md"
    urls_filename = f"{BASE_FILE_PATH}/release_notes_urls-{BUILD_VERSION}.txt"

    def check_if_exists_then_delete(file_path: List[str]) -> None:
        """Check if files exist and delete them if they do.
        
        Args:
            file_path: List of file paths to check and delete
        """
        base_dir = os.path.dirname(__file__)
        for file in file_path:
            full_path = os.path.join(base_dir, file)
            if os.path.exists(full_path):
                print(f"File {file} exists. Deleting")
                os.remove(full_path)
            else:
                logging.info(f"The file {file} does not exist, creating new.")
    
    def capitalize_acronyms(formatted_name: str) -> str:
        """Capitalize common acronyms in component names."""
        acronyms = {"sql": "SQL", "ml": "ML", "knn": "k-NN", "k-nn": "k-NN", "ml-commons": "ML Commons",
                    "ml commons": "ML Commons"}
        for acronym, replacement in acronyms.items():
            formatted_name = re.sub(r'\b' + re.escape(acronym) + r'\b', replacement, formatted_name,
                                    flags=re.IGNORECASE)
        return formatted_name

    def format_component_name_from_url(url: str) -> str:
        start_index = url.find("release-notes/")
        if start_index == -1:
            raise ValueError("'release-notes/' not found in the URL")
        end_index = url.find(".release-notes", start_index)
        if end_index == -1:
            raise ValueError("'.release-notes' not found after 'release-notes/'")
        component_name = url[start_index + len("release-notes/"): end_index]
        formatted_name = " ".join(word.capitalize() for word in re.split(r"[-.]", component_name))
        return capitalize_acronyms(formatted_name)

    def create_urls_file_if_not_exists(manifest_files: List[InputManifest]) -> None:
        base_dir = os.path.dirname(__file__)
        release_notes = ReleaseNotes(manifest_files, args.date, args.action, args.test_mode)
        table = release_notes.table()

        table_filepath = os.path.join(base_dir, table_filename)
        os.makedirs(os.path.dirname(table_filepath), exist_ok=True)
        with open(table_filepath, "a") as table_file:
            table.dump(table_file)

        if args.output is not None:
            logging.info(f"Moving {table_filepath} to {args.output}")
            shutil.move(table_filepath, args.output)
        else:
            with open(table_filepath, "r") as table_file:
                logging.info(table_file.read())

        urls = [row[-1].strip() for row in table.value_matrix if row[-1]]
        urls_filepath = os.path.join(base_dir, urls_filename)
        os.makedirs(os.path.dirname(urls_filepath), exist_ok=True)
        with open(urls_filepath, "a") as urls_file:
            urls_file.writelines("\n".join(urls))

    if args.action == "check":
        check_if_exists_then_delete([table_filename, urls_filename])
        create_urls_file_if_not_exists(manifests)
        return 0
    
    elif args.action == "generate":
        # Generate AI-powered release notes
        check_if_exists_then_delete([table_filename, urls_filename])
        
        def get_date_from_git_tag(current_version: str) -> str:
            """Get date from git tag."""
            
            # Calculate previous version
            try:
                version_parts = current_version.split('.')
                if len(version_parts) >= 2:
                    major, minor = int(version_parts[0]), int(version_parts[1])
                    previous_version = f"{major}.{minor-1}.0" if minor > 0 else f"{major-1}.0.0" if major > 0 else "2.0.0"
                else:
                    previous_version = "3.0.0"
                
                logging.info(f"Looking for tag date for version {previous_version}")
                
                # Clone and search for tag
                with TemporaryDirectory() as temp_dir:
                    repo_dir = f"{temp_dir.name}/opensearch-build"
                    clone_cmd = f"git clone --depth 50 https://github.com/opensearch-project/opensearch-build.git {repo_dir}"
                    
                    if subprocess.run(clone_cmd, shell=True, capture_output=True).returncode != 0:
                        raise Exception("Failed to clone repository")
                    
                    # Direct tag search - this is the approach that works
                    tag_cmd = f"git log --tags --simplify-by-decoration --pretty='format:%ai %d' | grep '{previous_version}'"
                    tag_result = subprocess.run(tag_cmd, shell=True, capture_output=True, text=True, cwd=repo_dir)
                    
                    if tag_result.returncode == 0 and tag_result.stdout.strip():
                        date_str = tag_result.stdout.strip().split('\n')[0].split()[0]
                        logging.info(f"Found tag date for {previous_version}: {date_str}")
                        return date_str
                
                raise ValueError(f"Tag {previous_version} not found in repository")
                
            except Exception as e:
                raise ValueError(f"Failed to determine date: {e}. Please use --date to specify the start date.")
        
        # Get date - use provided date or get from GitHub release
        current_release_version = manifests[0].build.version
        if args.date:
            date = str(args.date)
            logging.info(f"Using provided date: {date}")
        else:
            try:
                date = get_date_from_git_tag(current_release_version)
            except ValueError as e:
                logging.error(str(e))
                return 1
        
        logging.info(f"Generating AI release notes for version {current_release_version} since {date}")
        
        # Create ReleaseNotes instance with date
        release_notes = ReleaseNotes(manifests, date, args.action, args.test_mode)
        
        # Generate AI release notes for each component
        for i, manifest in enumerate(manifests):
            manifest_path = args.manifest[i].name if i < len(args.manifest) else None
            for component in manifest.components.select(focus=args.components, platform='linux'):
                if hasattr(component, "repository"):
                    logging.info(f"Processing {component.name} for AI release notes generation")
                    try:
                        release_notes.generate(component, manifest.build.version, manifest.build.qualifier, manifest_path)
                    except Exception as e:
                        logging.error(f"Failed to generate release notes for {component.name}: {e}")
        
        logging.info("AI release notes generation completed")
        
        # Print summary of what was processed
        processed_count = sum(1 for manifest in manifests 
                             for component in manifest.components.select(focus=args.components, platform='linux')
                             if hasattr(component, "repository"))
        
        if processed_count > 0:
            print(f"📊 Summary: Processed {processed_count} component(s)")
            if args.components:
                print(f"🔍 Component filter: {args.components}")
            print(f"📅 Date: {date}")
            print(f"🏷️  Target version: {BUILD_VERSION}")
        else:
            print(f"⚠️  No components found for processing" + 
                  (f" matching filter: {args.components}" if args.components else ""))
        
        return 0

    elif args.action == "compile":
        # Check if compile-specific dependencies are available
        if markdownify is None or mistune is None:
            logging.error("Compile action requires additional dependencies")
            logging.error("Please install: pip install markdownify mistune")
            return 1
            
        check_if_exists_then_delete([table_filename, urls_filename])
        create_urls_file_if_not_exists(manifests)

        RELEASENOTES_CATEGORIES = "BREAKING,FEATURES,ENHANCEMENTS,BUG FIXES,INFRASTRUCTURE,DOCUMENTATION,MAINTENANCE,REFACTORING,EXPERIMENTAL"
        RELEASE_NOTE_MD = f"{BASE_FILE_PATH}/release_notes-{BUILD_VERSION}.md"

        # Define heading mappings
        heading_mapping = {
            "Feature": "Features",
            "Feat": "Features",
            "Experimental Features": "Experimental",
            "Refactor": "Refactoring",
            "Enhancement": "Enhancements",
            "Bug Fix": "Bug Fixes",
        }
        
        def process_release_notes_urls(urls_file_path: str) -> defaultdict:
            """Process release notes URLs and extract content."""
            with open(urls_file_path, "r") as file:
                urls = [line.strip() for line in file if line.strip()]
            
            unique_urls = list(set(urls))
            plugin_data = defaultdict(lambda: defaultdict(list))
            
            for url in unique_urls:
                if url.startswith("#"):
                    continue
                    
                response = requests.get(url)
                if response.status_code != 200:
                    logging.warning(f"Failed to fetch URL: {url}")
                    continue
                    
                content = response.text
                plugin_name = format_component_name_from_url(url)
                
                # Extract headings
                headings = [match.strip() for match in re.findall(r"###.+", content)]
                if not headings:
                    continue
                
                # Process each heading
                for i, heading_text in enumerate(headings):
                    # Format heading
                    heading = heading_text.strip()
                    if heading.startswith("### "):
                        heading = heading[4:]
                    heading = heading.title()
                    
                    # Map to standard heading if needed
                    if heading in heading_mapping:
                        heading = heading_mapping[heading]
                    
                    # Extract content for this heading
                    content_start = content.find(headings[i])
                    if content_start == -1:
                        continue
                        
                    content_end = content.find(headings[i+1]) if i < len(headings)-1 else len(content)
                    content_to_end = content[content_start:content_end]
                    
                    # Format content
                    content_to_end = content_to_end.replace(f"### {heading}", "").lstrip()
                    parts = content_to_end.split("*", 1)
                    if len(parts) == 2:
                        content_to_end = "*" + parts[1]
                    else:
                        content_to_end = content_to_end.lstrip().lstrip("-")
                        if content_to_end:
                            content_to_end = "* " + content_to_end
                            
                    plugin_data[plugin_name][heading].append(content_to_end)
            
            return defaultdict(list, sorted(plugin_data.items()))
            
        # Process release notes URLs
        urls_filepath = os.path.join(os.path.dirname(__file__), urls_filename)
        plugin_data = process_release_notes_urls(urls_filepath)
        logging.info("Compilation complete.")

        # Markdown renderer
        markdown = mistune.create_markdown()

        RELEASE_NOTE_MD_PATH = os.path.join(os.path.dirname(__file__), RELEASE_NOTE_MD)
        os.makedirs(os.path.dirname(RELEASE_NOTE_MD_PATH), exist_ok=True)

        # Filter content for each category
        with open(RELEASE_NOTE_MD_PATH, "w") as outfile:
            outfile.write(markdown(f"# OpenSearch and OpenSearch Dashboards {BUILD_VERSION} Release Notes\n\n"))

            for category in RELEASENOTES_CATEGORIES.split(","):
                # Discard category content if no data is available
                temp_content = []
                temp_content.append(markdown(f"\n## {category}\n\n"))

                for plugin, categories in plugin_data.items():
                    if category.lower() in [cat.lower() for cat in categories.keys()]:
                        for cat, content_list in categories.items():
                            if cat.lower() == category.lower():
                                for content in content_list:
                                    if content.strip():
                                        temp_content.append(markdown(f"\n### {plugin}\n\n"))
                                        temp_content.append(markdown(content))

                if len(temp_content) > 1:
                    outfile.write("\n".join(temp_content))
                    outfile.write("\n")
                else:
                    logging.info(f"\n## {category} was empty\n\n")

            # Handle unknown categories
            temp_content = []
            for plugin, categories in plugin_data.items():
                for cat, content_list in categories.items():
                    if cat.lower() not in RELEASENOTES_CATEGORIES.lower():
                        temp_content.append(f"\n## {cat.upper()}\n\n")
                        temp_content.append(f"\n### {plugin}\n\n")
                        temp_content.extend(content_list)
            if temp_content:
                outfile.write(markdown("## NON-COMPLIANT"))
                for item in temp_content:
                    outfile.write(markdown(item))

        with open(RELEASE_NOTE_MD_PATH, 'r') as f:
            html_content = f.read()

        markdown_content = markdownify.markdownify(html_content, heading_style="ATX")

        with open(RELEASE_NOTE_MD_PATH, 'w') as f:
            f.write(markdown_content)

        if args.output is not None:
            logging.info(f"Moving {RELEASE_NOTE_MD} to {args.output}")
            shutil.move(RELEASE_NOTE_MD_PATH, args.output)
        else:
            logging.info(f"Release notes compiled to {RELEASE_NOTE_MD_PATH}")
        return 0


if __name__ == "__main__":
    main()
