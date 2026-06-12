#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# Unit tests for lib/shell/version_management.sh
# Run from the repo root: bash tests/shell/test_version_management.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

. "$REPO_ROOT/lib/shell/version_management.sh"

PASS=0
FAIL=0

function assert_equals() {
    local test_name="$1"
    local expected="$2"
    local actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "PASS: $test_name"
        PASS=$((PASS + 1))
    else
        echo "FAIL: $test_name — expected '$expected', got '$actual'"
        FAIL=$((FAIL + 1))
    fi
}

function assert_returns() {
    local test_name="$1"
    local expected_rc="$2"
    shift 2
    "$@" > /dev/null 2>&1
    local actual_rc=$?
    assert_equals "$test_name" "$expected_rc" "$actual_rc"
}

# ---------------------------------------------------------------------------
# Override curl so tests never hit the network.
# MOCK_TAGS_RESPONSE controls what the fake API returns.
# ---------------------------------------------------------------------------
MOCK_TAGS_RESPONSE=""

function curl() {
    # Ignore all curl flags/args and just return the mocked response
    echo "$MOCK_TAGS_RESPONSE"
    return 0
}
export -f curl

# Build a minimal Docker Hub API JSON response for a list of tag names
function make_tags_response() {
    local tags_json=""
    for tag in "$@"; do
        [ -n "$tags_json" ] && tags_json="$tags_json,"
        tags_json="${tags_json}{\"name\":\"${tag}\"}"
    done
    echo "{\"count\":$#,\"next\":null,\"results\":[${tags_json}]}"
}

# ---------------------------------------------------------------------------
# Test: missing arguments
# ---------------------------------------------------------------------------
function test_missing_arguments() {
    is_latest_version "" "opensearch" "2.15.0" > /dev/null 2>&1
    local rc=$?
    assert_equals "missing_registry_returns_error" "1" "$rc"

    is_latest_version "opensearchstaging" "" "2.15.0" > /dev/null 2>&1
    rc=$?
    assert_equals "missing_image_returns_error" "1" "$rc"

    is_latest_version "opensearchstaging" "opensearch" "" > /dev/null 2>&1
    rc=$?
    assert_equals "missing_version_returns_error" "1" "$rc"
}

# ---------------------------------------------------------------------------
# Test: no existing tags — treat candidate as latest
# ---------------------------------------------------------------------------
function test_no_existing_tags() {
    MOCK_TAGS_RESPONSE=$(make_tags_response)
    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "no_existing_tags_returns_0" "0" "$?"
}

# ---------------------------------------------------------------------------
# Test: candidate is the highest version
# ---------------------------------------------------------------------------
function test_candidate_is_highest() {
    MOCK_TAGS_RESPONSE=$(make_tags_response "2.14.0" "2.13.0" "1.3.3")
    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "candidate_higher_than_all_existing_returns_0" "0" "$?"
}

# ---------------------------------------------------------------------------
# Test: candidate equals the current highest (idempotent re-run)
# ---------------------------------------------------------------------------
function test_candidate_equals_highest() {
    MOCK_TAGS_RESPONSE=$(make_tags_response "2.15.0" "2.14.0" "1.3.3")
    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "candidate_equals_highest_existing_returns_0" "0" "$?"
}

# ---------------------------------------------------------------------------
# Test: a higher version already exists — do not tag latest
# ---------------------------------------------------------------------------
function test_higher_version_exists() {
    MOCK_TAGS_RESPONSE=$(make_tags_response "2.15.0" "2.14.0" "1.3.3")
    is_latest_version "opensearchstaging" "opensearch" "1.3.3" > /dev/null 2>&1
    assert_equals "lower_version_than_existing_returns_1" "1" "$?"
}

function test_patch_backport_not_latest() {
    MOCK_TAGS_RESPONSE=$(make_tags_response "2.15.0" "2.14.1" "2.14.0" "1.3.3")
    is_latest_version "opensearchstaging" "opensearch" "2.14.1" > /dev/null 2>&1
    assert_equals "patch_backport_lower_than_current_major_returns_1" "1" "$?"
}

# ---------------------------------------------------------------------------
# Test: non-semver tags are filtered out (latest, major-only, build-suffixed)
# ---------------------------------------------------------------------------
function test_non_semver_tags_ignored() {
    # Only non-semver tags exist — should treat candidate as latest
    MOCK_TAGS_RESPONSE=$(make_tags_response "latest" "2" "3" "2.15.0.3910" "2.15.0-SNAPSHOT")
    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "non_semver_tags_filtered_out_returns_0" "0" "$?"
}

function test_mixed_tags_only_semver_compared() {
    # Mix of semver and non-semver; 2.14.0 is the highest real semver
    MOCK_TAGS_RESPONSE=$(make_tags_response "latest" "2" "2.14.0" "2.14.0.1234" "2.14.0-SNAPSHOT")
    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "only_semver_compared_candidate_wins_returns_0" "0" "$?"
}

# ---------------------------------------------------------------------------
# Test: API unreachable — default to true (conservative)
# ---------------------------------------------------------------------------
function test_api_unreachable() {
    # Override curl to simulate failure
    function curl() { return 1; }
    export -f curl

    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "api_unreachable_defaults_to_latest_returns_0" "0" "$?"

    # Restore working curl mock
    function curl() { echo "$MOCK_TAGS_RESPONSE"; return 0; }
    export -f curl
}

# ---------------------------------------------------------------------------
# Test: pagination — tags span multiple pages
# ---------------------------------------------------------------------------
function test_pagination() {
    # Simulate page 1 pointing to page 2
    local page2_url="https://hub.docker.com/v2/repositories/opensearchstaging/opensearch/tags?page=2"
    local page1="{\"count\":2,\"next\":\"${page2_url}\",\"results\":[{\"name\":\"2.14.0\"}]}"
    local page2="{\"count\":2,\"next\":null,\"results\":[{\"name\":\"2.15.0\"}]}"

    call_count=0
    function curl() {
        call_count=$((call_count + 1))
        if [ "$call_count" -eq 1 ]; then
            echo "$page1"
        else
            echo "$page2"
        fi
        return 0
    }
    export -f curl

    # 2.15.0 is already the highest — candidate 2.15.0 should equal it → return 0
    is_latest_version "opensearchstaging" "opensearch" "2.15.0" > /dev/null 2>&1
    assert_equals "pagination_reads_all_pages_highest_equals_candidate_returns_0" "0" "$?"

    # 2.14.0 is lower than the paginated 2.15.0 → return 1
    is_latest_version "opensearchstaging" "opensearch" "2.14.0" > /dev/null 2>&1
    assert_equals "pagination_reads_all_pages_higher_tag_found_returns_1" "1" "$?"

    # Restore default mock
    function curl() { echo "$MOCK_TAGS_RESPONSE"; return 0; }
    export -f curl
}

# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------
test_missing_arguments
test_no_existing_tags
test_candidate_is_highest
test_candidate_equals_highest
test_higher_version_exists
test_patch_backport_not_latest
test_non_semver_tags_ignored
test_mixed_tags_only_semver_compared
test_api_unreachable
test_pagination

echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
