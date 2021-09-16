- [OpenSearch Bundle Workflow](#opensearch-bundle-workflow)
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

## OpenSearch Bundle Workflow

The bundle workflow builds a complete OpenSearch distribution from source. You can currently build 1.0, 1.1 and 1.1-SNAPSHOT.

### Build from Source

Each build requires a manifest to be passed as input. We currently have the following input manifests.

| name                                                                  | description                                                   |
|-----------------------------------------------------------------------|---------------------------------------------------------------|
| [opensearch-1.0.0.yml](/manifests/opensearch-1.0.0.yml)               | Manifest to reproduce 1.0.0 build.                            |
| [opensearch-1.0.0-maven.yml](/manifests/opensearch-1.0.0-maven.yml)   | One-time manifest to build maven artifacts for 1.0 from tags. |
| [opensearch-1.1.0.yml](/manifests/opensearch-1.1.0.yml)               | Manifest to build upcoming 1.x release.                       |

The following example builds a shapshot version of OpenSearch 1.1.0.

```bash
./bundle-workflow/build.sh manifests/opensearch-1.1.0.yml --snapshot
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

The following example kicks off all test suites for a distribution of OpenSearch 1.1.0.

```bash
./bundle-workflow/test.sh manifests/opensearch-1.1.0.yml
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --component [name] | Test a single component by name, e.g. `--component common-utils`.       |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

#### Integration Tests

This step runs integration tests invoking `integtest.sh` in each component from bundle manifest.

To run integration tests locally, use below command. It pulls down the built bundle and its manifest file from S3, reads all components of the bundle and runs integration tests against each component.
 
```
export AWS_ROLE_ARN=arn:aws:iam::<AWS_JENKINS_ACCOUNT>:role/opensearch-test
export AWS_ROLE_SESSION_NAME=dummy-session

Next, configure temporary credentials in environment w/
export AWS_SESSION_TOKEN=<value>
export AWS_ACCESS_KEY_ID=<value>
export AWS_SECRET_ACCESS_KEY=<value>

cd bundle-workflow
./test.sh integ-test --test-run-id <execution-id> --s3-bucket <bucket_name> --opensearch-version <version> --build-id <id> --architecture <arch>
```
#### Backwards Compatibility Tests

This step run backward compatibility invoking `bwctest.sh` in each component from bundle manifest.

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
./bundle-workflow/ci.sh manifests/opensearch-1.1.0.yml --snapshot
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --component [name] | Test a single component by name, e.g. `--component common-utils`.       |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

### Auto-Generate Manifests

The [manifests workflow](src/manifests) reacts to version increments in OpenSearch and its components by extracting Gradle properties from project branches. When a new version is identified, it creates a new input manifest in [manifests](../manifests) and [opens a pull request](../.github/workflows/manifests.yml).

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
