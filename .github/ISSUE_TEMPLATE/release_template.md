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
- [ ] Declare a pencils down date for new features to be merged. 
- [ ] __REPLACE_RELEASE-minus-14-days__ is pencils down date for feature freeze.
- [ ] Update the Campaigns section to include monitoring campaigns during this release. 
- [ ] Update this issue so all `__REPLACE_RELEASE-__` placeholders have actual dates.
- [ ] Document any new quality requirements or changes.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1). 
- [ ] [Create a release issue in every component repo](https://github.com/opensearch-project/opensearch-build/blob/main/meta/README.md#create-a-release-issue) that links back to this issue, update Components section with these links.
- [ ] Ensure the label is created in each component repo for this new version, and the next minor release. [Create a version label](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#create-or-update-labels-in-all-plugin-repos)
- [ ] Ensure that all release issues created above are assigned to an owner in the component team.
- [ ] Increase the build frequency for the this release from once a day (H 1 * * *) to once every hour (H/60 * * * *) in [jenkinsFile](https://github.com/opensearch-project/opensearch-build/blob/main/jenkins/check-for-build.jenkinsfile)

### CI/CD (Feature Freeze) - _Ends __REPLACE_RELEASE-minus-14-days__

- [ ] Create Jenkins workflows that run daily snapshot builds for OpenSearch and OpenSearch Dashboards. 
- [ ] Increment each component version to {{ env.VERSION }} and ensure working CI in component repositories.
- [ ] Make pull requests to add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml) with the corresponding checks.
- [ ] OpenSearch / OpenSearch-Dashboards core and components teams finalize their features
- [ ] OpenSearch / OpenSearch-Dashboards core cut branch `<MajorVersion>.<MinorVersion>` early.

### Campaigns

__REPLACE with OpenSearch wide initiatives to improve quality and consistency.__

### Code Complete - _Ends __REPLACE_RELEASE-minus-10-days___

- [ ] Code Complete: Make sure that the code for this specific version of the release is ready and the branch corresponding to this release has been added to this release version manifest.
- [ ] Verify pull requests to add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml) have been merged.
- [ ] Gather, review and combine the release notes from components repositories.

### Release testing - _Ends __REPLACE_RELEASE-minus-6-days___

- [ ] All components should have cut branch `<MajorVersion>.<MinorVersion>` for the release.
- [ ] Declare a release candidate build, and provide the instructions with the release candidates for teams on testing (__REPLACE_RELEASE-minus-8-days__).
- [ ] Stop builds for this version of OpenSearch and/or OpenSearch Dashboards in order to avoid accidental commits going in unknowingly. Restart only if necessary else manually run the build workflow and declare new release candidate.
- [ ] Sanity Testing (__REPLACE_RELEASE-minus-8-days__ - __REPLACE_RELEASE-minus-6-days__): Sanity testing and fixing of critical issues found by teams. Teams test their components within the distribution, ensuring integration, backwards compatibility, and perf tests pass.
- [ ] Publish all test results in the comments of this issue.

### Performance testing validation - _Ends __REPLACE_RELEASE-minus-6-days___

- [ ] Performance tests do not show a regression
- [ ] Longevity tests do not show any issues

### Release - _Ends {__REPLACE_RELEASE-day}_

- [ ] Verify [all issues labeled `v{{ env.VERSION }}` in all projects](https://github.com/opensearch-project/project-meta#find-labeled-issues) have been resolved.
- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website) for this release.
- [ ] Author [blog post](https://github.com/opensearch-project/project-website) for this release.
- [ ] __REPLACE_RELEASE-minus-1-day - Publish this release on [opensearch.org](https://opensearch.org/downloads.html).
- [ ] __REPLACE_RELEASE-day - Publish a [blog post](https://github.com/opensearch-project/project-website) - release is launched!

### Post Release

- [ ] Create [release tags](https://github.com/opensearch-project/opensearch-build/blob/main/jenkins/release-tag/release-tag.jenkinsfile) for each component (Jenkins job name: release-tag-creation).
- [ ] Replace refs in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}) with tags and remove checks.
- [ ] If this is a major or minor version release, stop building previous patch version.
- [ ] Generate distribution release notes reviewed by PM team for opensearch-build repository.
- [ ] Increment version for Helm Charts [(sample PR)](https://github.com/opensearch-project/helm-charts/pull/246) for the `{{ env.VERSION }}` release.
- [ ] Increment version for Ansible Charts [(sample PR)](https://github.com/opensearch-project/ansible-playbook/pull/50) for the `{{ env.VERSION }}` release.
- [ ] Prepare [for next patch release](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#increment-a-version-in-every-plugin) by incrementing patch versions for each component.
- [ ] Update [this template](https://github.com/opensearch-project/opensearch-build/blob/main/.github/ISSUE_TEMPLATE/release_template.md) with any new or missed steps.
- [ ] Create an issue for a retrospective, solicit feedback, and publish a summary.

### Components

__Replace with links to all component tracking issues.__

| Component | On track | Release Notes |
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
