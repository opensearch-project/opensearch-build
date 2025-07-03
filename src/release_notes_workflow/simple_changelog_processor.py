# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

"""OpenSearch release notes generator using AI analysis of commit history."""

import argparse
import json
import logging
import os
import time
from typing import Dict, List, Optional

import boto3
import requests
import yaml

from git.git_repository import GitRepository
from system.temporary_directory import TemporaryDirectory


def get_github_token():
    """Get GitHub token from user input."""
    import getpass
    return getpass.getpass("Enter your GitHub API token: ")


def get_latest_version() -> str:
    """Get the latest version folder from the manifests directory."""
    manifests_url = "https://api.github.com/repos/opensearch-project/opensearch-build/contents/manifests"
    
    try:
        response = requests.get(manifests_url)
        if response.status_code == 200:
            contents = response.json()
            
            # Filter for directories that look like version numbers
            version_dirs = []
            for item in contents:
                if item['type'] == 'dir':
                    name = item['name']
                    # Check if it looks like a version (e.g., "3.2.0", "3.1.0", etc.)
                    if name.replace('.', '').replace('-', '').isdigit() or any(char.isdigit() for char in name):
                        version_dirs.append(name)
            
            if version_dirs:
                # Sort versions and get the latest
                version_dirs.sort(key=lambda x: [int(i) if i.isdigit() else i for i in x.replace('-', '.').split('.')], reverse=True)
                latest_version = version_dirs[0]
                print(f"Found latest version: {latest_version}")
                return latest_version
            
    except Exception as e:
        print(f"Error getting latest version: {e}")
    
    # Fallback to hardcoded version
    print("Using fallback version: 3.2.0")
    return "3.2.0"


def fetch_manifest_repos() -> List[str]:
    """Fetch repository names from the latest OpenSearch manifest."""
    # Get the latest version dynamically
    # start of code to comment out during test
    # version = get_latest_version()
    # end of code to comment out during test
    
    # start of test code
    # For 3.1.0 release notes, use 3.1.0 manifest instead of latest
    version = "3.1.0"
    # end of test code
    
    # Try both OpenSearch and OpenSearch Dashboards manifests
    manifest_urls = [
        f"https://raw.githubusercontent.com/opensearch-project/opensearch-build/main/manifests/{version}/opensearch-{version}.yml",
        f"https://raw.githubusercontent.com/opensearch-project/opensearch-build/main/manifests/{version}/opensearch-dashboards-{version}.yml"
    ]
    
    # start of code to comment out during test
    # print(f"Fetching OpenSearch {version} manifests...")
    # end of code to comment out during test
    # start of test code
    print(f"Fetching OpenSearch 3.1.0 manifests...")
    # end of test code
    
    repo_names = set()  # Use set to avoid duplicates
    
    for manifest_url in manifest_urls:
        try:
            print(f"  - Trying: {manifest_url}")
            response = requests.get(manifest_url)
            
            if response.status_code == 200:
                manifest_data = yaml.safe_load(response.text)
                
                for component in manifest_data.get('components', []):
                    repo_url = component.get('repository', '')
                    if 'opensearch-project' in repo_url:
                        repo_name = repo_url.split('/')[-1].replace('.git', '')
                        repo_names.add(repo_name)
                
                print(f"  ✅ Found {len(manifest_data.get('components', []))} components in this manifest")
            else:
                print(f"  ❌ Manifest not found (HTTP {response.status_code})")
                
        except Exception as e:
            print(f"  ❌ Error fetching manifest: {e}")
    
    repo_list = sorted(list(repo_names))
    print(f"Found {len(repo_list)} unique repositories total")
    return repo_list


def get_pull_request_for_commit(repo_name: str, commit_sha: str, headers: dict) -> Optional[dict]:
    """Get the pull request associated with a commit."""
    url = f"https://api.github.com/repos/opensearch-project/{repo_name}/commits/{commit_sha}/pulls"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pulls = response.json()
        if pulls:
            return pulls[0]  # Return the first (most relevant) PR
    
    return None


def get_pull_request_labels(repo_name: str, pr_number: int, headers: dict) -> List[str]:
    """Get labels from a pull request."""
    url = f"https://api.github.com/repos/opensearch-project/{repo_name}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pr_data = response.json()
        labels = pr_data.get("labels", [])
        return [label["name"] for label in labels]
    
    return []


