---
name: Release
title: "[RELEASE] Release version {{ env.VERSION }}"
labels: untriaged, release
---

## Release OpenSearch and OpenSearch Dashboards {{ env.VERSION }}

I noticed that a manifest was automatically created in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}). Please follow the following checklist to make a release.

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Document any new quality requirements or changes.
- [ ] Declare a pencils down date for new features to be merged.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] [Create a version label](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#create-or-update-labels-in-all-plugin-repos) in each component repo.
- [ ] [Create a release issue in every component repo](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#create-an-issue-in-all-plugin-repos) that links back to this issue.
- [ ] Ensure that all release issues created above are assigned to an owner in the component team.

### CI/CD

- [ ] Create Jenkins workflows that run daily snapshot builds for OpenSearch and OpenSearch Dashboards. 
- [ ] Increment each component version to {{ env.VERSION }} and ensure working CI in component repositories.
- [ ] Make pull requests to add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml) with the corresponding checks.

### Release

- [ ] Declare a release candidate build, and publish all test results.
- [ ] Verify all issued labeled `v{{ env.VERSION }}` in all projects have been resolved.
- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website) for this release.
- [ ] Author and publish a [blog post](https://github.com/opensearch-project/project-website) for this release.
- [ ] Gather, review and publish release notes.
- [ ] Publish this release on [opensearch.org](https://opensearch.org/downloads.html).

### Post Release

- [ ] Create [release tags](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging) for each component.
- [ ] Update [this template](./release_template.md) with any new or missed steps.
- [ ] Conduct a postmortem, and publish its results.
