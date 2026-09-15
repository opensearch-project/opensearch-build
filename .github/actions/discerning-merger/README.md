# Discerning merger

Merges a pull request only when:

- its author is listed in `allowed-authors`;
- every changed file matches at least one `allowed-files` glob; and
- every check run on the pull request head has completed with `success` or
  `neutral`.

Repository rules and branch protections continue to apply. The calling workflow
must provide a token with `checks: read`, `contents: write`, and
`pull-requests: write` permissions. The action does not create or retrieve a
GitHub App token.

```yaml
- id: merge
  uses: opensearch-project/opensearch-build/.github/actions/discerning-merger@<commit-sha>
  with:
    token: ${{ github.token }}
    pull-request-number: ${{ steps.find-pr.outputs.pr-number }}
    allowed-authors: |
      dependabot[bot]
      opensearch-ci-bot
    allowed-files: |
      manifests/*/*.yml
```

The action sets `merged`, `reason`, and `merge-commit-sha` outputs. A skipped
merge is a successful action invocation with `merged` set to `false`; unexpected
API and configuration errors fail the action.

This action is derived from
[`peternied/discerning-merger`](https://github.com/peternied/discerning-merger),
which is licensed under the Apache License 2.0.
