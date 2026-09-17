# Find triggering pull request

Returns the first pull request associated with the `workflow_run` that invoked the
calling workflow. The `pr-number` output is empty when the workflow run is not
associated with a pull request.

```yaml
- id: find-pr
  uses: opensearch-project/opensearch-build/.github/actions/find-triggering-pr@<commit-sha>
  with:
    token: ${{ github.token }}
```

This action is derived from
[`peternied/find-triggering-pr`](https://github.com/peternied/find-triggering-pr),
which is licensed under the Apache License 2.0.
