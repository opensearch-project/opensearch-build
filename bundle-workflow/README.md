- [OpenSearch Bundle Workflow](#opensearch-bundle-workflow)
  - [How it works](#how-it-works)
  - [Build from Source](#build-from-source)
    - [Custom Build Scripts](#custom-build-scripts)
  - [Assemble the Bundle](#assemble-the-bundle)
    - [Custom Install Scripts](#custom-install-scripts)
  - [Sign Artifacts](#sign-artifacts)
  - [Test the Bundle](#test-the-bundle)
    - [Integration Tests](#integration-tests)
    - [Backwards Compatibility Tests](#backwards-compatibility-tests)
    - [Performance Tests](#performance-tests)
  - [Sanity Check the Bundle](#sanity-check-the-bundle)
  - [Auto-Generate Manifests](#auto-generate-manifests)
  - [Component Onboarding](#component-onboarding)

## OpenSearch Bundle Workflow

The bundle workflow builds a complete OpenSearch distribution from source. You can currently build 1.0, 1.1 and 1.1-SNAPSHOT.

### How it works

This system performs a top-down build of all components required for a specific OpenSearch bundle release. 
The input to the system is a manifest that defines the order in which components should be built. 
All manifests for our current releases are [here](/manifests).
 
To build components we rely on a common entry-point in the form of a `build.sh` script. See [Custom Build Scripts](#custom-build-scripts).
Within each build script components have the option to place artifacts in a set of directories to be picked up and published on their behalf.  These are

| name               | description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| /maven        | Include any publications that should be pushed to maven                                                 |
| /plugins      | Where a plugin zip should be placed. If included it will be installed during bundle assembly.           |
| /core-plugins | Where plugins shipped from `https://github.com/opensearch-project/OpenSearch` should be placed          |
| /bundle       | Where the min bundle should be placed when built from `https://github.com/opensearch-project/OpenSearch`|
| /libs         | Where any additional libs should be placed that are required during bundle assembly                     |

The build order allows us to first publish `OpenSearch` followed by `common-utils` and publish these artifacts to maven local so that
they are available for each component.  In order to ensure that the same versions are used, a `-Dopensearch.version` flag is passed to
each component's build script that defines which version the component should build against.

### Build from Source

Each build requires a manifest to be passed as input. We currently have the following input manifests.

| name                                                                        | description                                                   |
|-----------------------------------------------------------------------------|---------------------------------------------------------------|
| [opensearch-1.0.0.yml](/manifests/1.0.0/opensearch-1.0.0.yml)               | Manifest to reproduce 1.0.0 build.                            |
| [opensearch-1.0.0-maven.yml](/manifests/1.0.0/opensearch-1.0.0-maven.yml)   | One-time manifest to build maven artifacts for 1.0 from tags. |
| [opensearch-1.1.0.yml](/manifests/1.1.0/opensearch-1.1.0.yml)               | Manifest for 1.1.0, the next version.                         |
| [opensearch-1.2.0.yml](/manifests/1.2.0/opensearch-1.2.0.yml)               | Manifest for 1.2.0, the following version.                    |
| [opensearch-2.0.0.yml](/manifests/2.0.0/opensearch-2.0.0.yml)               | Manifest for 2.0.0, the next major version of OpenSearch.     |

The following example builds a shapshot version of OpenSearch 1.1.0.

```bash
./bundle-workflow/build.sh manifests/1.1.0/opensearch-1.1.0.yml --snapshot
```

The [OpenSearch repo](https://github.com/opensearch-project/OpenSearch) is built first, followed by [common-utils](https://github.com/opensearch-project/common-utils), and all declared plugin repositories. These dependencies are published to maven local under `~/.m2`, and subsequent project builds pick those up. All final output is placed into an `artifacts` folder along with a build output `manifest.yml` that contains output details.

Artifacts will contain the following folders.

```
/artifacts
  bundle/ <- contains opensearch min tarball 
  maven/ <- all built maven artifacts
  plugins/ <- all built plugin zips
  core-plugins/ <- all built core plugins zip
  manifest.yml <- build manifest describing all built components and their artifacts
```

The following options are available in `bundle-workflow/build.sh`.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --snapshot         | Build a snapshot instead of a release artifact, default is `false`.     |
| --component [name] | Rebuild a single component by name, e.g. `--component common-utils`.    |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

#### Custom Build Scripts

Each component build relies on a `build.sh` script that is used to prepare bundle artifacts for a particular bundle version that takes two arguments: version and target architecture. By default the tool will look for a script in [scripts/components](scripts/components), then in the checked-out repository in `build/build.sh`, then default to a Gradle build implemented in [scripts/default/build.sh](scripts/default/build.sh).

### Assemble the Bundle 

```bash
./bundle-workflow/assemble.sh artifacts/manifest.yml
```

The bundling step takes output from the build step, installs plugins, and assembles a full bundle into a `bundle` folder. The input requires a path to the build manifest and is expected to be inside the `artifacts` directory that contains `bundle`, `maven`, `plugins` and `core-plugins` subdirectories from the build step.

Artifacts will be updated as follows.

```
/bundle
  <file-name>.tar.gz <- assembled tarball
  manifest.yml <- bundle manifest describing versions for the min bundle and all installed plugins and their locations
```

#### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/bundle-build/components](scripts/bundle-build/components), then default to a noop version implemented in [scripts/default/install.sh](scripts/default/install.sh).

### Sign Artifacts

The signing step (optional) takes the manifest file created from the build step and signs all its component artifacts using a tool called `opensearch-signer-client` (in progress of being open-sourced). The input requires a path to the build manifest and is expected to be inside the artifacts directory with the same directories mentioned in the build step. 

The following options are available. 

| name          | description                                                                           |
|---------------|---------------------------------------------------------------------------------------|
| --component   | The component name of the component whose artifacts will be signed.                   |
| --type        | The artifact type to be signed. Currently one of 3 options: [plugins, maven, bundle]. |
| -v, --verbose | Show more verbose output.                                                             |

The signed artifacts (<artifact>.asc) will be found in the same location as the original artifact. 

The following command signs all artifacts.

```bash
./bundle_workflow/sign.sh artifacts/manifest.yml
```

### Test the Bundle

Tests the OpenSearch bundle.

This workflow contains integration, backwards compatibility and performance tests.

Usage:
```bash
export AWS_ROLE_ARN=arn:aws:iam::<AWS_JENKINS_ACCOUNT>:role/opensearch-test
export AWS_ROLE_SESSION_NAME=dummy-session

export AWS_SESSION_TOKEN=<value>
export AWS_ACCESS_KEY_ID=<value>
export AWS_SECRET_ACCESS_KEY=<value>
./bundle-workflow/test.sh <test-type>
```

The following options are available.

| name                 | description                                                             |
|----------------------|-------------------------------------------------------------------------|
| test-type            | Run tests of a test suite. [integ-test, bwc-test]                       |
| --test-run-id        | Unique identifier for a test run                                        |
| --s3-bucket          | Artifact S3 bucket to pull manifests and dependencies                   |
| --opensearch-version | OpenSearch version                                                      |
| --build-id           | Unique identifier for a build                                           |
| --architecture       | CPU architecture for all components                                     |
| --component          | Test a specific component in a manifest                                 |
| --keep               | Do not delete the temporary working directory on both success or error. |
| -v, --verbose        | Show more verbose output.                                               |

#### Integration Tests

This step runs integration tests invoking `run_integ_test.py` in each component from bundle manifest.

To run integration tests locally, use below command. It pulls down the built bundle and its manifest file from S3, reads all components of the bundle and runs integration tests against each component.
 
Usage:
```bash
cd bundle-workflow
./test.sh integ-test --test-run-id <execution-id> --s3-bucket <bucket_name> --opensearch-version <version> --build-id <id> --architecture <arch>
```
#### Backwards Compatibility Tests

This step run backward compatibility invoking `run_bwc_test.py` in each component from bundle manifest.

Usage:
```bash
cd bundle-workflow
./test.sh bwc-test --test-run-id <execution-id> --s3-bucket <bucket_name> --opensearch-version <version> --build-id <id> --architecture <arch>
```

#### Performance Tests

TODO

### Sanity Check the Bundle

This workflow runs sanity checks on every component present in the bundle, executed as part of the [manifests workflow](/.github/workflows/manifests.yml) in this repostiory. It ensures that the component GitHub repositories are correct and versions in those components match the OpenSearch version.

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

The following checks are available.

| name                                          | description                                                   |
|-----------------------------------------------|---------------------------------------------------------------|
| gradle:properties:version                     | Check version of the component.                               |
| gradle:dependencies:opensearch.version        | Check dependency on the correct version of OpenSearch.        |
| gradle:publish                                | Check that publishing to Maven local works, and publish.      |

The following example sanity-checks components in the the OpenSearch 1.1.0 manifest.

```bash
./bundle-workflow/ci.sh manifests/1.1.0/opensearch-1.1.0.yml --snapshot
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --component [name] | Test a single component by name, e.g. `--component common-utils`.       |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

### Auto-Generate Manifests

The [manifests workflow](src/manifests) reacts to version increments in OpenSearch and its components by extracting Gradle properties from project branches. Currently OpenSearch `main`, and `x.y` branches are checked out one-by-one, published to local maven, and their versions extracted using `./gradlew properties`. When a new version is found, a new input manifest is added to [manifests](../manifests), and [a pull request is opened](../.github/workflows/manifests.yml) (e.g. [opensearch-build#491](https://github.com/opensearch-project/opensearch-build/pull/491)).

Show information about existing manifests. 

```bash
./bundle-workflow/manifests.sh list
```

Check for updates and create any new manifests. 

```bash
./bundle-workflow/manifests.sh update
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

### Component Onboarding

With many components included in the distribution each component bears responsibility to keep the release process streamlined and react to integration issues.

1. Components repositories have a label matching the manifest versions so incoming issues can be appropriately labeled, e.g. Add `v1.1.0` to https://github.com/opensearch-project/opensearch-build/labels.

1. Ensure your repository branches have continuous integration checks enabled and passing, e.g [job-scheduler workflow](https://github.com/opensearch-project/job-scheduler/blob/main/.github/workflows/test-and-build-workflow.yml).

1. Create a `scripts/build.sh` if you have specific requirements that are not covered by the [default build.sh script](/scripts/default/build.sh) and commit it to your repository.

1. Ensure your `build.sh` reads and passes along both `-Dbuild.snapshot=` and `-Dopensearch.version=` flags.  Snapshot builds should produce a -SNAPSHOT named artifact for example `opensearch-plugin-1.1.0.0-SNAPSHOT.zip` where a release build of the same component would produce `opensearch-plugin-1.1.0.0.zip`.
  1. It is recommended that unit tests without network traffic are run to ensure a baseline quality level.

1. Execute `./bundle-workflow/build.sh` to ensure your component builds and all artifacts are correctly placed into ./artifacts/ with correct output names.

1. Execute `./bundle-workflow/assemble.sh` to ensure the full bundle is assembled and placed in to /bundles/*.tar.gz.  Unpack the tarball to ensure all your components are placed in their correct locations.

1. Update a [manifest](/manifests) for a particular release to include your plugin.  For example to be included in the 1.1.0 release, you would update [opensearch-1.1.0.yml](/manifests/1.1.0/opensearch-1.1.0.yml). We require your plugin name, repository url, and git ref that should be used. For unreleased versions this should be a branch in your repository.  Once a release is cut, these refs will be updated to build from a tag or specific commit hash.

1. Publish a PR to this repo including the updated manifest and the names of the artifacts being added.