# Set Up OpenSearch Dashboards

Composite GitHub Action for checking out OpenSearch Dashboards, checking out a Dashboards plugin into the plugin directory, configuring Node.js and Yarn, bootstrapping OpenSearch Dashboards, and optionally building and installing the plugin into a downloaded OpenSearch Dashboards distribution.

Consumers should pin this action to a full `opensearch-build` commit SHA:

```yaml
- name: Set up OpenSearch Dashboards
  uses: opensearch-project/opensearch-build/.github/actions/setup-opensearch-dashboards@<opensearch-build-commit-sha>
  with:
    plugin_name: security-dashboards-plugin
    opensearch_dashboards_yml: opensearch_dashboards.yml
```

For binary install testing, set `install_zip` and provide the built plugin naming inputs:

```yaml
- name: Set up OpenSearch Dashboards
  uses: opensearch-project/opensearch-build/.github/actions/setup-opensearch-dashboards@<opensearch-build-commit-sha>
  with:
    plugin_name: security-dashboards-plugin
    built_plugin_name: securityDashboards
    install_zip: true
    snapshot: true
    opensearch_dashboards_yml: opensearch_dashboards.yml
```

Set `snapshot: false` to download the OpenSearch Dashboards artifact from `ci.opensearch.org` release artifacts instead of `artifacts.opensearch.org` snapshots.

To check out a plugin from a different repository or branch, provide `plugin_repo` and/or `plugin_branch`:

```yaml
- name: Set up OpenSearch Dashboards
  uses: opensearch-project/opensearch-build/.github/actions/setup-opensearch-dashboards@<opensearch-build-commit-sha>
  with:
    plugin_name: security-dashboards-plugin
    plugin_repo: opensearch-project/security-dashboards-plugin
    plugin_branch: main
```
