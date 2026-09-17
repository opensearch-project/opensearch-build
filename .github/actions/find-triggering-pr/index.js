/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * Derived from peternied/find-triggering-pr, licensed under Apache-2.0.
 */

import * as core from "@actions/core";
import * as github from "@actions/github";
import { pathToFileURL } from "node:url";

export async function findPullRequestNumber(octokit, owner, repo, workflowRunId) {
  const { data: workflowRun } = await octokit.rest.actions.getWorkflowRun({
    owner,
    repo,
    run_id: workflowRunId,
  });

  return workflowRun.pull_requests?.[0]?.number;
}

export async function run() {
  try {
    const workflowRunId = github.context.payload.workflow_run?.id;
    const { owner, repo } = github.context.repo;

    if (!workflowRunId) {
      throw new Error("This action must be run from a workflow_run event.");
    }

    core.info(`Checking workflow run ${workflowRunId}.`);
    const octokit = github.getOctokit(core.getInput("token", { required: true }));
    const prNumber = await findPullRequestNumber(octokit, owner, repo, workflowRunId);

    core.setOutput("pr-number", prNumber ?? "");
    if (prNumber) {
      core.info(`Found pull request #${prNumber}.`);
    } else {
      core.info("No pull request is associated with this workflow run.");
    }
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  run();
}
