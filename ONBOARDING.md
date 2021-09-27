## Component Onboarding

This document describes steps to onboard a new plugin to release workflow for continuous integration and testing.

### Step 1: Onboard to `build-workflow`

1. Update a [manifest](/manifests) for a particular release to include your plugin.  For example to be included in the 1.1.0 release, you would update [opensearch-1.1.0.yml](/manifests/1.1.0/opensearch-1.1.0.yml). We require your plugin name, repository url, and git ref that should be used. For unreleased versions this should be a branch in your repository.  Once a release is cut, these refs will be updated to build from a tag or specific commit hash.

2. Create a `scripts/build.sh` if you have specific requirements that are not covered by the [default build.sh script](/scripts/default/build.sh) and commit it to your repository.

3. Ensure your `build.sh` reads and passes along both `-Dbuild.snapshot=` and `-Dopensearch.version=` flags.  Snapshot builds should produce a -SNAPSHOT tagged artifact for example `opensearch-plugin-1.1.0.0-SNAPSHOT.zip` where a release build of the same component would produce `opensearch-plugin-1.1.0.0.zip`.

4. Execute `./bundle-workflow/build.sh` to ensure your component builds and all artifacts are correctly placed into ./artifacts/ with correct output names.

5. Execute `./bundle-workflow/assemble.sh` to ensure the full bundle is assembled and placed in to /bundles/*.tar.gz.  Unpack the tarball to ensure all your components are placed in their correct locations.

6. Publish a PR to this repo including the updated manifest and the names of the artifacts being added.

### Step 2: Onboard to `test-workflow`

1. Update the test configuration file, [test_manifest.yml](https://github.com/opensearch-project/opensearch-build/blob/main/bundle-workflow/src/test_workflow/config/test_manifest.yml), for a particular release, to include your plugin. This test configuration defines full suite of tests - `integ`, `bwc`, that can be run on the plugin.

2. For integration testing, the `test-workflow` runs integration tests available in the plugin repository. You will need to add `integ-test` config for your plugin in test_manifest.yml, [example](https://github.com/opensearch-project/opensearch-build/blob/85bbe204e947d5d1579af771bbafe399c11cbd70/bundle-workflow/src/test_workflow/config/test_manifest.yml#L3).
    1. It supports two test configs - `with-security` and `without-security`, which runs test with security plugin enabled and disabled respectively. Choose one or both depending on what your plugin integration tests support.
    2. If your plugin is dependent on `job-scheduler` zip, you can define that in `build-dependencies` in the config. Currently, the test workflow only supports `job-scheduler` as build dependency. Please create an issue if your plugin needs more support.

3. For backward compatibility testing, the `test-workflow` runs backward compatibility tests available in the plugin repository, (see [reference]((https://github.com/opensearch-project/anomaly-detection/blob/d9a122d05282f7efc1e24c61d64f18dec0fd47af/build.gradle#L428))). Like integration test, it has a set of configurable options defined in test_manifest.yml, [example](https://github.com/opensearch-project/opensearch-build/blob/85bbe204e947d5d1579af771bbafe399c11cbd70/bundle-workflow/src/test_workflow/config/test_manifest.yml#L8).
