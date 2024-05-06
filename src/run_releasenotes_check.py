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
from collections import defaultdict
from typing import List

import markdownify
import mistune
import requests

from manifests.input_manifest import InputManifest
from release_notes_workflow.release_notes import ReleaseNotes
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from system import console


def main() -> int:
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
        for file in file_path:
            if os.path.exists(os.path.join(os.path.dirname(__file__), file)):
                print(f"file {file} exists. Deleting")
                os.remove(os.path.join(os.path.dirname(__file__), file))
            else:
                logging.info(f"The file {file} does not exist, creating new.")

    def capitalize_acronyms(formatted_name: str) -> str:
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
        if component_name == "opensearch-sql":
            component_name = "SQL"
        formatted_name = " ".join(word.capitalize() for word in re.split(r"[-.]", component_name))
        return capitalize_acronyms(formatted_name)

    def create_urls_file_if_not_exists(manifest_files: List[InputManifest]) -> None:

        release_notes = ReleaseNotes(manifest_files, args.date, args.action)
        table = release_notes.table()

        table_filepath = os.path.join(os.path.dirname(__file__), table_filename)
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

        urls_filepath = os.path.join(os.path.dirname(__file__), urls_filename)
        os.makedirs(os.path.dirname(urls_filepath), exist_ok=True)
        with open(urls_filepath, "a") as urls_file:
            urls_file.writelines("\n".join(urls))

    if args.action == "check":
        check_if_exists_then_delete([table_filename, urls_filename])
        create_urls_file_if_not_exists(manifests)
        return 0

    elif args.action == "compile":
        check_if_exists_then_delete([table_filename, urls_filename])
        create_urls_file_if_not_exists(manifests)

        RELEASENOTES_CATEGORIES = "BREAKING,FEATURES,ENHANCEMENTS,BUG FIXES,INFRASTRUCTURE,DOCUMENTATION,MAINTENANCE,REFACTORING,EXPERIMENTAL"
        RELEASE_NOTE_MD = f"{BASE_FILE_PATH}/release_notes-{BUILD_VERSION}.md"

        # Clean up URLs in the file
        urls_filepath = os.path.join(os.path.dirname(__file__), urls_filename)
        with open(urls_filepath, "r") as file:
            urls = [line.strip() for line in file if line.strip()]

        unique_urls = list(set(urls))

    # store plugin data
    plugin_data: defaultdict = defaultdict(lambda: defaultdict(list))
    # handle custom headings
    heading_mapping = {
        "Feature": "Features",
        "Feat": "Features",
        "Experimental Features": "Experimental",
        "Refactor": "Refactoring",
        "Enhancement": "Enhancements",
        "Bug Fix": "Bug Fixes",
    }
    unique_headings = set()
    for url in unique_urls:
        if not url.startswith("#"):
            response = requests.get(url)

            if response.status_code == 200:
                content = response.text
                plugin_name = format_component_name_from_url(url)

                # obtain headings (###) from the content
                headings = [match.strip() for match in re.findall(r"###.+", content)]
                if not headings:
                    continue

                # Store content under each heading in respective plugin
                for i in range(len(headings)):
                    heading = headings[i].strip()
                    if heading.startswith("### "):
                        heading = heading[4:]
                    heading = heading.title()

                    if heading in heading_mapping:
                        heading = heading_mapping[heading]
                    unique_headings.add(heading)

                    content_start = content.find(headings[i])
                    if content_start != -1:
                        if i == len(headings) - 1:
                            content_to_end = content[content_start:]
                        else:
                            content_to_end = content[content_start: content.find(headings[i + 1])]
                    content_to_end = content_to_end.replace(f"### {heading}", "").lstrip()
                    parts = content_to_end.split("*", 1)
                    if len(parts) == 2:
                        content_to_end = "*" + parts[1]
                    else:
                        content_to_end = content_to_end.lstrip().lstrip("-")
                        if len(content_to_end) > 0:
                            content_to_end = "* " + content_to_end
                    plugin_data[plugin_name][heading].append(content_to_end)
    plugin_data = defaultdict(list, sorted(plugin_data.items()))
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
