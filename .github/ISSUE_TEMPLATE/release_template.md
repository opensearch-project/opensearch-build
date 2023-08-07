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

This issue captures the state of the OpenSearch release, its assignee (Release Manager) is responsible for driving the release. Please contact them or @mention them on this issue for help. There are linked issues on components of the release where individual components can be tracked. For more information check the the [Release Process OpenSearch Guide](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md).

</p>
</details>

Please refer to the following link for the release version dates: [Release Schedule and Maintenance Policy](https://opensearch.org/releases.html).

### [Preparation](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#preparation)

- [ ] [Release manager](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-manager) assigned.
- [ ] Existence of label in each component repo. For more information check the [release-label](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-label) section.
- [ ] [Increase the build frequency](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#increase-the-build-frequency).
- [ ] [Release Issue](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-issue).

### [Campaigns](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#campaigns)

- [ ] [Component Release Issue](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#component-release-issue).
- [ ] [Release Campaigns](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-campaigns).

### [Release Branch and Version Increment](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-branch-readiness) - _Ends __REPLACE_RELEASE-minus-14-days__

- [ ] [Core Release Branch](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#core).
- [ ] [Core Version Increment](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#core-version-increment).
- [ ] [Components Release Branch](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#components).
- [ ] [Components Version Increment](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#components-version-increment).

### [Feature Freeze](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#code-complete-and-feature-freeze) - _Ends __REPLACE_RELEASE-minus-12-days__

- [ ] OpenSearch / OpenSearch-Dashboards core and components teams finalize their features.

### [Code Complete](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#code-complete-and-feature-freeze) - _Ends __REPLACE_RELEASE-minus-10-days___

- [ ] Mark this as done once the [Code Complete](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#code-complete-and-feature-freeze) is reviewed.
- [ ] Create/Verify pull requests to add each component to relase input [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml).

### [Release Candidate Creation and Testing](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-candidate-creation-and-testing) - _Ends __REPLACE_RELEASE-minus-6-days___

- [ ] [Generate Release Candidate](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-candidate).
- [ ] [Integ Test TAR](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#integ-test-tar).
- [ ] [Integ Test RPM](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#integ-test-rpm).
- [ ] [Docker Build and Scan](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#docker-build-and-scan).
- [ ] [Backwards Compatibility Tests](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#backwards-compatibility-tests).
- [ ] [Windows Integration Test](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#windows-integration-test).
- [ ] [Broadcast and Communication](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#broadcast-and-communication).
- [ ] [Release Candidate Lock](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-candidate-lock).

### [Performance testing validation](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#benchmark-tests) - _Ends __REPLACE_RELEASE-minus-6-days___

- [ ] Post the benchmark-tests
- [ ] Longevity tests do not show any issues.

### [Pre Release](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#pre-release) - _Ends __REPLACE_RELEASE-minus-1-days___

- [ ] [Release Labeled Issues](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-labeled-issues).
- [ ] [Go or No-Go](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#go-or-no-go).
- [ ] [Promote Repos](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#promote-repos).
- [ ] [Promote artifacts](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#promote-artifacts).
- [ ] [Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-notes).

### [Release](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#main-release) - _Ends {__REPLACE_RELEASE-day}_

- [ ] [Maven Promotion](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#maven-promotion).
- [ ] [Docker Promotion](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#docker-promotion).
- [ ] [Release Validation](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-validation).
- [ ] [Collaboration with the Project Management Team](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#collaboration-with-the-project-management-team).

### [Release Checklist](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-checklist).

<br>
<details><summary>Release Checklist</summary>
<p>

### Pre-Release activities
- [ ] Promote Repos.
   - - [ ] OS
   - - [ ] OSD
- [ ] Promote Artifacts.
   - - [ ] Windows
   - - [ ] Linux Debian
   - - [ ] Linux RPM
   - - [ ] Linux TAR
- [ ] Consolidated Release Notes.

### Release activities
- [ ] Docker Promotion.
- [ ] Release Validation part 1.
     -  - [ ] OpenSearch and OpenSearch Dashboard Validation.
     -  - [ ] Validate the native plugin installation.
- [ ] Merge consolidated release notes PR.
- [ ] Website and Documentation Changes.
    - - [ ] Merge staging website PR.
    - - [ ] Promote the website changes to prod.
    - - [ ] Add website alert.
- [ ] Release Validation part 2.
    -  - [ ] Validate the artifact download URL's and signatures. 
- [ ] Release Validation part 3.
    -  - [ ] Trigger the validation build (Search for `Completed validation for <>` in the logs).
- [ ] Maven Promotion.
- [ ] Publish blog posts.
- [ ] Advertise on Social Media.
- [ ]  Post on public slack and Github Release issue.

### Post-Release activities
- [ ] Release Tags.
- [ ] Input Manifest Update.
- [ ] Decrease the Build Frequency.
- [ ] OpenSearch Build Release notes.
- [ ] Retrospective Issue.
- [ ] Helm and Ansible Playbook release.
- [ ] Upcoming Release Preparation.

</p>
</details>
<br>

### [Post Release](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#post-release)

- [ ] [Release Tags](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#release-tags).
- [ ] [Input Manifest Update](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#input-manifest-update).
- [ ] [OpenSearch Build Release notes](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#opensearch-build-release-notes).
- [ ] [Decrease the Build Frequency](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#decrease-the-build-frequency).
- [ ] [Retrospective Issue](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#retrospective-issue).
- [ ] [Helm and Ansible Playbook release](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#helm-and-ansible-playbook-release).
- [ ] [Upcoming Release Preparation](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASE_PROCESS_OPENSEARCH.md#upcoming-release-preparation).

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