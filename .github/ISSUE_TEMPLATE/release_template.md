---
name: Release
title: "[RELEASE] Release version {{ env.VERSION }}"
labels: untriaged, release
---

## Release OpenSearch and OpenSearch Dashboards {{ env.VERSION }}

I've noticed that a manifest was automatically created in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}). Please follow the following checklist to make a release.

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Document any new quality requirements or changes.
- [ ] Declare a pencils down date for new features to be merged.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] Create GitHub issues for the release in each component repository that link to this issue and assign an owner.

### CI/CD

- [ ] Create Jenklins workflows that run daily snapshot builds for OpenSearch and OpenSearch Dashboards. 
- [ ] Increment each components' version to {{ env.VERSION }} and ensure working CI in component repositories.
- [ ] Add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) and [manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-dashboards-{{ env.VERSION }}.yml) with the corresponding checks. 

### Release

- [ ] Declare a release candidate build and publish all test results.
- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website) for this release.
- [ ] Prepare a [blog post](https://github.com/opensearch-project/project-website) for this release.
- [ ] Gather, review and publish release notes.
- [ ] Publish this release on [opensearch.org](https://opensearch.org/downloads.html).

### Post Release

- [ ] Conduct a postmortem and publish its results.
