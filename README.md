<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

[![python](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml)
[![groovy](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml)
[![manifests](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml)
[![codecov](https://codecov.io/gh/opensearch-project/opensearch-build/branch/main/graph/badge.svg?token=03S5XZ80UI)](https://codecov.io/gh/opensearch-project/opensearch-build)

- [Releasing OpenSearch](#releasing-opensearch)
  - [Creating a New Version](#creating-a-new-version)
  - [Onboarding a New Plugin](#onboarding-a-new-plugin)
  - [Building and Testing an OpenSearch Distribution](#building-and-testing-an-opensearch-distribution)
    - [Building from Source](#building-from-source)
    - [Assembling a Distribution](#assembling-a-distribution)
    - [Building Patches](#building-patches)
    - [CI/CD Environment](#cicd-environment)
    - [Testing the Distribution](#testing-the-distribution)
    - [Signing Artifacts](#signing-artifacts)
  - [Making a Release](#making-a-release)
    - [Releasing for Linux](#releasing-for-linux)
    - [Releasing for FreeBSD](#releasing-for-freebsd)
    - [Releasing for Windows](#releasing-for-windows)
    - [Releasing for MacOS](#releasing-for-macos)
  - [Utilities](#utilities)
    - [Checking Out Source](#checking-out-source)
    - [Cross-Platform Builds](#cross-platform-builds)
    - [Sanity Checking the Bundle](#sanity-checking-the-bundle)
    - [Auto-Generating Manifests](#auto-generating-manifests)
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

The distribution workflow builds a complete OpenSearch and OpenSearch Dashboards distribution from source. You can currently build 1.0, 1.1, 1.1-SNAPSHOT and 1.2 versions. This system performs a top-down [build](src/build_workflow) of all components required for a specific OpenSearch and OpenSearch Dashboards release, then [assembles](src/assemble_workflow/) a distribution. The input to the system is a manifest that defines the order in which components should be built. All manifests for our current releases are [here](manifests). 

#### Building from Source

```bash
./build.sh manifests/1.2.0/opensearch-1.2.0.yml
```

This builds OpenSearch 1.2.0 from source, placing the output into `./builds/opensearch`. 

See [build workflow](src/build_workflow) for more information.

#### Assembling a Distribution 

```bash
./assemble.sh builds/opensearch/manifest.yml
```

The assembling step takes output from the build step, installs plugins, and assembles a full distribition into the `dist` folder. 

See [assemble workflow](src/assemble_workflow) for more information.

#### Building Patches

A patch release contains output from previous versions mixed with new source code. Manifests can mix such references. See [opensearch-1.1.1.yml](/manifests/1.1.1/opensearch-1.1.1.yml) for an example.

#### CI/CD Environment

We build, assemble, and test our artifacts on docker containers. We provide docker files in [docker/ci](docker/ci) folder, and images on [staging docker hub repositories](https://hub.docker.com/r/opensearchstaging/ci-runner/). All Jenkins pipelines can be found in [jenkins](./jenkins/). Jenkins itself is in the process of being made public and its CDK open-sourced.

See [jenkins](./jenkins) and [docker](./docker) for more information.

#### Testing the Distribution

Tests the OpenSearch distribution, including integration, backwards-compatibility and performance tests.

```bash
./test.sh <test-type> <test-manifest-path> <path>
```

See [src/test_workflow](./src/test_workflow) for more information.

#### Signing Artifacts

The signing step takes the manifest file created from the build step and signs all its component artifacts using a tool called `opensearch-signer-client` (in progress of being open-sourced). The input requires a path to the build manifest and is expected to be inside the artifacts directory with the same directories mentioned in the build step. 

```bash
./sign.sh builds/opensearch/manifest.yml
```

See [src/sign_workflow](./src/sign_workflow) for more information.

### Making a Release

#### Releasing for Linux

The Linux release is managed by a team at Amazon following [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#566](https://github.com/opensearch-project/opensearch-build/issues/566)).

#### Releasing for FreeBSD

The FreeBSD ports and packages for OpenSearch are managed by a community [OpenSearch Team](https://wiki.freebsd.org/OpenSearch) at FreeBSD.  When a new release is rolled out, this team will update the port and commit it to the FreeBSD ports tree. Anybody is welcome to help the team by providing patches for [upgrading the ports](https://docs.freebsd.org/en/books/porters-handbook/book/#port-upgrading) following the [FreeBSD Porter's Handbook](https://docs.freebsd.org/en/books/porters-handbook/book/) instructions.

#### Releasing for Windows

At this moment there's no official Windows distribution. However, this project does support building and assembling OpenSearch for Windows, with some caveats. See [opensearch-build#33](https://github.com/opensearch-project/opensearch-build/issues/33) for details.

#### Releasing for MacOS

At this moment there's no official MacOS distribution. However, this project does support building and assembling OpenSearch for MacOS. See [opensearch-build#37](https://github.com/opensearch-project/opensearch-build/issues/37) and [#38](https://github.com/opensearch-project/opensearch-build/issues/38) for more details.

### Utilities

#### Checking Out Source

The [checkout workflow](src/checkout_workflow) checks out source code for a given manifest for further examination.

```bash
./checkout.sh manfiests/1.2.0/opensearch-1.2.0.yml
```

See [src/checkout_workflow](./src/checkout_workflow) for more information.

#### Cross-Platform Builds

You can perform cross-platform builds. For example, build and assemble a Windows distribution on MacOS.

```bash
export JAVA_HOME=$(/usr/libexec/java_home) # required by OpenSearch install-plugin during assemble
./build.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot --platform windows
./assemble.sh builds/opensearch/manifest.yml
```

This will produce `dist/opensearch-1.2.0-SNAPSHOT-windows-x64.zip` on Linux and MacOS.

#### Sanity Checking the Bundle

This workflow runs sanity checks on every component present in the bundle, executed as part of the [manifests workflow](.github/workflows/manifests.yml) in this repository. It ensures that the component GitHub repositories are correct and versions in those components match the OpenSearch version.

The following example sanity-checks components in the the OpenSearch 1.2.0 manifest.

```bash
./ci.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot
```

See [src/ci_workflow](./src/ci_workflow) for more information.

#### Auto-Generating Manifests

The [manifests workflow](src/manifests_workflow) reacts to version increments in OpenSearch and its components by extracting Gradle properties from project branches. When a new version is found, a new input manifest is added to [manifests](manifests), and [a pull request is opened](.github/workflows/manifests.yml) (e.g. [opensearch-build#491](https://github.com/opensearch-project/opensearch-build/pull/491)).

Show information about existing manifests. 

```bash
./manifests.sh list
```
Check for updates and create any new manifests. 

```bash
./manifests.sh update
```

See [src/manifests_workflow](./src/manifests_workflow) for more information.

### Deploying Infrastructure

Storage and access roles for the OpenSearch release process are codified in a [CDK project](./deployment/README.md).

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
