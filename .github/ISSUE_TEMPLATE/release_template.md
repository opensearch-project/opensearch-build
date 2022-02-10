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
