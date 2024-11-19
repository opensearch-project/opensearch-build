<img src="https://raw.githubusercontent.com/opensearch-project/opensearch-build/main/opensearch_build_image.png" height="64px" alt="OpenSearch Build">

[![python](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/python-tests.yml)
[![groovy](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/groovy-tests.yml)
[![codecov](https://codecov.io/gh/opensearch-project/opensearch-build/branch/main/graph/badge.svg?token=03S5XZ80UI)](https://codecov.io/gh/opensearch-project/opensearch-build)

- [Releasing OpenSearch](#releasing-opensearch)
  - [Releases and Versions](#releases-and-versions)
  - [Release labels](#release-labels)
- [Onboarding a New Plugin](#onboarding-a-new-plugin)
- [Building and Testing an OpenSearch Distribution](#building-and-testing-an-opensearch-distribution)
  - [Testing the Distribution](#testing-the-distribution)
  - [Signing Artifacts](#signing-artifacts)
    - [PGP](#pgp)
    - [Windows](#windows)
  - [Signing RPM artifacts](#signing-rpm-artifacts)
- [Making a Release](#making-a-release)
  - [Releasing for Linux](#releasing-for-linux)
  - [Releasing for FreeBSD](#releasing-for-freebsd)
  - [Releasing for Windows](#releasing-for-windows)
  - [Releasing for macOS](#releasing-for-macos)
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

### Releasing OpenSearch

Please refer to the [release process document](https://github.com/opensearch-project/opensearch-build/wiki/Releasing-the-Distribution) for detailed information on how to release the OpenSearch and OpenSearch Dashboards software.


#### Releases and Versions

The OpenSearch project releases as versioned distributions of OpenSearch, OpenSearch Dashboards, and the OpenSearch plugins. It [follows semantic versioning](https://opensearch.org/blog/technical-post/2021/08/what-is-semver/). Software, such as Data Prepper, clients, and the Logstash output plugin, are versioned independently of the OpenSearch Project. They also may have independent releases from the main project distributions. The OpenSearch Project may also release software under alpha, beta, release candidate, and generally available labels. The definition of when to use these labels is derived from [the Wikipedia page on Software release lifecycle](https://en.wikipedia.org/wiki/Software_release_life_cycle). Below is the definition of when to use each label.

#### Release labels:

* **Alpha** - The code is released with instructions to build. Built distributions of the software may not be available. Some features many not be complete. Additional testing and development work is planned. Distributions will be postfixed with `-alphaX` where "X" is the number of the alpha version  (e.g., "2.0-alpha1").
* **Beta** - Built distributions of the software are available. All features are completed. Additional testing and development work is planned. Distributions will be postfixed with `-betaX` where "X" is the number of the beta version  (e.g., "2.0.0-beta1").
* **Release Candidate** - Built distributions of the software are available. All features are completed. Code is tested and minimal validation remains. At this stage the software is potentially stable and will release unless significant bugs emerge. Distributions will be postfixed with `-rcX` where "X" is the number of the release candidate version (e.g., "2.0.0-rc1").
* **Generally Available** - Built distributions of the software are available. All features are completed and documented. All testing is completed. Distributions for generally available versions are not postfixed with an additional label (e.g., "2.0.0").


### Onboarding a New Plugin

Plugin owners can follow the [Onboarding Process](ONBOARDING.md) to onboard their plugins to the release process. 

### Building and Testing an OpenSearch Distribution

See [wiki](https://github.com/opensearch-project/opensearch-build/wiki/Building-an-OpenSearch-and-OpenSearch-Dashboards-Distribution)

#### Testing the Distribution

See [wiki](https://github.com/opensearch-project/opensearch-build/wiki/Testing-the-Distribution)

#### Signing Artifacts

For all types of signing within OpenSearch project we use `opensearch-signer-client` (in progress of being open-sourced) which is a wrapper around internal signing system and is only available for authenticated users. The input requires a path to the build manifest or directory containing all the artifacts or a single artifact. 

Usage:

```bash
./sign.sh builds/opensearch/manifest.yml
```

The tool currently supports following platforms for signing.

##### PGP

Anything can be signed using PGP signing eg: tarball, any type of file, etc. A `.sig` file will be returned containing the signature. OpenSearch and OpenSearch dashboards distributions, components such as data prepper, etc. as well as maven artifacts are signed using PGP signing. See [this page](https://opensearch.org/verify-signatures.html) for how to verify signatures.


##### Windows

Windows signing can be used to sign windows executables such as `.msi, .msp, .msm, .cab, .dll, .exe, .appx, .appxbundle, .msix, .msixbundle, .sys, .vxd, .ps1, .psm1`, and any PE file that is supported by [Signtool.exe](https://docs.microsoft.com/en-us/dotnet/framework/tools/signtool-exe). Various windows artifacts such as SQL OBDC, opensearch-cli, etc are signed using this method. 
Windows code signing uses EV (Extended Validated) code signing certificates.

|  Types of signing/Details   | Digest           | Cipher  | Key Size|
| ------------- |:-------------| :-----| :-----|
| PGP      | SHA1 | AES-128 | 2048 |
| Windows      | SHA256      |    RSA | |
| RPM | SHA512      |    RSA | 4096 |


#### Signing RPM artifacts

RPM artifacts are signed via a legacy shell script which uses a [macros template](scripts/pkg/sign_templates/rpmmacros). See [this commit](https://github.com/opensearch-project/opensearch-build/commit/950d55c1ed3f82e98120541fa40ff506338c1059) for more information and [this issue](https://github.com/opensearch-project/opensearch-build/issues/1547) to add RPM artifact signing functionality to the above signing system. Currently we are only signing OpenSearch and OpenSearch dashboards RPM distributions using this method.

See [src/sign_workflow](./src/sign_workflow) for more information.


### Making a Release

#### Releasing for Linux and Windows

The Linux / Windows release is managed by a team at Amazon following [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#2649](https://github.com/opensearch-project/opensearch-build/issues/2649)).

#### Releasing for FreeBSD

The FreeBSD ports and packages for OpenSearch are managed by a community [OpenSearch Team](https://wiki.freebsd.org/OpenSearch) at FreeBSD.  When a new release is rolled out, this team will update the port and commit it to the FreeBSD ports tree. Anybody is welcome to help the team by providing patches for [upgrading the ports](https://docs.freebsd.org/en/books/porters-handbook/book/#port-upgrading) following the [FreeBSD Porter's Handbook](https://docs.freebsd.org/en/books/porters-handbook/book/) instructions.

#### Releasing for macOS

At this moment there's no official macOS distribution. However, this project does support building and assembling OpenSearch for macOS. See [opensearch-build#37](https://github.com/opensearch-project/opensearch-build/issues/37) and [#38](https://github.com/opensearch-project/opensearch-build/issues/38) for more details.

### Utilities

#### Checking Out Source

The [checkout workflow](src/checkout_workflow) checks out source code for a given manifest for further examination.

```bash
./checkout.sh manifests/1.3.0/opensearch-1.3.0.yml
```

See [src/checkout_workflow](./src/checkout_workflow) for more information.

#### Cross-Platform Builds

You can perform cross-platform builds. For example, build and assemble a Windows distribution on macOS.

```bash
export JAVA_HOME=$(/usr/libexec/java_home) # required by OpenSearch install-plugin during assemble
./build.sh manifests/1.3.0/opensearch-1.3.0.yml --snapshot --platform windows
./assemble.sh builds/opensearch/manifest.yml
```

This will produce `dist/opensearch-1.3.0-SNAPSHOT-windows-x64.zip` on Linux and macOS.

#### Sanity Checking the Bundle

This workflow runs sanity checks on every component present in the bundle, executed as part of the [manifests workflow](.github/workflows/manifests.yml) in this repository. It ensures that the component GitHub repositories are correct and versions in those components match the OpenSearch version.

The following example sanity-checks components in the OpenSearch 1.3.0 manifest.

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

This project uses jenkins as the build infrastructure for building, testing and releasing the artifacts. The infrastructure is deployed using CDK and code can be found in [opensearch-ci](https://github.com/opensearch-project/opensearch-ci/tree/main) repository.

## Contributing

See [developer guide](DEVELOPER_GUIDE.md) and [how to contribute to this project](CONTRIBUTING.md). 

## Getting Help

If you find a bug, or have a feature request, please don't hesitate to open an issue in this repository.

For more information, see [project website](https://opensearch.org/) and [documentation](https://opensearch.org/docs/). If you need help and are unsure where to open an issue, try [forums](https://discuss.opendistrocommunity.dev/).

## Code of Conduct

This project has adopted the [Amazon Open Source Code of Conduct](CODE_OF_CONDUCT.md). For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq), or contact [opensource-codeofconduct@amazon.com](mailto:opensource-codeofconduct@amazon.com) with any additional questions or comments.

## Security

If you discover a potential security issue in this project we ask that you notify OpenSearch Security directly via email to security@opensearch.org. Please do **not** create a public GitHub issue.

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright OpenSearch Contributors. See [NOTICE](NOTICE) for details.
