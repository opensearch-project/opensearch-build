/*
 * SPDX-License-Identifier: Apache-2.0
 */

import assert from "node:assert/strict";
import test from "node:test";

import { findPullRequestNumber } from "../index.js";

test("returns the first associated pull request", async () => {
  const octokit = {
    rest: {
      actions: {
        getWorkflowRun: async (request) => {
          assert.deepEqual(request, {
            owner: "opensearch-project",
            repo: "security",
            run_id: 42,
          });
          return { data: { pull_requests: [{ number: 2411 }] } };
        },
      },
    },
  };

  assert.equal(
    await findPullRequestNumber(octokit, "opensearch-project", "security", 42),
    2411
  );
});

test("returns undefined when no pull request is associated", async () => {
  const octokit = {
    rest: {
      actions: {
        getWorkflowRun: async () => ({ data: { pull_requests: [] } }),
      },
    },
  };

  assert.equal(
    await findPullRequestNumber(octokit, "opensearch-project", "security", 42),
    undefined
  );
});
