- [Sanity Testing the Distribution](#sanity-testing-the-distribution)
  - [Manifest Checks](#manifest-checks)
  - [Ci.sh Options](#cish-options)

## Sanity Testing the Distribution

This workflow runs sanity checks on every component present in the bundle, executed as part of the [manifests workflow](../../.github/workflows/manifests.yml) in this repository. It ensures that the component GitHub repositories are correct and versions in those components match the OpenSearch or OpenSearch Dashboards versions.

To use checks, nest them under `checks` in the manifest.

```yaml
- name: common-utils
  repository: https://github.com/opensearch-project/common-utils.git
  ref: main
  checks:
    - gradle:publish
    - gradle:properties:version
    - gradle:dependencies:opensearch.version
    - gradle:dependencies:opensearch.version: alerting
```

### Manifest Checks

The following checks are available.

| name                                          | description                                                                       |
|-----------------------------------------------|-----------------------------------------------------------------------------------|
| gradle:properties:version                     | Check version of the component.                                                   |
| gradle:dependencies:opensearch.version        | Check dependency on the correct version of OpenSearch in gradle properties.       |
| gradle:publish                                | Check that publishing to Maven local works, and publish.                          |
| npm:package:version                           | Check dependency on the correct version of OpenSearch Dashboards in package.json. |

The following example sanity-checks components in the the OpenSearch 1.2.0 manifest.

```bash
./ci.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot
```

### Ci.sh Options

The following options are available.

| name                    | description                                                                         |
|-------------------------|-------------------------------------------------------------------------------------|
| --component [name ...]  | Test a subset of components by name, e.g. `--component common-utils job-scheduler`. |
| --keep                  | Do not delete the temporary working directory on both success or error.             |
| -v, --verbose           | Show more verbose output.                                                           |
