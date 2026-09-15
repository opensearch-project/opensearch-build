/*
 * SPDX-License-Identifier: Apache-2.0
 */

import assert from "node:assert/strict";
import test from "node:test";

import {
  evaluatePullRequest,
  inspectAndMerge,
  lines,
} from "../index.js";

const pullRequest = {
  state: "open",
  user: { login: "opensearch-ci-bot" },
  head: { sha: "abc123" },
};
const files = [{ filename: "manifests/3.0.0/opensearch.yml" }];
const checks = [
  { name: "CI", status: "completed", conclusion: "success" },
  { name: "Lint", status: "completed", conclusion: "neutral" },
];

test("normalizes newline-separated inputs", () => {
  assert.deepEqual(lines(" first \n\n second\n"), ["first", "second"]);
});

test("accepts an eligible pull request", () => {
  assert.deepEqual(
    evaluatePullRequest(
      pullRequest,
      files,
      checks,
      ["opensearch-ci-bot"],
      ["manifests/*/*.yml"]
    ),
    { eligible: true, reason: "eligible" }
  );
});

test("rejects a disallowed author", () => {
  assert.equal(
    evaluatePullRequest(pullRequest, files, checks, ["someone-else"], ["**"]).reason,
    "author-not-allowed"
  );
});

test("reports every disallowed file", () => {
  const result = evaluatePullRequest(
    pullRequest,
    [...files, { filename: "README.md" }, { filename: "build.sh" }],
    checks,
    ["opensearch-ci-bot"],
    ["manifests/*/*.yml"]
  );

  assert.equal(result.reason, "files-not-allowed");
  assert.deepEqual(result.disallowedFiles, ["README.md", "build.sh"]);
});

test("rejects pending and unsuccessful checks", () => {
  const result = evaluatePullRequest(
    pullRequest,
    files,
    [
      ...checks,
      { name: "Pending", status: "in_progress", conclusion: null },
      { name: "Failed", status: "completed", conclusion: "failure" },
    ],
    ["opensearch-ci-bot"],
    ["**"]
  );

  assert.equal(result.reason, "checks-not-successful");
  assert.deepEqual(
    result.incompleteChecks.map((check) => check.name),
    ["Pending", "Failed"]
  );
});

test("paginates files and checks and pins the merge to the inspected SHA", async () => {
  const paginateCalls = [];
  let mergeRequest;
  let commentRequest;
  const listFiles = Symbol("listFiles");
  const listForRef = Symbol("listForRef");
  const octokit = {
    paginate: async (endpoint, request) => {
      paginateCalls.push({ endpoint, request });
      return endpoint === listFiles ? files : checks;
    },
    rest: {
      pulls: {
        get: async () => ({ data: pullRequest }),
        listFiles,
        merge: async (request) => {
          mergeRequest = request;
          return { data: { merged: true, sha: "merge123" } };
        },
      },
      checks: { listForRef },
      issues: {
        createComment: async (request) => {
          commentRequest = request;
        },
      },
    },
  };

  const result = await inspectAndMerge({
    octokit,
    owner: "opensearch-project",
    repo: "opensearch-build",
    pullRequestNumber: 99,
    allowedAuthors: ["opensearch-ci-bot"],
    allowedFiles: ["manifests/*/*.yml"],
    mergeMethod: "squash",
  });

  assert.deepEqual(result, {
    merged: true,
    reason: "merged",
    mergeCommitSha: "merge123",
  });
  assert.equal(paginateCalls.length, 2);
  assert.equal(paginateCalls[0].request.per_page, 100);
  assert.equal(paginateCalls[1].request.per_page, 100);
  assert.equal(mergeRequest.sha, "abc123");
  assert.equal(mergeRequest.merge_method, "squash");
  assert.equal(commentRequest.issue_number, 99);
});

test("rejects an invalid merge method before calling GitHub", async () => {
  await assert.rejects(
    inspectAndMerge({
      octokit: {},
      owner: "opensearch-project",
      repo: "opensearch-build",
      pullRequestNumber: 99,
      allowedAuthors: [],
      allowedFiles: [],
      mergeMethod: "invalid",
    }),
    /Invalid merge-type/
  );
});
