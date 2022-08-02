<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

[![python](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml)
[![groovy](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml)
[![manifests](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml)
[![codecov](https://codecov.io/gh/opensearch-project/opensearch-build/branch/main/graph/badge.svg?token=03S5XZ80UI)](https://codecov.io/gh/opensearch-project/opensearch-build)

- [Releasing OpenSearch](#releasing-opensearch)
  - [Releases and Versions](#releases-and-versions)
  - [Creating a New Version](#creating-a-new-version)
  - [Onboarding a New Plugin](#onboarding-a-new-plugin)
  - [Building and Testing an OpenSearch Distribution](#building-and-testing-an-opensearch-distribution)
    - [Building from Source](#building-from-source)
    - [Assembling a Distribution](#assembling-a-distribution)
    - [Building Patches](#building-patches)
    - [CI/CD Environment](#cicd-environment)
    - [Latest Distribution Url](#latest-distribution-url)
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

### Releases and Versions

The OpenSearch project releases as versioned distributions of OpenSearch, OpenSearch Dashboards, and the OpenSearch plugins. It [follows semantic versioning](https://opensearch.org/blog/technical-post/2021/08/what-is-semver/). Software, such as Data Prepper, clients, and the Logstash output plugin, are versioned independently of the OpenSearch Project. They also may have independent releases from the main project distributions. The OpenSearch Project may also release software under alpha, beta, release candidate, and generally available labels. The definition of when to use these labels is derived from [the Wikipedia page on Software release lifecycle](https://en.wikipedia.org/wiki/Software_release_life_cycle). Below is the definition of when to use each label.

Release labels:

* **Alpha** - The code is released with instructions to build. Built distributions of the software may not be available. Some features many not be complete. Additional testing and developement work is planned. Distributions will be postfixed with `-alphaX` where "X" is the number of the alpha version  (e.g., "2.0-alpha1").
* **Beta** - Built distributions of the software are available. All features are completed. Additional testing and developement work is planned. Distributions will be postfixed with `-betaX` where "X" is the number of the beta version  (e.g., "2.0.0-beta1").
* **Release Candidate** - Built distributions of the software are available. All features are completed. Code is tested and minimal validation remains. At this stage the software is potentially stable and will release unless signficant bugs emerge. Distributions will be postfixed with `-rcX` where "X" is the number of the release candidate version (e.g., "2.0.0-rc1").
* **Generally Available** - Built distributions of the software are available. All features are completed and documented. All testing is completed. Distributions for generally available versions are not postfixed with an additional label (e.g., "2.0.0").

### Creating a New Version

Each new OpenSearch release process starts when any one component increments a version, typically on the `main` branch. For example, [OpenSearch#1192](https://github.com/opensearch-project/OpenSearch/pull/1192) incremented the version to 2.0. The [version check automation workflow](.github/workflows/versions.yml) will notice this change or it can be triggered [manually](https://github.com/opensearch-project/opensearch-build/actions/workflows/versions.yml), and make a pull request (e.g. [opensearch-build#514](https://github.com/opensearch-project/opensearch-build/pull/514)) that adds a new manifest (e.g. [opensearch-2.0.0.yml](manifests/2.0.0/opensearch-2.0.0.yml). After that's merged, a GitHub issue is automatically opened by [this workflow](.github/workflows/releases.yml) to make a new release using [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#566](https://github.com/opensearch-project/opensearch-build/issues/566)). Existing and new components [(re)onboard into every release](ONBOARDING.md) by submitting pull requests to each version's manifest.

### Onboarding a New Plugin

Plugin owners can follow the [Onboarding Process](ONBOARDING.md) to onboard their plugins to the release process. 

### Building and Testing an OpenSearch Distribution

The distribution workflow builds a complete OpenSearch and OpenSearch Dashboards distribution from source. You can currently build 1.0, 1.1, 1.1-SNAPSHOT and 1.2 versions. This system performs a top-down [build](src/build_workflow) of all components required for a specific OpenSearch and OpenSearch Dashboards release, then [assembles](src/assemble_workflow/) a distribution. The input to the system is a manifest that defines the order in which components should be built. All manifests for our current releases are [here](manifests). 

#### Building from Source

```bash
./build.sh manifests/1.3.0/opensearch-1.3.0.yml 
```

This builds OpenSearch 1.3.0 from source, placing the output into `./builds/opensearch`. 

See [build workflow](src/build_workflow) for more information.

#### Assembling a Distribution 

```bash
./assemble.sh builds/opensearch/manifest.yml
```

The assembling step takes output from the build step, installs plugins, and assembles a full distribition into the `dist` folder. 

See [assemble workflow](src/assemble_workflow) for more information.

#### Building Patches

A patch release contains output from previous versions mixed with new source code. Manifests can mix such references. See [opensearch-1.1.1.yml](/manifests/1.1.1/opensearch-1.1.1.yml) for an example.

OpenSearch is often released with changes in `opensearch-min`, and no changes to plugins other than a version bump. This can be performed by a solo Engineer following [a cookbook](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#increment-a-version-in-every-plugin). See also [opensearch-build#1375](https://github.com/opensearch-project/opensearch-build/issues/1375) which aims to automate incrementing versions for the next development iteration.

#### CI/CD Environment

We build, assemble, and test our artifacts on docker containers. We provide docker files in [docker/ci](docker/ci) folder, and images on [staging docker hub repositories](https://hub.docker.com/r/opensearchstaging/ci-runner/). All Jenkins pipelines can be found in [jenkins](./jenkins/). Jenkins itself is in the process of being made public and its CDK open-sourced.

See [jenkins](./jenkins) and [docker](./docker) for more information.

#### Latest Distribution Url

The distribution url has a build number (from Jenkins job) embedded inside it. See this example where `3942` is the build number. https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/2.1.0/3942/linux/arm64/rpm/builds/opensearch-dashboards/manifest.yml


The feature of `latest` distribution url is to make it build number agnostic. For the example above, its corresponding latest distribution url is as follows.

https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/2.1.0/latest/linux/arm64/rpm/builds/opensearch-dashboards/manifest.yml

It resolves `latest` to a specific build number by checking an `index.json` [file](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/2.1.0/index.json). This file has contents like this.

```
{"latest":"3942"}
```

The file is updated when a distribution build job is completed for the given product and version (or is created when such distribution job succeeds for the first time). Since one distribution build job consists of multiple stages for diffferent combinations of distribution type, platform and architecture, the `index.json` is only modified once all stages succeed. With this said, the `latest` url only works when the distribution build job succeeds at least once for the given product and version.

The resolution logic exists in [CloudFront url rewriter](https://github.com/opensearch-project/opensearch-build/tree/main/deployment/lambdas/cf-url-rewriter). The TTL (time to live) is set to `5 mins` which means that the `latest` url may need up to 5 mins to get new contents after `index.json` is updated.

All the artifacts accessible through the regular distribution url can be accessed by the `latest` url. This includes both OpenSearch Core, OpenSearch Dashboards Core and their plugins.

#### Testing the Distribution

Tests the OpenSearch distribution, including integration, backwards-compatibility and performance tests.

```bash
./test.sh <test-type> <test-manifest-path> <path>
```

See [src/test_workflow](./src/test_workflow) for more information.

#### Signing Artifacts

For all types of signing within OpenSearch project we use `opensearch-signer-client` (in progress of being open-sourced) which is a wrapper around internal signing system and is only available for authenticated users. The input requires a path to the build manifest or directory containing all the artifacts or a single artifact. 

Usage:
```bash
./sign.sh builds/opensearch/manifest.yml
```

The tool currently supports following platforms for signing.
#### PGP

Anything can be signed using PGP signing eg: tarball, any type of file, etc. A .sig file will be returned containing the signature. OpenSearch and OpenSearch dashboards distributions, components such as data prepper, etc as well as maven artifacts are signed using PGP signing. See [this page](https://opensearch.org/verify-signatures.html) for how to verify signatures.


#### WINDOWS

Windows signing can be used to sign windows executables such as .msi, .msp, .msm, .cab, .dll, .exe, .appx, .appxbundle, .msix, .msixbundle, .sys, .vxd, .ps1, .psm1, and any PE file that is supported by [Signtool.exe](https://docs.microsoft.com/en-us/dotnet/framework/tools/signtool-exe). Various windows artifacts such as SQL OBDC, opensearch-cli, etc are signed using this method. 
Windows code signing uses EV (Extended Validated) code signing certificates.

|  Types of signing/Details   | Digest           | Cipher  | Key Size|
| ------------- |:-------------| :-----| :-----|
| PGP      | SHA1 | AES-128 | 2048 |
| Windows      | SHA256      |    RSA | |
| RPM | SHA512      |    RSA | 4096 |


### Signing RPM artifacts
RPM artifacts are signed via shell script which uses a [macros template](https://github.com/opensearch-project/opensearch-build/blob/main/scripts/pkg/sign_templates/rpmmacros). More details in this [commit](https://github.com/opensearch-project/opensearch-build/commit/950d55c1ed3f82e98120541fa40ff506338c1059). See [issue](https://github.com/opensearch-project/opensearch-build/issues/1547) to add RPM artifact signing functionality to the above signing system. Currently we are only signing OpenSearch and OpenSearch dashboards RPM distributions using this method.

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
./checkout.sh manfiests/1.3.0/opensearch-1.3.0.yml
```

See [src/checkout_workflow](./src/checkout_workflow) for more information.

#### Cross-Platform Builds

You can perform cross-platform builds. For example, build and assemble a Windows distribution on MacOS.

```bash
export JAVA_HOME=$(/usr/libexec/java_home) # required by OpenSearch install-plugin during assemble
./build.sh manifests/1.3.0/opensearch-1.3.0.yml --snapshot --platform windows
./assemble.sh builds/opensearch/manifest.yml
```

This will produce `dist/opensearch-1.3.0-SNAPSHOT-windows-x64.zip` on Linux and MacOS.

#### Sanity Checking the Bundle

This workflow runs sanity checks on every component present in the bundle, executed as part of the [manifests workflow](.github/workflows/manifests.yml) in this repository. It ensures that the component GitHub repositories are correct and versions in those components match the OpenSearch version.

The following example sanity-checks components in the the OpenSearch 1.3.0 manifest.

```bash
./ci.sh manifests/1.3.0/opensearch-1.3.0.yml --snapshot
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