def get_baseline_tag_date(token: str) -> tuple:
    """Get the latest tag and its date from opensearch-build repository."""
    headers = {"Authorization": f"token {token}"}
    
    # Get latest tag from opensearch-build
    # start of code to comment out during test
    # tags_url = "https://api.github.com/repos/opensearch-project/opensearch-build/tags"
    # response = requests.get(tags_url, headers=headers, params={"per_page": 1})
    # end of code to comment out during test
    
    # start of test code
    # For 3.1.0 release notes, get the 3.0.0 tag instead of latest
    tags_url = "https://api.github.com/repos/opensearch-project/opensearch-build/tags"
    response = requests.get(tags_url, headers=headers, params={"per_page": 100})  # Get more tags to find 3.0.0
    # end of test code
    
    if response.status_code == 200:
        tags = response.json()
        if tags:
            # start of code to comment out during test
            # tag_name = tags[0]["name"]
            # end of code to comment out during test
            
            # start of test code
            # For 3.1.0 release notes, find the 3.0.0 tag
            tag_name = "3.0.0"  # Default fallback
            for tag in tags:
                if tag["name"] == "3.0.0":
                    tag_name = tag["name"]
                    break
            # end of test code
            
            # Get the tag's commit date
            # start of code to comment out during test
            # commit_url = f"https://api.github.com/repos/opensearch-project/opensearch-build/commits/{tags[0]['commit']['sha']}"
            # commit_response = requests.get(commit_url, headers=headers)
            # end of code to comment out during test
            
            # start of test code
            # For 3.1.0 release notes, get 3.0.0 tag's commit
            for tag in tags:
                if tag["name"] == "3.0.0":
                    commit_url = f"https://api.github.com/repos/opensearch-project/opensearch-build/commits/{tag['commit']['sha']}"
                    commit_response = requests.get(commit_url, headers=headers)
                    break
            # end of test code
            
            if commit_response.status_code == 200:
                commit_data = commit_response.json()
                tag_date = commit_data["commit"]["committer"]["date"]
                return tag_name, tag_date
    
    return None, None


def fetch_changelog(repo_name: str, token: str, baseline_tag: str = None, baseline_date: str = None) -> str:
    """Fetch changelog or commits since baseline tag for a repository."""
    headers = {"Authorization": f"token {token}"}
    
    # Try to get CHANGELOG.md
    changelog_url = f"https://api.github.com/repos/opensearch-project/{repo_name}/contents/CHANGELOG.md"
    response = requests.get(changelog_url, headers=headers)
    
    if response.status_code == 200:
        import base64
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        print(f"   ✅ Found CHANGELOG.md")
        # start of test code
        # Skip repositories that have CHANGELOG.md files
        print(f"   ⏭️  Skipping {repo_name} - has CHANGELOG.md")
        return f"## {repo_name}\n\nSkipped - has CHANGELOG.md"
        # end of test code
        # start of code to comment out during test
        # return f"## {repo_name}\n\n{content}"
        # end of code to comment out during test
    
    # No changelog found, get commits since baseline tag
    print(f"   ❌ No CHANGELOG.md found, getting commits since opensearch-build tag {baseline_tag}")
    
    if baseline_date:
        # Get ALL commits (without date filtering first, then filter manually)
        commits_url = f"https://api.github.com/repos/opensearch-project/{repo_name}/commits"
        all_commits = []
        page = 1
        
        while True:
            params = {
                "per_page": 100,
                "page": page
            }
            response = requests.get(commits_url, headers=headers, params=params)
            
            if response.status_code != 200:
                break
                
            commits = response.json()
            if not commits:  # No more commits
                break
                
            # Filter commits to only include those after baseline_date
            for commit in commits:
                commit_date = commit["commit"]["committer"]["date"]
                if commit_date >= baseline_date:
                    all_commits.append(commit)
                else:
                    # Once we hit commits older than baseline, we can stop
                    break
            
            # If we found commits older than baseline, stop pagination
            if commits and commits[-1]["commit"]["committer"]["date"] < baseline_date:
                break
                
            page += 1
            
            # Add small delay to avoid rate limiting
            time.sleep(0.1)
        
        if all_commits:
            commit_list = []
            for commit in all_commits:
                # start of test code
                # For 3.1.0 release notes, filter out commits after 3.1.0 release date
                commit_date = commit["commit"]["committer"]["date"]
                if commit_date > "2025-06-24T22:53:00Z":  # 3.1.0 release date
                    continue
                # end of test code
                
                message = commit["commit"]["message"].split('\n')[0]
                commit_sha = commit["sha"]
                
                # Try to get PR for this commit
                pr_info = get_pull_request_for_commit(repo_name, commit_sha, headers)
                
                if pr_info:
                    pr_number = pr_info["number"]
                    pr_url = f"https://github.com/opensearch-project/{repo_name}/pull/{pr_number}"
                    commit_line = f"- {message} ([#{pr_number}]({pr_url}))"
                    
                    # Get PR labels for categorization
                    pr_labels = get_pull_request_labels(repo_name, pr_number, headers)
                    if pr_labels:
                        labels_str = ", ".join(pr_labels)
                        commit_line += f" [Labels: {labels_str}]"
                else:
                    # No PR found, just show the message
                    commit_line = f"- {message}"
                
                commit_list.append(commit_line)
                
                # Small delay to avoid rate limiting
                time.sleep(0.05)
            
            print(f"   ✅ Found {len(all_commits)} commits since {baseline_tag}")
            return f"## {repo_name}\n\n### Commits since opensearch-build tag {baseline_tag}\n\n" + "\n".join(commit_list)
        else:
            print(f"   ⚠️  No commits found since {baseline_tag}")
            return f"## {repo_name}\n\n### No commits since opensearch-build tag {baseline_tag}\n\nNo commits found."
    
    print(f"   ❌ Could not fetch commits")
    return f"## {repo_name}\n\nNo data available."


