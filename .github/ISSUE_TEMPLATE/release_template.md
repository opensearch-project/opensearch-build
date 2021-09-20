---
name: Release
title: "[RELEASE] Release version {{ env.VERSION }}"
labels: untriaged, release
---

## Release OpenSearch and OpenSearch Dashboards {{ env.VERSION }}

I've noticed that a manifest has been automatically created in [manifests/{{ env.VERSION }}](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}). Please follow the following checklist.

### OpenSearch

- [ ] Add a Jenklins workflow that runs daily snapshot builds. 
- [ ] Increment each components' version to {{ env.VERSION }} and ensure working CI.
- [ ] Add each component to [manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml](/opensearch-project/opensearch-build/tree/main/manifests/{{ env.VERSION }}/opensearch-{{ env.VERSION }}.yml) with the corresponding checks. 

### OpenSearch Dashboards

- [ ] TODO