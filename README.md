<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

[![python](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml)
[![groovy](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml)
[![manifests](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml)
[![codecov](https://codecov.io/gh/opensearch-project/opensearch-build/branch/main/graph/badge.svg?token=03S5XZ80UI)](https://codecov.io/gh/opensearch-project/opensearch-build)

- [Releasing OpenSearch](#releasing-opensearch)
  - [Creating a New Version](#creating-a-new-version)
  - [Onboarding a New Plugin](#onboarding-a-new-plugin)
  - [Building and Testing an OpenSearch Distribution](#building-and-testing-an-opensearch-distribution)
    - [How it works](#how-it-works)
      - [OpenSearch](#opensearch)
      - [OpenSearch Dashboards](#opensearch-dashboards)
    - [CI CD Environment](#ci-cd-environment)
      - [Build CI Runner Docker Image from Dockerfile](#build-ci-runner-docker-image-from-dockerfile)
    - [Check Out Source](#check-out-source)
    - [Build from Source](#build-from-source)
      - [Custom Build Scripts](#custom-build-scripts)
      - [Avoiding Rebuilds](#avoiding-rebuilds)
      - [Patch Releases](#patch-releases)
    - [Assemble the Bundle](#assemble-the-bundle)
      - [Cross-Platform Builds](#cross-platform-builds)
      - [Custom Install Scripts](#custom-install-scripts)
    - [Sign Artifacts](#sign-artifacts)
    - [Test the Bundle](#test-the-bundle)
      - [Integration Tests](#integration-tests)
      - [Backwards Compatibility Tests](#backwards-compatibility-tests)
      - [Performance Tests](#performance-tests)
    - [Sanity Check the Bundle](#sanity-check-the-bundle)
    - [Auto-Generate Manifests](#auto-generate-manifests)
  - [Making a Release](#making-a-release)
    - [Releasing for Linux](#releasing-for-linux)
    - [Releasing for FreeBSD](#releasing-for-freebsd)
    - [Releasing for Windows](#releasing-for-windows)
    - [Releasing for MacOS](#releasing-for-macos)
  - [Deploying Infrastructure](#deploying-infrastructure)
- [Contributing](#contributing)
- [Getting Help](#getting-help)
- [Code of Conduct](#code-of-conduct)
- [Security](#security)
- [License](#license)
- [Copyright](#copyright)

## Releasing OpenSearch

### Creating a New Version

OpenSearch and OpenSearch Dashboards are distributed as bundles that include both core engines and plugins. Each new OpenSearch release process starts when any one component increments a version, typically on the `main` branch. For example, [OpenSearch#1192](https://github.com/opensearch-project/OpenSearch/pull/1192) incremented the version to 2.0. The [manifest automation workflow](.github/workflows/manifests.yml) will notice this change, and make a pull request (e.g. [opensearch-build#514](https://github.com/opensearch-project/opensearch-build/pull/514)) that adds a new manifest (e.g. [opensearch-2.0.0.yml](manifests/2.0.0/opensearch-2.0.0.yml). After that's merged, a GitHub issue is automatically opened by [this workflow](.github/workflows/releases.yml) to make a new release using [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#566](https://github.com/opensearch-project/opensearch-build/issues/566)). Existing and new components [(re)onboard into every release](ONBOARDING.md) by submitting pull requests to each version's manifest.

### Onboarding a New Plugin

Plugin owners can follow the [Onboarding Process](ONBOARDING.md) to onboard their plugins to the release process. 

### Building and Testing an OpenSearch Distribution

The bundle workflow builds a complete OpenSearch and OpenSearch Dashboards distribution from source. You can currently build 1.0, 1.1, 1.1-SNAPSHOT and 1.2 versions.

#### How it works

This system performs a top-down build of all components required for a specific OpenSearch and OpenSearch Dashboards bundle release. The input to the system is a manifest that defines the order in which components should be built. 
All manifests for our current releases are [here](manifests).
 
To build components we rely on a common entry-point in the form of a `build.sh` script. See [Custom Build Scripts](#custom-build-scripts).

Within each build script components have the option to place artifacts in a set of directories to be picked up and published on their behalf. These are as follows.

| name               | description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| /maven        | Include any publications that should be pushed to maven                                                 |
| /plugins      | Where a plugin zip should be placed. If included it will be installed during bundle assembly.           |
| /core-plugins | Where plugins shipped from `https://github.com/opensearch-project/OpenSearch` should be placed          |
| /bundle       | Where the min bundle should be placed when built from `https://github.com/opensearch-project/OpenSearch`|
| /libs         | Where any additional libs should be placed that are required during bundle assembly                     |

##### OpenSearch

The build order first publishes `OpenSearch` followed by `common-utils`, and publishes these artifacts to maven local so that they are available for each component. In order to ensure that the same versions are used, a `-Dopensearch.version` flag is provided to each component's build script that defines which version the component should build against.

##### OpenSearch Dashboards

The build order first pulls down `OpenSearch-Dashboards` and then utilizes it to build other components. Currently, building plugins requires having the core repository built first to bootstrap and build the modules utilized by plugins.

#### CI CD Environment

We build, assemble, and test our artifacts on docker containers. All of our pipelines are using the same docker image for consistency. We provide docker files in [docker/ci](docker/ci) folder, and images on [staging docker hub repositories](https://hub.docker.com/r/opensearchstaging/ci-runner/).

##### Build CI Runner Docker Image from Dockerfile

* If you only want to build the docker image for either x64 or arm64, run this on a x64 or arm64 host respectively:
  ```
  docker build -f ./docker/ci/dockerfiles/integtest-runner.al2.dockerfile . -t <Docker Hub RepoName>/<Docker Image Name>:<Tag Name>
  ```

* If you want to build multi-arch docker image for both x64 and arm64, make sure you are using Docker Desktop:
  * Run these commands to setup the multi-arch builder, you can re-use this build later on, just need to re-bootstrap again if you restart Docker Desktop:
    ```
    docker buildx create --name multiarch
    docker buildx use multiarch
    docker buildx inspect --bootstrap
    ```

  * You should be able to see similar output in `docker ps` like this:
    ```
    123456789012 moby/buildkit:buildx-stable-1 "buildkitd" 11 minutes ago Up 11 minutes buildx_buildkit_multiarch0
    ```

  * Docker buildx is using a container to build multi-arch images and combine all the layers together, so you can only upload it to Docker Hub,
    or save it locally as cache, means `docker images` will not show the image due to your host cannot have more than one CPU architecture.

  * Run these commands to actually build the docker image in multi-arch and push to Docker Hub (est. 1hr time depend on your host hardware specifications and network bandwidth):
    ```
    docker buildx build --platform linux/amd64,linux/arm64 -t <Docker Hub RepoName>/<Docker Image Name>:<Tag Name> -f <Docker File Path> --push .
    ```

#### Check Out Source

The [checkout workflow](src/checkout_workflow) checks out source code for a given manifest for further examination.

```bash
./checkout.sh manfiests/1.2.0/opensearch-1.2.0.yml
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| -v, --verbose      | Show more verbose output.                                               |


#### Build from Source

Each build requires a manifest to be passed as input. We currently have the following input manifests.

| name                                                                                 | description                                                    |
|--------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [opensearch-1.0.0.yml](/manifests/1.0.0/opensearch-1.0.0.yml)                        | Manifest to reproduce 1.0.0 build.                             |
| [opensearch-1.0.0-maven.yml](/manifests/1.0.0/opensearch-1.0.0-maven.yml)            | One-time manifest to build maven artifacts for 1.0 from tags.  |
| [opensearch-1.1.0.yml](/manifests/1.1.0/opensearch-1.1.0.yml)                        | Manifest for 1.1.0, the current version.                       |
| [opensearch-1.1.1.yml](/manifests/1.1.1/opensearch-1.1.1.yml)                        | Manifest for 1.1.1, a patch release.                           |
| [opensearch-1.2.0.yml](/manifests/1.2.0/opensearch-1.2.0.yml)                        | Manifest for 1.2.0, the next version.                          |
| [opensearch-2.0.0.yml](/manifests/2.0.0/opensearch-2.0.0.yml)                        | Manifest for 2.0.0, the next major version of OpenSearch.      |
| [opensearch-dashboards-1.1.0.yml](/manifests/1.1.0/opensearch-dashboards-1.1.0.yml)  | Manifest for 1.1.0, the next version of OpenSearch Dashboards. |    

The following example builds a snapshot version of OpenSearch 1.2.0.

```bash
./build.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot
```

While the following builds a snapshot version of OpenSearch-Dashboards 1.2.0.

```bash
./build.sh manifests/1.2.0/opensearch-dashboards-1.2.0.yml --snapshot
```

The [OpenSearch repo](https://github.com/opensearch-project/OpenSearch) is built first, followed by [common-utils](https://github.com/opensearch-project/common-utils), and all declared plugin repositories. These dependencies are published to maven local under `~/.m2`, and subsequent project builds pick those up. 

The [OpenSearch Dashboards repo](https://github.com/opensearch-project/OpenSearch-Dashboards) is built first, followed by all declared plugin repositories. 

All final output is placed into an `builds` folder along with a build output `manifest.yml` that contains output details.

Artifacts will contain the following folders.

```
/builds
  dist/ <- contains opensearch or opensearch-dashboards min tarball 
  maven/ <- all built maven artifacts
  plugins/ <- all built plugin zips
  core-plugins/ <- all built core plugins zip
  manifest.yml <- build manifest describing all built components and their artifacts
```

The following options are available in `build.sh`.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --snapshot         | Build a snapshot instead of a release artifact, default is `false`.     |
| --component [name] | Rebuild a single component by name, e.g. `--component common-utils`.    |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -l, --lock         | Generate a stable reference manifest.                                   |
| -v, --verbose      | Show more verbose output.                                               |

##### Custom Build Scripts

Each component build relies on a `build.sh` script that is used to prepare bundle artifacts for a particular bundle version that takes two arguments: version and target architecture. By default the tool will look for a script in [scripts/components](scripts/components), then in the checked-out repository in `build/build.sh`, then default to a Gradle build implemented in [scripts/default/build.sh](scripts/default/build.sh).

##### Avoiding Rebuilds

Builds can automatically generate a `manifest.lock` file with stable git references (commit IDs) and build options (platform, architecture and snapshot) by specifying `--lock`. The output can then be reused as input manifest after checking against a collection of prior builds.

```bash
MANIFEST=manifests/1.2.0/opensearch-1.2.0.yml
SHAS=shas

./build.sh --lock $MANIFEST # generates opensearch-1.2.0.yml.lock

MANIFEST_SHA=$(sha1sum $MANIFEST.lock | cut -f1 -d' ') # generate a checksum of the stable manifest

if test -f "$SHAS/$MANIFEST_SHA.lock"; then
  echo "Skipping $MANIFEST_SHA"
else
  ./build.sh $MANIFEST.lock # rebuild using stable references in .lock
  mkdir -p $SHAS
  cp $MANIFEST.lock $SHAS/$MANIFEST_SHA.lock # save the stable reference manifest
fi
```

##### Patch Releases

A patch release contains output from previous versions mixed with new source code. Manifests can mix such references. See [opensearch-1.1.1.yml](/manifests/1.1.1/opensearch-1.1.1.yml) for an example.

#### Assemble the Bundle 

```bash
./assemble.sh builds/opensearch/manifest.yml
```

The bundling step takes output from the build step, installs plugins, and assembles a full bundle into a `dist` folder. The input requires a path to the build manifest and is expected to be inside the `builds` directory that contains `dist`, `maven`, `plugins` and `core-plugins` subdirectories from the build step.

Artifacts will be updated as follows.

```
/dist
  <file-name>.tar.gz or .zip <- assembled tarball or zip depending on platform
  manifest.yml <- bundle manifest describing versions for the min bundle and all installed plugins and their locations
```

The following options are available in `assemble.sh`.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| -b, --base-url     | The base url to download the artifacts.                                 |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

##### Cross-Platform Builds

You can perform cross-platform builds. For example, build and assemble a Windows distribution on MacOS.

```bash
export JAVA_HOME=$(/usr/libexec/java_home) # required by OpenSearch install-plugin during assemble
./build.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot --platform windows
./assemble.sh builds/opensearch/manifest.yml
```

This will produce `dist/opensearch-1.2.0-SNAPSHOT-windows-x64.zip` on Linux and MacOS.

##### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/bundle-build/components](scripts/bundle-build/components), then default to a noop version implemented in [scripts/default/install.sh](scripts/default/install.sh).

#### Sign Artifacts

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

#### Test the Bundle

Tests the OpenSearch bundle.

This workflow contains integration, backwards compatibility and performance tests. 

More details around how this workflow is instrumented as part of CI CD, are covered [here](src/test_workflow/README.md).

Usage:

```bash
./test.sh <test-type> <path>
```

The following options are available.

| name                 | description                                                             |
|----------------------|-------------------------------------------------------------------------|
| test-type            | Run tests of a test suite. [integ-test, bwc-test, perf-test]            |
| path                 | Location of manifest(s).                                                |
| --test-run-id        | Unique identifier for a test run                                        |
| --component          | Test a specific component in a manifest                                 |
| --keep               | Do not delete the temporary working directory on both success or error. |
| -v, --verbose        | Show more verbose output.                                               |

##### Integration Tests

This step runs integration tests invoking `run_integ_test.py` in each component from bundle manifest.

To run integration tests locally, use below command. It pulls down the built bundle and its manifest file from S3, reads all components of the bundle and runs integration tests against each component.
 
Usage:

```bash
./test.sh integ-test <target>
```

For example, build locally and run integration tests.

```bash
./build.sh manifests/1.2.0/opensearch-1.2.0.yml
./assemble.sh builds/opensearch/manifest.yml
./test.sh integ-test . # looks for "./builds/opensearch/manifest.yml" and "./dist/opensearch/manifest.yml"
```

Run integration tests against an existing build.

```bash
./test.sh integ-test https://ci.opensearch.org/ci/dbc/bundle-build/1.2.0/869/linux/x64 # looks for https://.../builds/opensearch/manifest.yml and https://.../dist/opensearch/manifest.yml
```

##### Backwards Compatibility Tests

This step run backward compatibility invoking `run_bwc_test.py` in each component from bundle manifest.

Usage:

```bash
./test.sh bwc-test <target>
```

##### Performance Tests

TODO

#### Sanity Check the Bundle

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

The following example sanity-checks components in the the OpenSearch 1.2.0 manifest.

```bash
./ci.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --component [name] | Test a single component by name, e.g. `--component common-utils`.       |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

#### Auto-Generate Manifests

The [manifests workflow](src/manifests_workflow) reacts to version increments in OpenSearch and its components by extracting Gradle properties from project branches. Currently OpenSearch `main`, and `x.y` branches are checked out one-by-one, published to local maven, and their versions extracted using `./gradlew properties`. When a new version is found, a new input manifest is added to [manifests](manifests), and [a pull request is opened](.github/workflows/manifests.yml) (e.g. [opensearch-build#491](https://github.com/opensearch-project/opensearch-build/pull/491)).

Show information about existing manifests. 

```bash
./manifests.sh list
```

Check for updates and create any new manifests. 

```bash
./manifests.sh update
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --keep             | Do not delete the temporary working directory on both success or error. |
| --type             | Only list manifests of a specific type).                                |
| -v, --verbose      | Show more verbose output.                                               |

### Making a Release

#### Releasing for Linux

The Linux release is managed by a team at Amazon following [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#566](https://github.com/opensearch-project/opensearch-build/issues/566)).

#### Releasing for FreeBSD

The FreeBSD ports and packages for OpenSearch are managed by a community [OpenSearch Team](https://wiki.freebsd.org/OpenSearch) at FreeBSD.  When a new release is rolled out, this team will update the port and commit it to the FreeBSD ports tree. Anybody is welcome to help the team by providing patches for [upgrading the ports](https://docs.freebsd.org/en/books/porters-handbook/book/#port-upgrading) following the [FreeBSD Porter's Handbook](https://docs.freebsd.org/en/books/porters-handbook/book/) instructions.

#### Releasing for Windows

At this moment there's no official Windows distribution. However, this project does support building and assembling OpenSearch for Windows, with some caveats. See [opensearch-build#33](https://github.com/opensearch-project/opensearch-build/issues/33) for details.

#### Releasing for MacOS

At this moment there's no official MacOS distribution. However, this project does support building and assembling OpenSearch for MacOS. See [opensearch-build#37](https://github.com/opensearch-project/opensearch-build/issues/37) and [#38](https://github.com/opensearch-project/opensearch-build/issues/38) for more details.

### Deploying Infrastructure

Storage and access roles for the OpenSearch release process are codified in a [CDK project](deployment/README.md).

## Contributing

See [developer guide](DEVELOPER_GUIDE.md) and [how to contribute to this project](CONTRIBUTING.md). 

## Getting Help

If you find a bug, or have a feature request, please don't hesitate to open an issue in this repository.

For more information, see [project website](https://opensearch.org/) and [documentation](https://docs-beta.opensearch.org/). If you need help and are unsure where to open an issue, try [forums](https://discuss.opendistrocommunity.dev/).

## Code of Conduct

This project has adopted the [Amazon Open Source Code of Conduct](CODE_OF_CONDUCT.md). For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq), or contact [opensource-codeofconduct@amazon.com](mailto:opensource-codeofconduct@amazon.com) with any additional questions or comments.

## Security

If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright OpenSearch Contributors. See [NOTICE](NOTICE) for details.
