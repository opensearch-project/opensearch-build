/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * Derived from peternied/discerning-merger, licensed under Apache-2.0.
 */

import * as core from "@actions/core";
import * as github from "@actions/github";
import { minimatch } from "minimatch";
import { pathToFileURL } from "node:url";

const MERGE_METHODS = new Set(["merge", "squash", "rebase"]);

export function lines(value) {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function evaluatePullRequest(pullRequest, files, checks, allowedAuthors, allowedFiles) {
  if (pullRequest.state !== "open") {
    return { eligible: false, reason: "pull-request-not-open" };
  }

  if (!allowedAuthors.includes(pullRequest.user.login)) {
    return { eligible: false, reason: "author-not-allowed" };
  }

  const disallowedFiles = files
    .map((file) => file.filename)
    .filter(
      (filename) => !allowedFiles.some((pattern) => minimatch(filename, pattern))
    );
  if (disallowedFiles.length > 0) {
    return { eligible: false, reason: "files-not-allowed", disallowedFiles };
  }

  const incompleteChecks = checks.filter(
    (check) =>
      check.status !== "completed" ||
      !["success", "neutral"].includes(check.conclusion)
  );
  if (incompleteChecks.length > 0) {
    return { eligible: false, reason: "checks-not-successful", incompleteChecks };
  }

  return { eligible: true, reason: "eligible" };
}

export async function inspectAndMerge({
  octokit,
  owner,
  repo,
  pullRequestNumber,
  allowedAuthors,
  allowedFiles,
  mergeMethod,
}) {
  if (!MERGE_METHODS.has(mergeMethod)) {
    throw new Error(
      `Invalid merge-type '${mergeMethod}'. Expected merge, squash, or rebase.`
    );
  }

  const { data: pullRequest } = await octokit.rest.pulls.get({
    owner,
    repo,
    pull_number: pullRequestNumber,
  });
  const files = await octokit.paginate(octokit.rest.pulls.listFiles, {
    owner,
    repo,
    pull_number: pullRequestNumber,
    per_page: 100,
  });
  const checks = await octokit.paginate(octokit.rest.checks.listForRef, {
    owner,
    repo,
    ref: pullRequest.head.sha,
    per_page: 100,
  });

  const evaluation = evaluatePullRequest(
    pullRequest,
    files,
    checks,
    allowedAuthors,
    allowedFiles
  );
  if (!evaluation.eligible) {
    return { ...evaluation, merged: false };
  }

  const { data: merge } = await octokit.rest.pulls.merge({
    owner,
    repo,
    pull_number: pullRequestNumber,
    merge_method: mergeMethod,
    sha: pullRequest.head.sha,
  });

  if (!merge.merged) {
    throw new Error(merge.message || "GitHub declined to merge the pull request.");
  }

  await octokit.rest.issues.createComment({
    owner,
    repo,
    issue_number: pullRequestNumber,
    body: `This pull request was automatically merged because author '${pullRequest.user.login}' and all changed files satisfied the configured automatic-merge policy after all checks completed successfully.`,
  });

  return {
    merged: true,
    reason: "merged",
    mergeCommitSha: merge.sha || "",
  };
}

export async function run() {
  try {
    const token = core.getInput("token", { required: true });
    const pullRequestNumber = Number.parseInt(
      core.getInput("pull-request-number", { required: true }),
      10
    );
    if (!Number.isSafeInteger(pullRequestNumber) || pullRequestNumber < 1) {
      throw new Error("pull-request-number must be a positive integer.");
    }

    const allowedAuthors = lines(core.getInput("allowed-authors", { required: true }));
    const allowedFiles = lines(core.getInput("allowed-files", { required: true }));
    const mergeMethod = core.getInput("merge-type") || "squash";
    const { owner, repo } = github.context.repo;
    const octokit = github.getOctokit(token);

    const result = await inspectAndMerge({
      octokit,
      owner,
      repo,
      pullRequestNumber,
      allowedAuthors,
      allowedFiles,
      mergeMethod,
    });

    core.setOutput("merged", String(result.merged));
    core.setOutput("reason", result.reason);
    core.setOutput("merge-commit-sha", result.mergeCommitSha || "");

    if (result.reason === "files-not-allowed") {
      core.info(`Files outside the policy: ${result.disallowedFiles.join(", ")}`);
    } else if (result.reason === "checks-not-successful") {
      core.info(
        `Checks not successful: ${result.incompleteChecks
          .map((check) => check.name)
          .join(", ")}`
      );
    } else if (!result.merged) {
      core.info(`Pull request was not merged: ${result.reason}.`);
    } else {
      core.info(`Pull request #${pullRequestNumber} was merged.`);
    }
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  run();
}
