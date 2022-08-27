Coming from [opensearch-build#567](https://github.com/opensearch-project/opensearch-build/issues/567), release version 1.2. Please follow the following checklist.

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] Create, update, triage and label all features and issues targeted for this release with `v1.2.0`.

### CI/CD - _Ends Nov 2nd_

- [ ] Increment version on main to `1.2.0.0`.
- [ ] Ensure working and passing CI.
- [ ] Re(add) this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/1.2.0).

### Pre-Release

- [ ] Branch and build from a `1.2` branch.
- [ ] Update your branch in the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/1.2.0).
- [ ] Feature complete, pencils down.
- [ ] Fix bugs that target this release.

### Release testing
- [ ] Code complete phase (Nov 2 - Nov 5): Test your component within the distribution, ensuring integration, backwards compat and perf tests pass.
- [ ] Final sanity testing phase (Nov 8 - Nov 10): Final sanity testing *and* fixing of any issues you find.

### Release

- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website).
- [ ] Gather, review and publish release notes.
- [ ] Verify all issued labeled for this release are closed or labelled for the next release.

### Post Release

- [ ] Create [a release tag](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging).
- [ ] [Suggest improvements](https://github.com/opensearch-project/opensearch-build/issues/new) to [this template](https://github.com/opensearch-project/opensearch-build/meta/templates/releases/release-1.2.0.md).
- [ ] Conduct a postmortem, and publish its results.
