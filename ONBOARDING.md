
- [Component Onboarding](#component-onboarding)
  - [Onboard to OpenSearch Meta](#onboard-to-opensearch-meta)
    - [opensearch-plugins](#opensearch-plugins)
  - [Onboard to Build Workflow](#onboard-to-build-workflow)
  - [Onboard to `test-workflow`](#onboard-to-test-workflow)
- [Onboarding to universal/1-click release process](#onboarding-to-universal--1-click-release-process)
  
## Component Onboarding

This document describes steps to onboard a new plugin to release workflow for continuous integration and testing.

### Onboard to OpenSearch Meta

#### opensearch-plugins

Add the new plugin to the [opensearch-plugins meta](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md), e.g. [opensearch-plugins#97](https://github.com/opensearch-project/opensearch-plugins/pull/97), which added [cross-cluster-replication](https://github.com/opensearch-project/cross-cluster-replication).


### Onboard to Build Workflow

1. Update a [manifest](/manifests) for a particular release to include your plugin.  For example to be included in the 1.1.0 release, you would update [opensearch-1.1.0.yml](https://github.com/opensearch-project/opensearch-build/blob/opensearch-1.1.0/manifests/1.1.0/opensearch-1.1.0.yml). We require your plugin name, repository URL, and git ref that should be used. For unreleased versions this should be a branch in your repository.  Once a release is cut, these refs will be updated to build from a tag or specific commit hash.

2. Create a `scripts/build.sh` if you have specific requirements that are not covered by the [default build.sh script](/scripts/default/opensearch/build.sh) and commit it to your repository.

3. Ensure your `build.sh` reads and passes along both `-Dbuild.snapshot=` and `-Dopensearch.version=` flags.  Snapshot builds should produce a -SNAPSHOT tagged artifact for example `opensearch-plugin-1.1.0.0-SNAPSHOT.zip` where a release build of the same component would produce `opensearch-plugin-1.1.0.0.zip`.

4. Execute `./build.sh` to ensure your component builds and all artifacts are correctly placed into ./artifacts/ with correct output names.

5. Execute `./assemble.sh` to ensure the full bundle is assembled and placed in to /bundles/*.tar.gz.  Unpack the tarball to ensure all your components are placed in their correct locations.

6. Publish a PR to this repo including the updated manifest and the names of the artifacts being added.

### Onboard to `test-workflow`

1. Update the test configuration file (use 1.3.0 as an example), [opensearch-1.3.0-test.yml](https://github.com/opensearch-project/opensearch-build/blob/opensearch-1.3.0/manifests/1.3.0/opensearch-1.3.0-test.yml), for a particular release, to include your plugin. This test configuration defines full suite of tests - `integ`, `bwc`, that can be run on the plugin.

2. For integration testing, the `test-workflow` runs integration tests available in the plugin repository. You will need to add `integ-test` config for your plugin in opensearch-1.3.0-test.yml, [example](https://github.com/opensearch-project/opensearch-build/blob/opensearch-1.3.0/manifests/1.3.0/opensearch-1.3.0-test.yml).
   
    1. It supports two test configs - `with-security` and `without-security`, which runs test with security plugin enabled and disabled respectively. Choose one or both depending on what your plugin integration tests support.
   
    2. If your plugin is dependent on `job-scheduler` zip, you can define that in `build-dependencies` in the config. Currently, the test workflow only supports `job-scheduler` as build dependency. Please create an issue if your plugin needs more support.

3. For backward compatibility testing, the `test-workflow` runs backward compatibility tests available in the plugin repository, (see [reference](https://github.com/opensearch-project/anomaly-detection/blob/d9a122d05282f7efc1e24c61d64f18dec0fd47af/build.gradle#L428)). Like integration test, it has a set of configurable options defined in opensearch-1.3.0-test.yml, [example](https://github.com/opensearch-project/opensearch-build/blob/opensearch-1.3.0/manifests/1.3.0/opensearch-1.3.0-test.yml).

    1. It supports two test configs - `with-security` and `without-security`, which runs test with security plugin enabled and disabled respectively. Choose one or both depending on what your plugin integration tests support.


## Onboarding to universal / 1-click release process:

This document describes steps to onboard a new component to universal or 1-click release process.

See https://github.com/opensearch-project/opensearch-build/issues/1234 for details about end to end workflow.

1. Please ensure that [opensearch-ci-bot](https://github.com/opensearch-ci-bot) has the write access to your repository. If not, request by creating an [issue](https://github.com/opensearch-project/opensearch-build/issues) in this repository.
1. Add a webhook token as credentials to [CI system](https://build.ci.opensearch.org/) using configuration as code. To generate the token, use command `head -30 /dev/urandom | sha512sum | awk '{print $1;}'` that generates random alpha-numeric string.
1. Create a Jenkins workflow that utilizes one of the [build libraries](https://github.com/opensearch-project/opensearch-build-libraries#library-details) to publish the artifacts to right platform. Please check the [library requirements and retrieval methods](https://github.com/opensearch-project/opensearch-build-libraries#jenkins-shared-libraries) before using it.
1. For publishing to a new platform (other than ones specified above) a new library needs to be added. (ETA: 2 weeks)
1. **Release Drafter**: Release drafter is a GitHub Action workflow that drafts a release that may or may not contain the release artifacts. The drafted release acts as a trigger to the Jenkins workflow. It also acts as a staging environment for release artifacts. This is to make sure the build environment remains the same even for release artifacts. [Example](https://github.com/opensearch-project/opensearch-py/blob/main/.github/workflows/release-drafter.yml)
    * _**2 Person Review**_ It is highly recommended to add 2 PR approval for any release workflow. In universal release process this can be added to release-drafter workflow as that is the starting point to trigger any release. See how to [add the mechanism in the workflow](https://github.com/opensearch-project/opensearch-dsl-py/pull/102). The mentioned solution creates an issue that notifies and assigns the reviewers. [Example](https://github.com/gaiksaya/opensearch-dsl-py/issues/6).
1. **Jenkins Workflow:** Once the Jenkins workflow is added to the repository, onboard the workflow to publicly available [CI system](https://build.ci.opensearch.org/)
    1. Create a `New Item`
    2. Name it `<component-name>-release`
    3. Select `Pipeline` as type of the project
    4. Hit `Ok` and scroll to the bottom of the page
    5. Select "Pipeline script from SCM" under Pipeline section
       - _SCM_: GitHub repository link. eg: https://github.com/opensearch-project/opensearch-build
       - _Script_ Path: Relative path to jenkins file. eg: jenkins/check-for-build.jenkinsfile
    6. Run the workflow once in order to update the configuration of the Jenkins Workflow. You can abort once the workflow starts pulling the docker image. 
1. **GitHub Webhook**: Add webhook to your GitHub repository by going to repository settings → Click `Webhooks`:
    | Key                                                 | Value                                                                                     |
    |-----------------------------------------------------|-------------------------------------------------------------------------------------------|
    | Payload URL                                         | https://build.ci.opensearch.org/generic-webhook-trigger/invoke?token=tokenAddedInStep2 |
    | Content type                                        | application/json                                                                          |
    | SSL verification                                    | Enable                                                                                    |
    | Which events would you like to trigger this webhook | Releases. Please ensure to deselect the default option "Pushes"                           |
    | Active                                              | Enable                                                                                    |
1. Once a webhook is added, it will send a ping to check the connectivity (✅). You can check the ping by going to repository settings → Webhooks → Click on `Recent Deliveries` tabs
1. Add `RELEASING.md` file to the repository documenting how to release the artifact. [Example](https://github.com/opensearch-project/opensearch-py-ml/blob/main/RELEASING.md)
1. **Adding tests:** Each library has a respective library tester associated with it that can be used to test you jenkins workflow. This tests can be used to verify that the workflow is making the calls. The build system used is gradle. 
For example, this [PublishToNpm test](https://github.com/opensearch-project/opensearch-build-libraries/blob/main/tests/jenkins/TestPublishToNpm.groovy) uses [PublishToNpmLibTester](https://github.com/opensearch-project/opensearch-build-libraries/blob/main/tests/jenkins/lib-testers/PublishToNpmLibTester.groovy) with expected parameter that can be unique to your workflow. The assertions makes sure that calls to npm registry is made which is mandatory to release an artifact.