def post_process_release_notes(combined_analysis: str) -> str:
    """Post-process the release notes to check if the AI made a mistake."""
    print("Post-processing release notes to check for mistakes...")
    
    import re
    
    # Dictionary to store entries by category
    categories = {
        'Breaking Changes': [],
        'Features': [],
        'Enhancements': [],
        'Bug Fixes': [],
        'Infrastructure': [],
        'Documentation': [],
        'Maintenance': [],
        'Refactoring': [],
        'Other': []
    }
    
    # Track PR numbers to detect duplicates and mismatches
    pr_tracker = {}  # pr_number -> list of (category, repo, text, commit_hash)
    
    # Split the analysis into lines
    lines = combined_analysis.split('\n')
    current_category = None
    current_repo = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a main category header (## CATEGORY)
        if line.startswith('## '):
            category_name = line[3:].strip().title()
            # Map common variations to standard names
            category_mapping = {
                'Bug Fixes': 'Bug Fixes',
                'Bugfixes': 'Bug Fixes',
                'Bug Fix': 'Bug Fixes',
                'Features': 'Features',
                'Feature': 'Features',
                'Enhancements': 'Enhancements',
                'Enhancement': 'Enhancements',
                'Infrastructure': 'Infrastructure',
                'Documentation': 'Documentation',
                'Docs': 'Documentation',
                'Maintenance': 'Maintenance',
                'Refactoring': 'Refactoring',
                'Refactor': 'Refactoring',
                'Breaking Changes': 'Breaking Changes',
                'Breaking': 'Breaking Changes',
                'Other': 'Other'
            }
            current_category = category_mapping.get(category_name, category_name)
            current_repo = None
            continue
            
        # Check if this is an entry (starts with * or -)
        if line.startswith('* ') or line.startswith('- '):
            if current_category:
                # Since we no longer have repository subsections, extract repo from PR URL
                repo_match = re.search(r'https://github\.com/opensearch-project/([^/]+)/pull/', line)
                current_repo = repo_match.group(1) if repo_match else 'unknown'
                # Extract PR number and commit hash from the line
                pr_match = re.search(r'\[#(\d+)\]\(https://github\.com/opensearch-project/[^/]+/pull/(\d+)\)', line)
                
                if pr_match:
                    commit_number = pr_match.group(1)
                    pr_number = pr_match.group(2)
                    
                    # Check for mismatched commit/PR numbers
                    if commit_number != pr_number:
                        print(f"  ⚠️  Mismatched commit/PR numbers: #{commit_number} vs PR #{pr_number} - moving to Other")
                        categories['Other'].append({
                            'repo': current_repo,
                            'text': line + f" [MISMATCH: commit #{commit_number} vs PR #{pr_number}]"
                        })
                        continue
                    
                    # Track this PR number
                    if pr_number not in pr_tracker:
                        pr_tracker[pr_number] = []
                    
                    pr_tracker[pr_number].append({
                        'category': current_category,
                        'repo': current_repo,
                        'text': line,
                        'commit_hash': commit_number
                    })
                
                # Store the entry with repository info
                entry = {
                    'repo': current_repo,
                    'text': line
                }
                if current_category in categories:
                    categories[current_category].append(entry)
                else:
                    # If category not recognized, put in Other
                    categories['Other'].append(entry)
    
    # Process duplicates - remove from ALL sections and put only in Other
    duplicates_moved = 0
    for pr_number, occurrences in pr_tracker.items():
        if len(occurrences) > 1:
            # Collect all categories where this PR appeared
            duplicate_categories = [occ['category'] for occ in occurrences]
            duplicate_locations = ", ".join(sorted(set(duplicate_categories)))
            
            print(f"  ⚠️  Duplicate PR #{pr_number} found in {len(occurrences)} categories ({duplicate_locations}) - removing from all sections and moving to Other")
            
            # Remove from ALL original categories
            for occurrence in occurrences:
                original_category = occurrence['category']
                original_repo = occurrence['repo']
                original_text = occurrence['text']
                
                # Find and remove the entry from its original category
                if original_category in categories:
                    categories[original_category] = [
                        entry for entry in categories[original_category]
                        if not (entry['repo'] == original_repo and entry['text'] == original_text)
                    ]
            
            # Add to Other with all duplicate locations listed
            first_occurrence = occurrences[0]
            categories['Other'].append({
                'repo': first_occurrence['repo'],
                'text': first_occurrence['text'] + f" [DUPLICATE: found in {duplicate_locations}]"
            })
            duplicates_moved += len(occurrences)
    
    if duplicates_moved > 0:
        print(f"  ✅ Moved {duplicates_moved} duplicate entries to Other section")
    
    # Build the final output
    final_output = []
    
    for category, entries in categories.items():
        if not entries:
            continue
            
        # Add category header
        final_output.append(f"## {category}")
        final_output.append("")
        
        # Add all entries directly under the category without repository grouping
        for entry in entries:
            final_output.append(entry['text'])
        
        final_output.append("")
    
    result = '\n'.join(final_output)
    print(f"✅ Post-processing complete - combined {sum(len(entries) for entries in categories.values())} entries across {len([cat for cat, entries in categories.items() if entries])} categories")
    return result


def analyze_with_bedrock(content: str, repo_name: str) -> str:
    """Analyze content with Bedrock Claude 3.7 v2."""
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Extract version info if available
    version = "Latest"
    if '[' in repo_name and ']' in repo_name:
        import re
        version_match = re.search(r'\[(.*?)\]', repo_name)
        if version_match:
            version = version_match.group(1)
    
    repository_url = f"https://github.com/opensearch-project/{repo_name}"
    
    prompt = f"""I need you to generate OpenSearch plugin release notes from commit data. Please follow the category-first format where repositories are grouped under main category sections.

**Batch Information:**
- Batch Name: {repo_name}
- Version: {version}

**Commit Data:**
{content}

**Instructions:**

1. **Category-First Structure:**
   - Create main sections (##) for each category that has entries
   - Only include categories and repositories that have entries

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
   - If no labels match, analyze the Message content and PullRequestSubject to determine the appropriate category following below guidelines:
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
   - Use PullRequestSubject as the main content for each entry
   - Extract PR number from PullRequestSubject (format: (#123))
   - Format: `* <description> ([#<number>]({repository_url}/pull/<number>))`
   - Always use asterisk (*) for bullet points
   - Always wrap PR links in parentheses
   - **IMPORTANT**: Capitalize the first letter of every entry description (after the asterisk and space)

5. **Output Requirements:**
   - Generate markdown with ### headers for each category
   - Only include categories that have entries
   - Sort categories in this order: Breaking Changes, Features, Enhancements, Bug Fixes, Infrastructure, Documentation, Maintenance, Refactoring, Other
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

Generate the release notes in proper OpenSearch format:
Generate the release notes in category-first format like this example:

## FEATURES
* Feature description ([#123](https://github.com/opensearch-project/alerting/pull/123))
* Another feature description ([#124](https://github.com/opensearch-project/security/pull/124))

## ENHANCEMENTS
* Enhancement description ([#125](https://github.com/opensearch-project/ml-commons/pull/125))
* Another enhancement description ([#126](https://github.com/opensearch-project/neural-search/pull/126))"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 8000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    
    response = bedrock.invoke_model(
        modelId='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
        body=json.dumps(body),
        contentType='application/json'
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']


def main():
    parser = argparse.ArgumentParser(description="Simple OpenSearch changelog processor")
    parser.add_argument("--token", help="GitHub token")
    parser.add_argument("--max-repos", type=int, help="Max repositories to process (default: all)")
    args = parser.parse_args()
    
    # Get token
    token = args.token or get_github_token()
    
    # Get the latest version for use throughout the script
    version = get_latest_version()
    
    # Get repositories
    repo_names = fetch_manifest_repos()
    if args.max_repos:
        repo_names = repo_names[:args.max_repos]
    
    # Get baseline tag from opensearch-build
    print("Getting baseline tag from opensearch-build repository...")
    baseline_tag, baseline_date = get_baseline_tag_date(token)
    if baseline_tag:
        print(f"Using baseline tag: {baseline_tag} (date: {baseline_date})")
    else:
        print("⚠️  Could not get baseline tag, will use recent commits")
    
    print(f"\nFetching and processing {len(repo_names)} repositories individually...")
    
    # Process each repository individually
    all_analyses = []
    
    for i, repo_name in enumerate(repo_names, 1):
        print(f"[{i}/{len(repo_names)}] Processing {repo_name}...")
        
        try:
            # Fetch repository data
            content = fetch_changelog(repo_name, token, baseline_tag, baseline_date)
            
            # Skip repositories that were marked as "Skipped - has CHANGELOG.md"
            # start of test code
            if "Skipped - has CHANGELOG.md" in content:
                print(f"⏭️ Excluded {repo_name} from analysis (has CHANGELOG.md)")
                continue
            # end of test code
            # start of code to comment out during test
            # if "Skipped - has CHANGELOG.md" in content:
            #     print(f"⏭️ Excluded {repo_name} from analysis (has CHANGELOG.md)")
            #     continue
            # end of code to comment out during test
            
            print(f"✅ Fetched {repo_name}")
            
            # Save individual repository content for inspection
            repo_filename = f"{repo_name}_data.md"
            with open(repo_filename, "w") as f:
                f.write(content)
            print(f"  - Repository data saved to: {repo_filename}")
            
            # Run AI analysis on this repository with retry logic
            print(f"  - Running AI analysis on {repo_name}...")
            max_retries = 3
            retry_delay = 5  # Start with 5 seconds
            
            for attempt in range(max_retries):
                try:
                    repo_analysis = analyze_with_bedrock(content, f"OpenSearch {version} - {repo_name}")
                    all_analyses.append(repo_analysis)
                    
                    # Save individual repository analysis with version number
                    repo_analysis_filename = f"{repo_name}_{version}.md"
                    with open(repo_analysis_filename, "w") as f:
                        f.write(f"# OpenSearch {version} Release Notes - {repo_name}\n\n{repo_analysis}")
                    
                    print(f"  ✅ {repo_name} analysis completed and saved to {repo_analysis_filename}")
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    error_str = str(e).lower()
                    is_throttling = any(keyword in error_str for keyword in [
                        'throttling', 'rate limit', 'too many requests', 'quota', 'limit exceeded'
                    ])
                    
                    if is_throttling and attempt < max_retries - 1:
                        print(f"  ⚠️  Throttling error on {repo_name}, attempt {attempt + 1}/{max_retries}")
                        print(f"  ⏳ Waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        print(f"  ❌ Error analyzing {repo_name} (attempt {attempt + 1}/{max_retries}): {e}")
                        if attempt == max_retries - 1:
                            print(f"  ❌ Max retries exceeded for {repo_name}, skipping...")
                            break
            
            # Small delay between repositories to avoid rate limiting
            if i < len(repo_names):
                print(f"  - Waiting before next repository...")
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Error processing {repo_name}: {e}")
            continue
    
    # Clean up temporary repository data files (keep the analysis files)
    print(f"\nCleaning up temporary data files...")
    import os
    for repo_name in repo_names:
        try:
            # Remove repository data files (temporary)
            repo_data_file = f"{repo_name}_data.md"
            if os.path.exists(repo_data_file):
                os.remove(repo_data_file)
                
        except Exception as e:
            print(f"Warning: Could not remove {repo_name} data file: {e}")
    
    print(f"✅ Temporary files cleaned up")
    print(f"Successfully processed {len(all_analyses)} repositories individually")
    print(f"Individual release notes saved as: repositoryname_{version}.md")


if __name__ == "__main__":
    main()
