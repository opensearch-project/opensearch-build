<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

[![tests](https://github.com/opensearch-project/opensearch-build/actions/workflows/bundle-workflow.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/bundle-workflow.yml)
[![manifests](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml/badge.svg)](https://github.com/opensearch-project/opensearch-build/actions/workflows/manifests.yml)
[![codecov](https://codecov.io/gh/opensearch-project/opensearch-build/branch/main/graph/badge.svg?token=03S5XZ80UI)](https://codecov.io/gh/opensearch-project/opensearch-build)

- [Releasing OpenSearch](#releasing-opensearch)
  - [Creating a New Version](#creating-a-new-version)
  - [Onboarding a New Plugin](#onboarding-a-new-plugin)
  - [Building and Testing an OpenSearch Distribution](#building-and-testing-an-opensearch-distribution)
  - [Making a Release](#making-a-release)
    - [Releasing for Linux](#releasing-for-linux)
    - [Releasing for FreeBSD](#releasing-for-freebsd)
  - [Deploying infrastructure](#deploying-infrastructure)
- [Contributing](#contributing)
- [Getting Help](#getting-help)
- [Code of Conduct](#code-of-conduct)
- [Security](#security)
- [License](#license)
- [Copyright](#copyright)

## Releasing OpenSearch

### Creating a New Version

OpenSearch and OpenSearch Dashboards are distributed as bundles that include both core engines and plugins. Each new OpenSearch release process starts when any one component increments a version, typically on the `main` branch. For example, [OpenSearch#1192](https://github.com/opensearch-project/OpenSearch/pull/1192) incremented the version to 2.0. The [manifest automation workflow](.github/workflows/manifests.yml) will notice this change, and make a pull request (e.g. [opensearch-build#514](https://github.com/opensearch-project/opensearch-build/pull/514)) that adds a new manifest (e.g. [opensearch-2.0.0.yml](manifests/2.0.0/opensearch-2.0.0.yml). After that's merged, a GitHub issue is automatically opened by [this workflow](.github/workflows/releases.yml) to make a new release using [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#566](https://github.com/opensearch-project/opensearch-build/issues/566)). Existing and new components [(re)onboard into every release](ONBOARDING.md) by submitting pull requests to each version's manifest.

### Onboarding a new plugin

Plugin owners can follow the [Onboarding document](ONBOARDING.md) to onboard their plugins to the release process. 

### Building and Testing an OpenSearch Distribution

OpenSearch and its components are built from source, assembled, signed and tested using the [bundle workflow](bundle-workflow/README.md).

### Making a Release

#### Releasing for Linux

The Linux release is managed by a team at Amazon following [this release template](.github/ISSUE_TEMPLATE/release_template.md) (e.g. [opensearch-build#566](https://github.com/opensearch-project/opensearch-build/issues/566)).

#### Releasing for FreeBSD

The FreeBSD ports and packages for OpenSearch are managed by a community [OpenSearch Team](https://wiki.freebsd.org/OpenSearch) at FreeBSD.  When a new release is rolled out, this team will update the port and commit it to the FreeBSD ports tree. Anybody is welcome to help the team by providing patches for [upgrading the ports](https://docs.freebsd.org/en/books/porters-handbook/book/#port-upgrading) following the [FreeBSD Porter's Handbook](https://docs.freebsd.org/en/books/porters-handbook/book/) instructions.

### Deploying infrastructure

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

