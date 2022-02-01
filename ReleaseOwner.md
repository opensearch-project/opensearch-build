<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

- [Responsibilities](#responsibilities)
- [Github issue for tracking the release](#github-issue-for-tracking-the-release)
- [Communication Channel](#communication-channel)
- [Describing Tasks](#describing-tasks)
  - [Preparation](#preparation)
  - [Declare a release candidate build](#declare-a-release-candidate-build)
  - [Issue tracking](#issue-tracking)
  - [Run Integration Tests](#run-integration-tests)
  - [Opensearch maven release](#opensearch-maven-release)
- [Release Day](#release-day)
- [Post Release Tasks](#post-release-tasks)
  
## Responsibilities
Reponsibilities of a release manager includes but not limited to - 
- ensuring completion of all tasks on the Release Issue
- Keep track of any unresolved bugs and features that may affect the release timeline
- complete the [Release Day](#release-day) Tasks

## Github issue for tracking the release
We use a github issue (eg: issue [#1417](https://github.com/opensearch-project/opensearch-build/issues/1417)) to track 
the tasks and progress of the current release. This issue is assigned to the release 
manager of the release. The release manager is responsible for executing or making sure 
all the tasks listed on the issue are executed correctly. These components are further discussed below.

## Communication Channel
All communication will should be done through the github release issue and the release channel on slack. 
Tag `@here` for any important updated regarding the releases, such as finalizing build number, integ test execution etc.

## Describing Tasks
### Preparation
1. Assign this issue to a release owner. 
2. Make sure the issue is marked as "in progress" and is assigned to the release manager 
3. Document any new quality requirements or changes.
4. [Create a version label](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#create-or-update-labels-in-all-plugin-repos) in each component repo for this, and the next minor release.
    `ghi label 'v1.2.4' -c '#0052cc'`
    - Document the command used to generate the label (as above)
5. Confirm that OpenSearch-Dashboards does not need an updated manifest
    - This checkbox will be marked if the there is no dashboards release 

6. Make sure the version is bumped for all the repositories below
  - [alerting](https://github.com/opensearch-project/alerting)
  - [anomaly-detection](https://github.com/opensearch-project/anomaly-detection)
  - [reports-scheduler](https://github.com/opensearch-project/OpenSearch-Dashboards)
  - [dashboards-report](https://github.com/opensearch-project/OpenSearch-Dashboards)
  - [index-management](https://github.com/opensearch-project/index-management)
  - [job-scheduler](https://github.com/opensearch-project/job-scheduler)
  - [k-NN](https://github.com/opensearch-project/k-NN)
  - [sql](https://github.com/opensearch-project/sql)
  - [opensearch-observability](https://github.com/opensearch-project/observability)
  - [asynchronous-search](https://github.com/opensearch-project/asynchronous-search)
  - [cross-cluster-replication](https://github.com/opensearch-project/cross-cluster-replication)
  - [performance-analyzer](https://github.com/opensearch-project/performance-analyzer)
  - [performance-analyzer-rca](https://github.com/opensearch-project/performance-analyzer-rca)
  - [security](https://github.com/opensearch-project/security)
  - [opensearch](https://github.com/opensearch-project/OpenSearch)
  - [common-utils](https://github.com/opensearch-project/common-utils)
  - [opensearch-java](https://github.com/opensearch-project/opensearch-java)
  - [opensearch-build](https://github.com/opensearch-project/opensearch-build)

8. All the components then need to be added to opensearch-manifest such as [manifests/1.2.4/opensearch-1.2.4.yml](/opensearch-project/opensearch-build/tree/main/manifests/1.2.4/opensearch-1.2.4.yml)

### Declare a release candidate build
Once the new manifest file is merged, a build will be automatically triggered with the links to the 
artifacts and manifest file published on the console output and slack channel respectively.

The message will also contain the build number of the success build. Once the build is a success, 
we declare them available for testing. (Example - [link](https://github.com/opensearch-project/opensearch-build/issues/1417#issuecomment-1010576235)).

The message will contain the steps and to test the release candidates. 
One can simply reuse the message with updated values for the following - 
- gist
  - can be created using an existing gist with updated version numbers
- Update the build number used
- update the urls for manifest and tar.gz files for arm64
- update the urls for manifest and tar.gz files for x64

**Note:** The release candidate can be updated in future if there is another merge related to the release. Make sure to 
select the release candidate for integration tests after all the merges for the release are completed. As a release manager,
raise concerns over any delayed merges that can potentially change the release timeline.

### Issue tracking
- Holds the number of issues that are linked to the current release. 
- The number can be viewed using the links from the "State, Bug and Enhancement"

### Run Integration Tests
- Use the jenkins job to run integration tests for `arm64` and `x64`
- Create an issue publish all test results of the tests Eg: [Integration tests for 1.2.4 OpenSearch Artifacts](https://github.com/opensearch-project/opensearch-build/issues/1479)

### Recurring Tasks
1. Keep the Issue tracking table updated as much as possible.
2. Circle back to make sure all the component versions are bumped up correctly

### Opensearch maven release
Run the job `maven-bundle-build` with the build number and the version of the release. 
This will release the candidated to sonatype staging. 

This step should be executed one day before the release, since the artifacts on sonatype will otherwise expire.

## Release Day
1. Verify all issued labeled v1.2.4 in all projects have been resolved.
2. Complete [documentation](https://github.com/opensearch-project/documentation-website) for this release. 
   - This will be done with the help of PMs
3. Maven release 
   - Release the maven artifacts from staging to prod on sonatype. **This action is not reversible**
4. Execute the `distribution-promotion` job to sign and promote opensearch, opensearch-dashboards and native plugins
5. Publish Docker images
   - Use the `dockerhub-ecr-promote` job to promote artifacts from dockerhub staging to dockerhub production
6. Gather, review and publish release notes. [git-release-notes](https://github.com/ariatemplates/git-release-notes)
7. Publish this release on [opensearch.org](https://opensearch.org/downloads.html)
   - PMs will execute this step
8. Publish forum posts - release is launched! Eg: https://discuss.opendistrocommunity.dev/t/opensearch-1-2-4-is-now-available/8330
   - PMs will execute this step
9. Publish [blog post](https://github.com/opensearch-project/project-website) - release is launched!
   - PMs will execute this step

## Post Release Tasks
1. Create [release tags](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging) for each component.
2. Replace refs in manifests/<version> with tags. Eg:
   - [manifests/1.2.4](/opensearch-project/opensearch-build/tree/main/manifests/1.2.4)
   - [PR link](https://github.com/opensearch-project/opensearch-build/pull/1503)
3. Update [this template](https://github.com/opensearch-project/opensearch-build/blob/main/.github/ISSUE_TEMPLATE/release_template.md) with any new or missed steps.
4. Conduct a retrospective meeting with everyone involved and publish its results on a github issue
   - Eg: [1.2.4 Retrospective Issue](https://github.com/opensearch-project/opensearch-build/issues/1514)

## FAQs
1. How to get help on a critical issue?
> Narrow down the issue source. Reach out the respective component's release engineer/manager for the issue. Create an issue 
> in the respective component's repository. Also list the issue on the release issue for visibility. Eg: [issue comment](https://github.com/opensearch-project/opensearch-build/issues/1417#issuecomment-1011675002)
