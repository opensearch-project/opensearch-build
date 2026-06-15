# Start OpenSearch

Composite GitHub Action for downloading a snapshot OpenSearch distribution, optionally installing plugins, starting OpenSearch on the runner, and verifying the node is reachable.

Consumers should pin this action to `@main`. The `opensearch-build` repository has branch rulesets that require pull request reviews before merging, making `@main` safe to use:

```yaml
- name: Start OpenSearch
  uses: opensearch-project/opensearch-build/.github/actions/start-opensearch@main
  with:
    opensearch-version: 3.8.0
    plugins: "file:${{ github.workspace }}/build/distributions/opensearch-security.zip"
    security-enabled: true
    admin-password: ${{ steps.generate-password.outputs.password }}
```
