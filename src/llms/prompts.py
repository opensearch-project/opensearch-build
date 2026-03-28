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

AI_RELEASE_NOTES_PROMPT_COMMIT_OPENSEARCH = """I need you to generate OpenSearch component release notes from commit data. Please follow the OpenSearch release notes format exactly.

**Component Information:**
- Component Name: {component_name}
- Version: {version}
- Repository URL: {repository_url}

**Commit Data:**
{commits_text}

**Instructions:**

1. **Content filtering — apply BEFORE categorization:**
   - Do not add the pull request that has title starting with "[AUTO] Increment version to".
   - Do not add any PR with the `skip-changelog` label, regardless of content.
   - Exclude any commit/revert pairs as the net result is no change.
   - **Exclude the following non-user-facing changes:**
     * Test additions, modifications, fixes, or refactoring (including flaky test fixes, new integration tests,
       test infrastructure improvements, and test cleanup). A PR whose description says "Add test for X" or
       "Cleanup X in tests" is non-user-facing even if the underlying feature is user-facing.
     * Build and CI changes: GitHub Actions version bumps (e.g. actions/setup-java, actions/upload-artifact,
       peter-evans/create-pull-request, lycheeverse/lychee-action, tj-actions/*), Gradle build changes,
       Docker base image updates, CI pipeline configuration.
     * Dependency bumps that only affect test fixtures or build tooling (e.g. bumps under /test/fixtures/,
       /buildSrc/, or test-only libraries like wiremock).
     * Release machinery: changelog fixes, release notes commits, README edits.
     * Internal code refactoring that does not change any user-facing behavior, API, or configuration.
       This includes deprecation warning fixes, code cleanup, and removing unused internal code/plugins.
     * Maintainer list changes.
     * Incremental PRs for a larger feature (these should already have one entry from the main PR).
   - A PR matching an exclusion rule above must be excluded even if its labels would match a category.
   - Use the commit message, PR description, and labels to make this judgment.
   - When uncertain whether a change is user-facing, **include it** — a human reviewer can remove it later.

2. **Categorization — only for PRs that survive filtering:**
   - First, check if any labels match these categories (case-insensitive, partial matches allowed):
     * "breaking change" or "breaking" → Breaking Changes
     * "feature" or "feat" → Features
     * "enhancement" or "improve" → Enhancements
     * "bug" or "fix" or "bugfix" → Bug Fixes
     * "maintenance" or "version" or "support" → Maintenance
   - If no labels match, analyze the Message content, PullRequestSubject, and PR Description to determine
     the appropriate category:
     * Features: A net new unit of functionality that satisfies a requirement, represents a design decision,
       and provides a potential configuration option. For improvements on existing features, use Enhancements.
       For fixes on existing features, use Bug Fixes.
     * Enhancements: Improves the performance, usability, or reliability of an existing feature without
       changing its core functionality.
     * Bug Fixes: Resolves an issue or defect in the software.
     * Maintenance: Routine upkeep such as dependency updates that ship in the distribution.
   - Do not use "Infrastructure", "Documentation", or "Refactoring" as categories. Changes that would
     belong to those categories should have been excluded by the filtering step. If a PR survived filtering
     but does not fit any of the above categories, place it in "Maintenance".

3. **Entry Format:**
   - Use the PullRequestSubject and PR Description as input, but rewrite each entry as a concise, clear one-line
     summary. The target audience is OpenSearch users — end-users, operators, and system administrators — not developers.
     Do not simply copy the PR subject verbatim; improve clarity and consistency.
   - Extract PR number from PullRequestSubject (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - Make sure first character of each entry is capitalized.
   - Group related commits into a single entry when appropriate (e.g., multiple PRs implementing parts of the same
     feature, or a series of dependency bumps for the same library).

4. **Output Requirements:**
   - The main heading with ## should be "version number Release Notes" (e.g., For version 3.2.0 ## Version 3.2.0
   Release Notes followed by a blank line and then "Compatible with OpenSearch and OpenSearch Dashboards
   version <version number>" followed by content)
   - Generate markdown with ### headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Maintenance
   - Each entry should be a single line with proper PR link formatting

5. **PR Link Format:**
   - Extract PR number from PullRequestSubject
   - Format as: `([#<number>]({repository_url}/pull/<number>))`
   - Example: `([#456](https://github.com/opensearch-project/OpenSearch/pull/456))`

6. **Important Notes:**
   - If you cannot determine the appropriate category from labels OR content analysis, place the entry in "Maintenance"
   - Prioritize Message over PullRequestSubject for determining category when using fallback analysis

7. **Borderline Calls:**
   After the release notes, add a section starting with `<!-- BORDERLINE_CALLS` and ending with `-->`.
   Inside this HTML comment, list any judgment calls where the categorization, inclusion, or exclusion decision
   was debatable. For each, reference the PR number and briefly explain the decision and alternatives. Examples:
   - A PR labeled `bug` that reads more like a behavioral change
   - Grouping multiple PRs into a single entry
   - Including a PR that could reasonably be considered non-user-facing
   - Excluding a PR that could reasonably be considered user-facing
   - Choosing one category over another when both fit

   Format:
   ```
   <!-- BORDERLINE_CALLS
   - #1234: Excluded as non-user-facing (test fix) — but it changes test infrastructure that plugin authors rely on, so could be included under Infrastructure.
   - #5678: Placed in **Enhancements** — could also be **Bug Fixes** since it changes existing behavior to fix a usability issue.
   - #9012 + #9013: Grouped into one entry — both implement parts of the same feature.
   -->
   ```
   If there are no borderline calls, omit this section entirely.

Generate the release notes in proper OpenSearch format:"""
