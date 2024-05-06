- [Auto-Generating Manifests](#auto-generating-manifests)

## Auto-Generating Manifests

This workflow reacts to version increments in OpenSearch and its components by extracting Gradle properties from project branches. Currently OpenSearch `main`, and `x.y` branches are checked out one-by-one, published to local maven, and their versions extracted using `./gradlew properties`. When a new version is found, a new input manifest is added to [manifests](../../manifests), and [a pull request is opened](../../.github/workflows/manifests.yml) (e.g. [opensearch-build#491](https://github.com/opensearch-project/opensearch-build/pull/491)).

### Show information about existing manifests

```bash
./manifests.sh list
```

### Check for updates and create any new manifests
* If there are no existing manifests in either the `manifests` or `legacy-manifests` folder, use the manifest templates located in `manifests/templates` as a base to generate new manifests.
* If the requested new manifest version (e.g., 0.10.1) is lower than the lowest existing manifest version (e.g., 1.0.0), again, use the manifest templates located in `manifests/templates` as a base to generate new manifests.
* In other scenarios, always use the latest existing manifest version that is lower than the requested new manifest version as the base to generate new manifests (e.g., Use 2.12.0 to generate 2.12.1, even if 2.13.0 exists).

```bash
./manifests.sh update
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --keep             | Do not delete the temporary working directory on both success or error. |
| --type             | Only list manifests of a specific type).                                |
| -v, --verbose      | Show more verbose output.                                               |
