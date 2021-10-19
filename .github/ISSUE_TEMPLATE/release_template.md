---
name: Release
title: "[RELEASE] Release version {{ env.VERSION }}"
labels: untriaged, release, v{{ env.VERSION }}
---

## Release OpenSearch and OpenSearch Dashboards {{ env.VERSION }}

I noticed that a manifest was automatically created in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}). Please follow the following checklist to make a release.

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Declare a pencils down date for new features to be merged. _RELEASE-minus-14-days is pencils down_
- [ ] Update the Campaigns section to include monitoring campaigns during this release. 
- [ ] Update this issue so all `RELEASE-` placeholders have actual dates.
- [ ] Document any new quality requirements or changes.
- [ ] Declare a pencils down date for new features to be merged.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] [Create a version label](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#create-or-update-labels-in-all-plugin-repos) in each component repo.
- [ ] [Create a release issue in every component repo](https://github.com/opensearch-project/opensearch-build/blob/main/meta/README.md#create-a-release-issue) that links back to this issue, update Components section with these links.
- [ ] Ensure that all release issues created above are assigned to an owner in the component team.

### CI/CD - _Ends RELEASE-minus-14-days_

- [ ] Create Jenkins workflows that run daily snapshot builds for OpenSearch and OpenSearch Dashboards. 
- [ ] Increment each component version to {{ env.VERSION }} and ensure working CI in component repositories.
- [ ] Make pull requests to add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml) with the corresponding checks.

### Campaigns

__Replace with OpenSearch wide initiatives to improve quality and consistency.__

### Release testing - _Ends RELEASE-minus-6-days_

- [ ] Code Complete (RELEASE-minus-14-days - RELEASE-minus-11-days): Teams test their component within the distribution, ensuring integration, backwards compatibility, and perf tests pass.
- [ ] Sanity Testing (RELEASE-minus-8-days - RELEASE-minus-6-days): Sanity testing *and* fixing of critical issues found by teams.

### Release - _Ends {RELEASE-day}_

- [ ] Declare a release candidate build, and publish all test results.
- [ ] Verify all issued labeled `v{{ env.VERSION }}` in all projects have been resolved.
- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website) for this release.
- [ ] Author [blog post](https://github.com/opensearch-project/project-website) for this release.
- [ ] Gather, review and publish release notes.
- [ ] RELEASE-minus-1-day - Publish this release on [opensearch.org](https://opensearch.org/downloads.html).
- [ ] RELEASE-day - Publish [blog post](https://github.com/opensearch-project/project-website) - release is launched!

### Post Release

- [ ] Create [release tags](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging) for each component.
- [ ] Update [this template](./release_template.md) with any new or missed steps.
- [ ] Conduct a postmortem, and publish its results.

### Components

__Replace with links to all component tracking issues.__