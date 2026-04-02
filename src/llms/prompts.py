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
   Release Notes followed by a blank line and then "Compatible with OpenSearch and OpenSearch Dashboards
   version <version number>" followed by content)

**Entry Format:**
   - Each entry Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - If the line has multiple links format: `* <description> ([#<number>]({repository_url}/pull/<number>),
     [#<number>]({repository_url}/pull/<number>))` - Note: Only one set of outer parentheses should be used for all PR links.
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
   - If no labels match, analyze the Message content, PullRequestSubject, and PR Description to determine the appropriate category following below guidelines:
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

3. **Content filtering:**
   - Do not add the pull request that has title starting with "[AUTO] Increment version to".

4. **Entry Format:**
   - Use the PullRequestSubject and PR Description as input, but rewrite each entry as a concise, clear one-line
     summary. The target audience is end-users, operators, and system administrators — not developers.
     Do not simply copy the PR subject verbatim; improve clarity and consistency.
   - Extract PR number from PullRequestSubject (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - Make sure first character of each entry is capitalized.

5. **Output Requirements:**
   - The main heading with ## should be "version number Release Notes" (e.g., For version 3.2.0 ## Version 3.2.0
   Release Notes followed by a blank line and then "Compatible with OpenSearch and OpenSearch Dashboards
   version <version number>" followed by content)
   - Generate markdown with ### headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Infrastructure, Documentation,
   Maintenance, Refactoring
   - Each entry should be a single line with proper PR link formatting

6. **PR Link Format:**
   - Extract PR number from PullRequestSubject
   - Format as: `([#<number>]({repository_url}/pull/<number>))`
   - Example: `([#456](https://github.com/opensearch-project/anomaly-detection/pull/456))`

7. **Important Notes:**
   - Every commit should be categorized into exactly one category
   - If you cannot determine the appropriate category from labels OR content analysis, place the entry in an "Unknown" category
   - Do not skip any commits - every entry must appear somewhere in the release notes
   - Prioritize Message over PullRequestSubject for determining category when using fallback analysis

8. **Borderline Calls:**
   After the release notes, add a section starting with `<!-- BORDERLINE_CALLS` and ending with `-->`.
   Inside this HTML comment, list any judgment calls where the categorization or inclusion decision was debatable.
   For each, reference the PR number and briefly explain the decision and alternatives. Example:
   ```
   <!-- BORDERLINE_CALLS
   - #1234: Placed in **Enhancements** — could also be **Bug Fixes** since it changes existing behavior to fix a usability issue.
   - #5678: Placed in **Maintenance** — borderline with **Infrastructure**, chose Maintenance because it's a dependency update.
   -->
   ```
   If there are no borderline calls, omit this section entirely.

Generate the release notes in proper OpenSearch format:"""

AI_RELEASE_NOTES_PROMPT_COMMIT_OPENSEARCH = """Generate release notes for {component_name} {version} from the commit data below.

Repository: {repository_url}

**Commit Data:**
{commits_text}

**Filtering (apply first):**
- Exclude PRs titled "[AUTO] Increment version to...".
- Exclude PRs with the `skip-changelog` label.
- Exclude commit/revert pairs.
- Exclude non-user-facing changes: test-only changes, CI/build changes, GitHub Actions bumps,
  release machinery (changelogs, READMEs), internal refactoring with no behavior/API/config
  change, maintainer list changes, and incremental PRs for a feature already covered by another entry.
- Exclusion rules override label-based categorization.
- When uncertain, include — a human reviewer can remove it later.

**Categorization (for surviving PRs):**
- Match labels first (case-insensitive, partial match):
  "breaking"→Breaking Changes, "feature"/"feat"→Features, "enhancement"/"improve"→Enhancements,
  "bug"/"fix"/"bugfix"→Bug Fixes, "maintenance"/"version"/"support"→Maintenance
- If no label matches, categorize by content:
  Features=net new functionality, Enhancements=improves existing feature,
  Bug Fixes=fixes a defect, Maintenance=dependency updates and routine upkeep.
- Only use these 5 categories. If none fit, use "Unknown".

**Entry format:**
`* <concise one-line summary for end-users/operators> ([#<number>]({repository_url}/pull/<number>))`
- Rewrite PR subjects for clarity; do not copy verbatim. Capitalize first character.
- Group related PRs into a single entry when appropriate.

Example rewrites:
  PR Subject: "Add support for warm index pre-loading of global ordinals on replica shards with segment replication (#20650)"
  Good: * Add index warmer support for replica shards using segment replication ([#20650](https://github.com/opensearch-project/OpenSearch/pull/20650))
  Bad:  * Add WarmerRefreshListener to NRTReplicationEngine to warm replica shards ([#20650](https://github.com/opensearch-project/OpenSearch/pull/20650))
  Why: The "good" version uses user-facing language. The "bad" version leaks internal class names.

**Output format:**

## Version {version} Release Notes

Compatible with OpenSearch and OpenSearch Dashboards version {version}

### Breaking Changes
* ...

### Features
* ...

- Only include categories that have entries.
- Order: Breaking Changes, Features, Enhancements, Bug Fixes, Maintenance.

**Borderline calls:**
After the release notes, add `<!-- BORDERLINE_CALLS ... -->` listing any debatable
filtering, categorization, or grouping decisions with PR numbers and brief rationale.
Omit if none.

Generate the release notes in proper OpenSearch format:"""
