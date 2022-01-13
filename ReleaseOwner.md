<img src="https://opensearch.org/assets/brand/SVG/Logo/opensearch_logo_default.svg" height="64px"/>

## Responsibilities


## Github issue for tracking the release
We use a github issue (eg: issue [#1417](https://github.com/opensearch-project/opensearch-build/issues/1417)) to track 
the tasks and progress of the current release. This issue is assigned to the release 
manager of the release. The release manager is responsible for executing or making sure 
all the tasks listed on the issue are executed correctly. These components are further discussed below.

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

### Issue tracking
- Holds the number of issues that are linked to the current release. 
- The number can be viewed using the links from the "State, Bug and Enhancement"

### Recurring Tasks
1. Keep the Issue tracking table updated as much as possible.
2. Circle back to make sure all the component versions are bumped up correctly
