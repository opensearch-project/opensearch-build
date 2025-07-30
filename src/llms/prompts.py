# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

"""Prompt constants for LLM-based functionality."""

# AI Release Notes Generator prompt
AI_RELEASE_NOTES_PROMPT_CHANGELOG = """Generate release notes for {component_name} {version} from the changelog below. Use only the "Unreleased 3.x" section.

**Instructions:**
- Extract over the content from the "Unreleased 3.x" or "Unreleased" section of the changelog along with pull request links.
- If no section containing "Unreleased" AND no section matching version {version} exists, send an empty response back.

**Output Requirements:**
   - The main heading with ## should be "version number Release Notes" (e.g., For version 3.2.0 ## Version 3.2.0
   Release Notes followed by a blank line and then "Compatible with OpenSearch and OpenSearch Dashboards version
   <version number>" followed by content)

**Entry Format:**
   - Each entry Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - Make sure first character of each entry is capitalized.

**Changelog Content:**
{changelog_content}
"""

AI_RELEASE_NOTES_PROMPT_COMMIT = """I need you to generate OpenSearch component release notes from commit data. Please follow the OpenSearch release notes format exactly.

**Component Information:**
- Component Name: {component_name}
- Version: {version}
- Repository URL: {repository_url}

**Commit Data:**
{commits_text}

**Instructions:**

1. **Label-based Categorization Logic:**
   - First, check if any labels match these categories (case-insensitive, partial matches allowed):
     * "breaking change" or "breaking" → Breaking Changes
     * "feature" or "feat" → Features
     * "enhancement" or "improve" → Enhancements
     * "bug" or "fix" or "bugfix" → Bug Fixes
     * "infrastructure" or "ci" or "test" → Infrastructure
     * "documentation" or "docs" → Documentation
     * "maintenance" or "version" or "support" → Maintenance
     * "refactor" or "refactoring" → Refactoring

2. **Fallback Message Analysis:**
   - If no labels match, analyze the Message content and PullRequestSubject to determine the appropriate category following below guidelines:
    * Features: A change that introduce a net new unit of functionality of a software system that satisfies a requirement,
    represents a design decision, and provides a potential configuration option. As for improvement on existing features,
    use the Enhancement category. As for fixes on existing features, use the Bug Fixes category.
    Example: "Add start/stop batch actions on detector list page"
    * Enhancements: A change that improves the performance, usability, or reliability of an existing feature without
    changing its core functionality. Example: "Improve detector list page performance"
    * Bug Fixes: A change that resolves an issue or defect in the software.
    Example: "Fix issue with detector creation form validation"
    * Infrastructure: A change that modifies the underlying architecture, build process, or deployment of the software
    Example: "Update CI/CD pipeline for better reliability"
    * Documentation: A change that updates or adds documentation, such as README files, user guides, or API docs.
    Example: "Update README with new installation instructions"
    * Maintenance: A change that involves routine upkeep, such as version updates, dependency management, or minor
    tweaks that do not fit other categories. Example: "Update dependencies to latest versions"
    * Refactoring: A change that improves the internal structure of the code without changing its external behavior.
    Example: "Refactor detector service for better readability or Make ClusterDetailsEventProcessor and all its access
    methods non-static"
   - Do not lose any commit information, even if it doesn't match any category

3. **Entry Format:**
   - Use PullRequestSubject as the main content for each entry
   - Extract PR number from PullRequestSubject (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - Make sure first character of each entry is capitalized.

4. **Output Requirements:**
   - The main heading with ## should be "version number Release Notes" (e.g., For version 3.2.0 ## Version 3.2.0
   Release Notes followed by a blank line and then "Compatible with OpenSearch and OpenSearch Dashboards version
   <version number>" followed by content)
   - Generate markdown with ### headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Infrastructure, Documentation,
   Maintenance, Refactoring
   - Each entry should be a single line with proper PR link formatting

5. **PR Link Format:**
   - Extract PR number from PullRequestSubject
   - Format as: `([#<number>]({repository_url}/pull/<number>))`
   - Example: `([#456](https://github.com/opensearch-project/anomaly-detection/pull/456))`

6. **Important Notes:
   - Every commit should be categorized into exactly one category
   - If you cannot determine the appropriate category from labels OR content analysis, place the entry in an "Unknown" category
   - Do not skip any commits - every entry must appear somewhere in the release notes
   - Prioritize Message over PullRequestSubject for determining category when using fallback analysis

Generate the release notes in proper OpenSearch format:"""
