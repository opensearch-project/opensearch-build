# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import re
import shutil
from collections import defaultdict

import mistune
import requests

from manifests.input_manifest import InputManifest
from release_notes_workflow.release_notes import ReleaseNotes
from release_notes_workflow.release_notes_check_args import ReleaseNotesCheckArgs
from system import console


def main() -> int:
    args = ReleaseNotesCheckArgs()
    console.configure(level=args.logging_level)
    manifest_file = InputManifest.from_file(args.manifest)
    BUILD_VERSION = manifest_file.build.version

    BASE_FILE_PATH = "release_notes_automation"
    table_filename = f"{BASE_FILE_PATH}/release_notes_table-{BUILD_VERSION}.md"
    urls_filename = f"{BASE_FILE_PATH}/release_notes_urls-{BUILD_VERSION}.txt"

    def format_component_name_from_url(url) -> str:
        start_index = url.find("release-notes/")
        if start_index == -1:
            raise ValueError("'release-notes/' not found in the URL")
        end_index = url.find(".release-notes", start_index)
        if end_index == -1:
            raise ValueError("'.release-notes' not found after 'release-notes/'")
        component_name = url[start_index + len("release-notes/") : end_index]
        formatted_name = " ".join(word.capitalize() for word in component_name.split("-"))
        return formatted_name

    def create_urls_file_if_not_exists() -> None:
        urls_filepath = os.path.join(os.path.dirname(__file__), urls_filename)
        if os.path.exists(urls_filepath):
            print("URLs file already exists. Skipping creation.")
            return
        print("URLs file does not exist. Creating...")

        release_notes = ReleaseNotes(manifest_file, args.date, args.action)
        table = release_notes.table()

        table_filepath = os.path.join(os.path.dirname(__file__), table_filename)
        os.makedirs(os.path.dirname(table_filepath), exist_ok=True)
        with open(table_filepath, "w") as table_file:
            table.dump(table_file)

        if args.output is not None:
            print(f"Moving {table_filepath} to {args.output}")
            shutil.move(table_filepath, args.output)
        else:
            with open(table_filepath, "r") as table_file:
                print(table_file.read())

        urls = [row[-1].strip() for row in table.value_matrix if row[-1]]

        os.makedirs(os.path.dirname(urls_filepath), exist_ok=True)
        urls_filepath = os.path.join(os.path.dirname(__file__), urls_filename)
        with open(urls_filepath, "w") as urls_file:
            urls_file.writelines("\n".join(urls))

    if args.action == "check":
        create_urls_file_if_not_exists()

    elif args.action == "compile":
        create_urls_file_if_not_exists()

        RELEASENOTES_CATEGORIES = "BREAKING,FEATURES,ENHANCEMENTS,BUG FIXES,INFRASTRUCTURE,DOCUMENTATION,MAINTENANCE,REFACTORING,EXPERIMENTAL"
        RELEASE_NOTE_MD = f"{BASE_FILE_PATH}/release_notes-{BUILD_VERSION}.md"

        # Clean up URLs in the file
        urls_filepath = os.path.join(os.path.dirname(__file__), urls_filename)
        with open(urls_filepath, "r") as file:
            urls = [line.strip() for line in file if line.strip()]

        unique_urls = list(set(urls))

    # store plugin data
    plugin_data = defaultdict(lambda: defaultdict(list))

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
                            content_to_end = content[content_start : content.find(headings[i + 1])]
                    # remove heading from obtained content to avoid duplication
                    parts = content_to_end.split("*", 1)
                    if len(parts) == 2:
                        content_to_end = "*" + parts[1]
                    plugin_data[plugin_name][heading].append(content_to_end)
                    # print(plugin_data[plugin_name][heading])
    print("Compilation complete.")
    # print("Unique Headings:")
    # for heading in sorted(unique_headings):
    #     print(heading)

    # Markdown renderer
    markdown = mistune.create_markdown()

    RELEASE_NOTE_MD_path = os.path.join(os.path.dirname(__file__), RELEASE_NOTE_MD)
    os.makedirs(os.path.dirname(RELEASE_NOTE_MD_path), exist_ok=True)

    # Filter content for each category
    with open(RELEASE_NOTE_MD_path, "w") as outfile:
        outfile.write(markdown(f"# OpenSearch and OpenSearch Dashboards {BUILD_VERSION} Release Notes\n\n"))

        for category in RELEASENOTES_CATEGORIES.split(","):
            # Discard category content if no data is available
            temp_content = []
            temp_content.append(markdown(f"\n## {category}\n\n"))

            for plugin, categories in plugin_data.items():
                if category.lower() in [cat.lower() for cat in categories.keys()]:
                    temp_content.append(markdown(f"\n### {plugin}\n\n"))
                    for cat, content_list in categories.items():
                        if cat.lower() == category.lower():
                            for content in content_list:
                                if content.strip():
                                    temp_content.append(markdown(content))

            if len(temp_content) > 1:
                outfile.write("\n".join(temp_content))
                outfile.write("\n")
            else:
                print(f"\n## {category} was empty\n\n")

        # Handle unknown categories
        for plugin, categories in plugin_data.items():
            for cat, content_list in categories.items():
                if cat.lower() not in RELEASENOTES_CATEGORIES.lower():
                    outfile.write(markdown(f"\n## {cat.upper()} [NEW CATEGORY]\n\n"))
                    outfile.write(markdown(f"\n### {plugin}\n\n"))
                    for content in content_list:
                        outfile.write(markdown(content))
                        outfile.write("\n")

    if args.output is not None:
        print(f"Moving {RELEASE_NOTE_MD} to {args.output}")
        shutil.move(RELEASE_NOTE_MD_path, args.output)
    else:
        print(f"Release notes compiled to {RELEASE_NOTE_MD_path}")
    return 0


if __name__ == "__main__":
    main()
