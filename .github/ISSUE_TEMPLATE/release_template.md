---
name: Release
title: "[RELEASE] Release version {{ env.VERSION }}"
labels: untriaged, release, v{{ env.VERSION }}
---

## Release OpenSearch and OpenSearch Dashboards {{ env.VERSION }}

I noticed that a manifest was automatically created in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}). Please follow the following checklist to make a release.

<details><summary>How to use this issue</summary>
<p>

## This Release Issue

This issue captures the state of the OpenSearch release, its assignee is responsible for driving the release. Please contact them or @mention them on this issue for help. There are linked issues on components of the release where individual components can be tracked.  More details are included in the Maintainers [Release owner](https://github.com/opensearch-project/opensearch-build/blob/main/MAINTAINERS.md#release-owner) section.

## Release Steps

There are several steps to the release process, these steps are completed as the whole release and components that are behind present risk to the release.  The release owner completes the tasks in this ticket, whereas component owners resolve tasks on their ticket in their repositories.

Steps have completion dates for coordinating efforts between the components of a release; components can start as soon as they are ready far in advance of a future release.

### Component List

To aid in understanding the state of the release there is a table with status indicating each component state. This is updated based on the status of the component issues.

</p>
</details>

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Declare a pencils down date for new features to be merged. ___REPLACE_RELEASE-minus-14-days__ is pencils down.
- [ ] Update the Campaigns section to include monitoring campaigns during this release. 
- [ ] Update this issue so all `__REPLACE_RELEASE-__` placeholders have actual dates.
- [ ] Document any new quality requirements or changes.
- [ ] Declare a pencils down date for new features to be merged.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] [Create a version label](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#create-or-update-labels-in-all-plugin-repos) in each component repo for this, and the next minor release.
- [ ] [Create a release issue in every component repo](https://github.com/opensearch-project/opensearch-build/blob/main/meta/README.md#create-a-release-issue) that links back to this issue, update Components section with these links.
- [ ] Ensure that all release issues created above are assigned to an owner in the component team.

### CI/CD - _Ends __REPLACE_RELEASE-minus-14-days___

- [ ] Create Jenkins workflows that run daily snapshot builds for OpenSearch and OpenSearch Dashboards. 
- [ ] Increment each component version to {{ env.VERSION }} and ensure working CI in component repositories.
- [ ] Make pull requests to add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml) with the corresponding checks.

### Campaigns

__REPLACE with OpenSearch wide initiatives to improve quality and consistency.__

### Release testing - _Ends __REPLACE_RELEASE-minus-6-days___

- [ ] Code Complete (__REPLACE_RELEASE-minus-14-days__ - __REPLACE_RELEASE-minus-11-days__): Teams test their component within the distribution, ensuring integration, backwards compatibility, and perf tests pass.
- [ ] Sanity Testing (__REPLACE_RELEASE-minus-8-days__ - __REPLACE_RELEASE-minus-6-days__): Sanity testing and fixing of critical issues found by teams.

### Performance testing validation - _Ends __REPLACE_RELEASE-minus-6-days___
- [ ] Performance tests do not show a regression

<details><summary>How to identify regressions in performance tests</summary>
<p>

Disclaimer: the guidelines listed below were determined based on empirical testing using OpenSearch Benchmark. 
These tests were run against OpenSearch 1.2 build #762 and used the nyc_taxis workload with 2 warmup and 3 test iterations. 
The values listed below are **not** applicable to other configurations. More details on the test setup can be found here: https://github.com/opensearch-project/OpenSearch/issues/2461

Using the aggregate results from the nightly performance test runs, compare indexing and query metrics to the specifications layed out in the table

Please keep in mind the following:

1. Expected values are rough estimates. These are only meant to establish a baseline understanding of test results. 
2. StDev% Mean is the standard deviation as a percentage of the mean. This is expected variation between tests. 
   1. If the average of several tests consistently falls outside this bound there may be a performance regression. 
3. MinMax% Diff is the worst case variance between any two tests with the same configuration. 
   1. If there is a difference greater than this value than there is likely a performance regression or an issue with the test setup. 
      1. In general, comparing one off test runs should be avoided if possible.


|Instance Type|Security|Expected Indexing Throughput Avg (req/s)|Expected Indexing Error Rate|Indexing StDev% Mean|Indexing MinMax% Diff|Expected Query Latency p90 (ms)|Expected Query Latency p99 (ms)|Expected Query Error Rate|Query StDev% Mean|Query MinMax% Diff|
|---|---|---|---|---|---|---|---|---|---|---|
|m5.xlarge|Enabled|30554|0|~5%|~12%|431|449|0|~10%|~23%|
|m5.xlarge|Disabled|34472|0|~5%|~15%|418|444|0|~10%|~25%|
|m6g.xlarge|Enabled|38625|0|~3%|~8%|497|512|0|~8%|~23|
|m6g.xlarge|Disabled|45447|0|~2%|~3%|470|480|0|~5%|~15%|

Note that performance regressions are based on decreased indexing throughput and/or increased query latency.

Additionally, error rates on the order of 0.01% are acceptable, though higher ones may be cause for concern.


</p>
</details>

- [ ] Longevity tests do not show any issues

<details><summary>How to identify issues in longevity tests</summary>
<p>

Navigate to the Jenkins build for a longevity test. Look at the Console Output

Search for:

```
INFO:root:Test can be monitored on <link>
```

Navigate to that link then click the link for "Live Dashboards"

Use the following table to monitor metrics for the test:

|Metric|Health Indicators / Expected Values|Requires investigations / Cause for concerns|
|---|---|---|
|Memory|saw tooth graph|upward trends|
|CPU| |upward trends or rising towards 100%|
|Threadpool|0 rejections|any rejections|
|Indexing Throughput|Consistent rate during each test iteration|downward trends|
|Query Throughput|Varies based on the query being issued|downward trends between iterations|
|Indexing Latency|Consistent during each test iteration|upward trends|
|Query Latency|Varies based on the query being issued|upward trends|

</p>
</details>


### Release - _Ends {__REPLACE_RELEASE-day}_

- [ ] Declare a release candidate build, and publish all test results.
- [ ] Verify [all issues labeled `v{{ env.VERSION }}` in all projects](https://github.com/opensearch-project/project-meta#find-labeled-issues) have been resolved.
- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website) for this release.
- [ ] Author [blog post](https://github.com/opensearch-project/project-website) for this release.
- [ ] Gather, review and publish release notes. [git-release-notes](https://github.com/ariatemplates/git-release-notes) may be used to generate release notes from your commit history.
- [ ] __REPLACE_RELEASE-minus-1-day - Publish this release on [opensearch.org](https://opensearch.org/downloads.html).
- [ ] __REPLACE_RELEASE-day - Publish a [blog post](https://github.com/opensearch-project/project-website) - release is launched!

### Post Release

- [ ] Create [release tags](https://github.com/opensearch-project/opensearch-build/issues/378#issuecomment-999700848) for each component.
- [ ] Replace refs in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}) with tags and remove checks.
- [ ] Prepare [for next patch release](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#increment-a-version-in-every-plugin) by incrementing patch versions for each component.
- [ ] Lower the [frequency of builds](https://github.com/opensearch-project/opensearch-build/pull/1475) for this version of OpenSearch and/or OpenSearch Dashboards.
- [ ] Update [this template](https://github.com/opensearch-project/opensearch-build/blob/main/.github/ISSUE_TEMPLATE/release_template.md) with any new or missed steps.
- [ ] Create an issue for a retrospective, solicit feedback, and publish a summary.

### Components

__Replace with links to all component tracking issues.__

| Component | On track | Notes |
| --------- | -------- | ----- |
| {COMPONENT_ISSUE_LINK} | {INDICATOR}} | {STATUS} |

<details><summary>Legend</summary>
<p>

| Symbol | Meaning |
| -------- | ---------- |
| :green_circle: | On track with overall release |
| :yellow_circle: | Missed last milestone |
| :red_circle: | Missed multiple milestones |

</p>
</details>
