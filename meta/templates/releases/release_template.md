Coming from [opensearch-build__REPLACE_ISSUE_NUMBER__](https://github.com/opensearch-project/opensearch-build/issues/__REPLACE_ISSUE_NUMBER__), release version __REPLACE_MAJOR_MINOR__. Please follow the following checklist.

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] Create, update, triage and label all features and issues targeted for this release with `v__REPLACE_MAJOR_MINOR_PATCH__`.

### CI/CD - __REPLACE_DATE___

- [ ] Increment version on main to `__REPLACE_MAJOR_MINOR_PATCH_BUILD__`.
- [ ] Ensure working and passing CI.
- [ ] Re(add) this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/__REPLACE_MAJOR_MINOR_PATCH__).

### Pre-Release

- [ ] Branch and build from a `__REPLACE_MAJOR_MINOR__` branch.
- [ ] Update your branch in the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/__REPLACE_MAJOR_MINOR_PATCH__).
- [ ] Increment the version on the parent branch.
- [ ] Feature complete, pencils down.
- [ ] Fix bugs that target this release.

### Release Testing

- [ ] Code Complete (__REPLACE_REPLACE_RELEASE-minus-14-days__ - __REPLACE_RELEASE-minus-11-days__): Test within the distribution, ensuring integration, backwards compatibility, and performance tests pass.
- [ ] Sanity Testing (__REPLACE_REPLACE_RELEASE-minus-8-days__ - __REPLACE_RELEASE-minus-6-days__): Sanity testing *and* fixing of critical issues found.

### Release

- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website).
- [ ] Gather, review and publish release notes.
- [ ] Verify all issued labeled for this release are closed or labelled for the next release.

### Post Release

- [ ] Create [a release tag](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging).
- [ ] [Suggest improvements](https://github.com/opensearch-project/opensearch-build/issues/new) to [this template](https://github.com/opensearch-project/opensearch-build/blob/main/meta/templates/releases/release_template.md).
- [ ] Conduct a postmortem, and publish its results.
