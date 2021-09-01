# OpenSearch Build / Release Ownership

On OpenSearch there are a number of processes that could be handled by individual development teams - and we are fortunate that there are a number of dedicate team members that can centralize the effort to help these teams scale so smaller teams can keep focused on their areas.  This team is called the OpenSearch DevOps team, it is not exclusive, but it’s dedicated.

This document’s purpose is to clarify where the boundaries between these projects exist and how to get things done.

## Build

OpenSearch is build on code and that code needs to build.  No specific build system is required; however, gradle and yarn are recommendations and will have the most support.

Repository: OpenSearch Project [Repositories](https://github.com/orgs/opensearch-project/repositories)

Ownership:

* Repository Teams: Manage repo build scripts that produce artifacts for development, testing, and release.

### Continuous Integration

Continuous integration makes sure that a repository has a baseline quality level by running automation against pull requests.  Repositories can leverage GitHub Actions, where heavy weight solution is needed can run on an OpenSearch Jenkins cluster.

Repository: OpenSearch Jenkins - Not yet public.

Ownership:

* Repository Teams: Manage GitHub Actions, onboard with OpenSearch Jenkins cluster.
* DevOps: Manage OpenSearch Jenkins environment, jobs, features/improvements, access polices.

### Distribution creation

The OpenSearch distribution refers to building all the required artifacts and bundling them together into a OpenSearch product deployable by end users. OpenSearch distribution have manifest file describing the artifacts are packaged together.  The manifest file also contains the details of particular git reference / commit_id that is used to build the component.

Repository: OpenSearch [Build](https://github.com/opensearch-project/opensearch-build)

Ownership:

* OpenSearch core team: Sets release cadence for OpenSearch distribution releases, determines dates and release criteria, creates new version manifest, triggers publishing of new build.
* Repository teams: Onboard bundling build script, update manifest for components to be included in the new OpenSearch distribution.
* DevOps: Build/bundling process, uploading to artifact management systems, signing OpenSearch distribution artifacts, publishing signed OpenSearch distribution.

### Packaging

Packaging refers to supporting different kind of distributions, platforms and architectures.  Such as Docker, Helm, RPM, Debs, CDK configuration for Single/Multi node

Repository: OpenSearch Project [Repositories](https://github.com/orgs/opensearch-project/repositories)

Ownership:

* Repository teams: Onboard packaging process with DevOps, managing packaging scripts,
* DevOps: Publishing packages to OpenSearch managed publishing systems.

## Testing

Validation of OpenSearch systems components before promotion and release steps.

Ownership:

* Repository teams: Testing practices, tests cases, build scripts which can execute them

### Unit, Component, & Backward Compatibility testing

Running tests at build time for source code, typically triggered during pull requests and snapshot build.

Ownership:

* Repository teams: Authoring tests, Manage GitHub Actions, onboard with OpenSearch Jenkins cluster.

### OpenSearch distribution Testing

Running tests on OpenSearch distribution after they have been deployed to a cluster.

Ownership:

* Repository teams: Authoring tests, scripts to execute tests
* DevOps: Setup up a cluster and trigger scripts to start tests against the cluster, capture logs and debug output from the cluster.

#### Integration Testing

Running the core and plugins integration tests against a OpenSearch distribution to approve for release

Ownership:

* OpenSearch core team: Authoring test cases
* Repository teams: Authoring plugin specific integration tests.
* DevOps: Test Execution and Results Reporting.

#### Perf Testing

Performance testing consist of running rally tracks on OpenSearch distribution. We run these tests with a specific machine and cluster configurations.  The results of these tests are stored for everyone to see.

Ownership:

* OpenSearch core team: Deep Diving Issues, Performance improvements, Defining Performance Criteria, Defining Configuration
* DevOps: Performance Test Execution, Results Reporting, Historical Results.
