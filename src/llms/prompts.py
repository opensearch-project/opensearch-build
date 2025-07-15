#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

"""Prompt constants for LLM-based functionality."""

# AI Release Notes Generator prompt
AI_RELEASE_NOTES_PROMPT_CHANGELOG = """Generate OpenSearch plugin release notes for a single component from the changelog.

**Component Information:**
- Component: {repo_name}
- Version: {version}
- Repository: {repository_url}

**Instructions:**
1. **Use the right section from the CHANGELOG**
   - the only section you will use is one that has the wor unreleased in it or one that has #.x
2. **Label-based Categorization Logic:**
   - First, check if any labels match these categories (case-insensitive, partial matches allowed):
     * "breaking change" or "breaking" → Breaking Changes
     * "feature" or "feat" → Features  
     * "enhancement" or "improve" → Enhancements
     * "bug" or "fix" or "bugfix" → Bug Fixes
     * "infrastructure" or "ci" or "test" → Infrastructure
     * "documentation" or "docs" → Documentation
     * "maintenance" or "version" or "support" → Maintenance
     * "refactor" or "refactoring" → Refactoring
   - If a commit has multiple labels that match different categories above, place it in the "Other" category
   - If a commit has no labels or labels that don't match any of the above categories, proceed to fallback analysis

3. **Fallback Message Analysis:**
   - If no labels match, analyze the Message content to determine the appropriate category following below guidelines:
    * Features: A change that introduce a net new unit of functionality of a software system that satisfies a requirement, 
    represents a design decision, and provides a potential configuration option. As for improvement on existing features, 
    use the Enhancement category. As for fixes on existing features, use the Bug Fixes category. Example: "Add start/stop batch actions on detector list page"
    * Enhancements: A change that improves the performance, usability, or reliability of an existing feature without changing its core functionality. Example: "Improve detector list page performance"
    * Bug Fixes: A change that resolves an issue or defect in the software. Example: "Fix issue with detector creation form validation"
    * Infrastructure: A change that modifies the underlying architecture, build process, or deployment of the software Example: "Update CI/CD pipeline for better reliability"
    * Documentation: A change that updates or adds documentation, such as README files, user guides, or API docs. Example: "Update README with new installation instructions"
    * Maintenance: A change that involves routine upkeep, such as version updates, dependency management, or minor tweaks that do not fit other categories. Example: "Update dependencies to latest versions"
    * Refactoring: A change that improves the internal structure of the code without changing its external behavior. Example: "Refactor detector service for better readability or Make ClusterDetailsEventProcessor and all its access methods non-static"
    * Other: If the commit cannot be clearly categorized into any of the above categories through message analysis, place it in "Other"
   - Do not lose any commit information, even if it doesn't match any category

4. **Entry Format:**
   - Use commit message as the main content for each entry
   - Extract PR number from commit message (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - **IMPORTANT**: Capitalize the first letter of every entry description (after the asterisk and space)

5. **Output Requirements:**
   - Generate markdown with ## headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Infrastructure, Documentation, Maintenance, Refactoring, Other
   - Each entry should be a single line with proper PR link formatting

6. **PR Link Format:**
   - Extract PR number from commit message
   - Format as: `([#<number>]({repository_url}/pull/<number>))`
   - Example: `([#456]({repository_url}/pull/456))`
   
7. **Important Notes:**
   - Every commit should be categorized into exactly one category
   - If you cannot determine the appropriate category from labels OR content analysis, place the entry in an "Other" category
   - Do not skip any commits - every entry must appear somewhere in the release notes
   - Prioritize GitHub PR labels over commit message analysis when available

Generate the release notes in category-first format like this example:
## Features
* Feature description ([#123]({repository_url}/pull/123))
* Another feature description ([#124]({repository_url}/pull/124))

## Enhancements
* Enhancement description ([#125]({repository_url}/pull/125))
* Another enhancement description ([#126]({repository_url}/pull/126))

## Bug Fixes
* Bug fix description ([#127]({repository_url}/pull/127))
"""

AI_RELEASE_NOTES_PROMPT_COMMIT = """Generate OpenSearch plugin release notes for a single component from the ACTUAL commit data provided below.
DO NOT invent or fabricate any commits or pull requests that are not in the data provided.
ONLY use the commits that are provided in the formatted_content below.

**Component Information:**
- Component: {repo_name}
- Version: {version}
- Repository: {repository_url}

**Actual Commit Data:**
{formatted_content}

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
   - If a commit has multiple labels that match different categories above, place it in the "Other" category
   - If a commit has no labels or labels that don't match any of the above categories, proceed to fallback analysis

2. **Fallback Message Analysis:**
   - If no labels match, analyze the Message content to determine the appropriate category following below guidelines:
    * Features: A change that introduce a net new unit of functionality of a software system that satisfies a requirement, 
    represents a design decision, and provides a potential configuration option. As for improvement on existing features, 
    use the Enhancement category. As for fixes on existing features, use the Bug Fixes category. Example: "Add start/stop batch actions on detector list page"
    * Enhancements: A change that improves the performance, usability, or reliability of an existing feature without changing its core functionality. Example: "Improve detector list page performance"
    * Bug Fixes: A change that resolves an issue or defect in the software. Example: "Fix issue with detector creation form validation"
    * Infrastructure: A change that modifies the underlying architecture, build process, or deployment of the software Example: "Update CI/CD pipeline for better reliability"
    * Documentation: A change that updates or adds documentation, such as README files, user guides, or API docs. Example: "Update README with new installation instructions"
    * Maintenance: A change that involves routine upkeep, such as version updates, dependency management, or minor tweaks that do not fit other categories. Example: "Update dependencies to latest versions"
    * Refactoring: A change that improves the internal structure of the code without changing its external behavior. Example: "Refactor detector service for better readability or Make ClusterDetailsEventProcessor and all its access methods non-static"
    * Other: If the commit cannot be clearly categorized into any of the above categories through message analysis, place it in "Other"
   - Do not lose any commit information, even if it doesn't match any category

3. **Entry Format:**
   - Use commit message as the main content for each entry
   - Extract PR number from commit message (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - **IMPORTANT**: Capitalize the first letter of every entry description (after the asterisk and space)

4. **Output Requirements:**
   - Generate markdown with ## headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Infrastructure, Documentation, Maintenance, Refactoring, Other
   - Each entry should be a single line with proper PR link formatting

5. **PR Link Format:**
   - Extract PR number from commit message
   - Format as: `([#<number>]({repository_url}/pull/<number>))`
   - Example: `([#456]({repository_url}/pull/456))`
   
6. **Important Notes:**
   - Every commit should be categorized into exactly one category
   - If you cannot determine the appropriate category from labels OR content analysis, place the entry in an "Other" category
   - Do not skip any commits - every entry must appear somewhere in the release notes
   - Prioritize GitHub PR labels over commit message analysis when available

Generate the release notes in category-first format like this example:
## Features
* Feature description ([#123]({repository_url}/pull/123))
* Another feature description ([#124]({repository_url}/pull/124))

## Enhancements
* Enhancement description ([#125]({repository_url}/pull/125))
* Another enhancement description ([#126]({repository_url}/pull/126))

## Bug Fixes
* Bug fix description ([#127]({repository_url}/pull/127))
"""
