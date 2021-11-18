Coming from [opensearch-build#870](https://github.com/opensearch-project/opensearch-build/issues/870), release version 1.1.1. Please follow the following checklist.
### You can find all the date in above issue 
### (We only make changes to OpenSearch-Dashboards to 1.1.1, therefore, OpenSearch stays 1.1.0.)

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] Create, update, triage and label all features and issues targeted for this release with v1.1.1.

### CI/CD

- [ ] Increment version on main to `1.1.1.0`.
- [ ] Ensure working and passing CI.
- [ ] Re(add) this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/1.1.1).

### Pre-Release

- [ ] Branch and build from a `1.1` branch.
- [ ] Update your branch in the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/1.1.1).
- [ ] Feature complete, pencils down.
- [ ] Apply sanity testing, and update results in the comment, contact corresponding assigner in meta issue above if needed.
- [ ] Fix bugs that target this release.

### Release

- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website).
- [ ] Gather, review and publish release notes.
- [ ] Verify all issued labeled for this release are closed or labelled for the next release.

### Post Release

- [ ] Create [a release tag](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging).
- [ ] Suggest improvements to [this template](https://github.com/opensearch-project/opensearch-plugins/templates/release.md).
- [ ] Conduct a postmortem, and publish its results.
