#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a library of all version management related functions.
# Source this file in your scripts:
#   . path/to/lib/shell/version_management.sh

# Determines whether the given version is the highest published semver tag
# for the specified image in a Docker Hub registry.
#
# Queries hub.docker.com/v2/repositories/<registry>/<image>/tags, filters
# results to strict X.Y.Z shaped tags only, and compares using sort -V.
# Tags like "latest", "2", "2.15.0.3910", or snapshot suffixes are excluded.
#
# Usage:
#   is_latest_version <registry> <image> <version>
#
# Arguments:
#   registry  Docker Hub organization name, e.g. "opensearchstaging"
#   image     Docker image name, e.g. "opensearch"
#   version   Semver string to evaluate, e.g. "2.15.0"
#
# Returns:
#   0 if <version> is >= the highest existing semver tag, or no semver tags exist
#   1 if a higher semver tag already exists in the registry
#
function is_latest_version() {
    local registry="$1"
    local image="$2"
    local version="$3"

    if [ -z "$registry" ] || [ -z "$image" ] || [ -z "$version" ]; then
        echo "Error: is_latest_version requires <registry> <image> <version>" >&2
        return 1
    fi

    local api_url="https://hub.docker.com/v2/repositories/${registry}/${image}/tags?page_size=100"
    local all_tags=()
    local next_url="$api_url"

    echo "Querying Docker Hub for existing tags of ${registry}/${image} ..."

    while [ -n "$next_url" ] && [ "$next_url" != "null" ]; do
        local response
        response=$(curl -sf --max-time 30 "$next_url" 2>/dev/null) || {
            echo "Warning: Unable to reach Docker Hub API at ${next_url}. Assuming ${version} is latest." >&2
            return 0
        }

        # Extract tag names from JSON response
        local page_tags
        page_tags=$(echo "$response" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"$//')
        while IFS= read -r tag; do
            [ -n "$tag" ] && all_tags+=("$tag")
        done <<< "$page_tags"

        # Extract next page URL, unescaping \u0026 -> &
        next_url=$(echo "$response" | grep -o '"next":"[^"]*"' | sed 's/"next":"//;s/"$//;s/\\u0026/\&/g')
    done

    # Filter to strict semver X.Y.Z only — excludes "latest", "2", "2.15.0.3910", snapshots, etc.
    local semver_tags=()
    for tag in "${all_tags[@]}"; do
        if [[ "$tag" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            semver_tags+=("$tag")
        fi
    done

    if [ ${#semver_tags[@]} -eq 0 ]; then
        echo "No existing semver tags found for ${registry}/${image}. Treating ${version} as latest."
        return 0
    fi

    # Include the candidate version and find the highest using version-aware sort
    semver_tags+=("$version")
    local highest
    highest=$(printf '%s\n' "${semver_tags[@]}" | sort -V | tail -n1)

    if [ "$highest" = "$version" ]; then
        echo "${version} is the highest semver tag for ${registry}/${image} — will tag as :latest"
        return 0
    else
        echo "${version} is NOT the highest semver tag for ${registry}/${image} (highest existing: ${highest}) — skipping :latest"
        return 1
    fi
}
