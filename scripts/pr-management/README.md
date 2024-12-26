# PR Management Scripts

This folder contains scripts for automating tasks related to pull requests.

## BackportPRs.py

This script handles backport PRs by:
- Detecting and resolving conflicts in `CHANGELOG.md`.
- Combining old and new changes during conflict resolution.
- Committing the resolved file back to the PR branch.

## StalledPRs.py

This script handles Stalled PRs by:
- Fetching all the stalled PRs using the Stalled label
- Rebase the PRs onto the latest target branch and push updates