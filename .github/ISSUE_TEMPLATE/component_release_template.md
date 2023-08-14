This is a component issue for `{{RELEASE_VERSION}}`.
Coming from {{RELEASE_ISSUE}}. Please follow the following checklist.
__Please refer to the DATES in that post__.

<details><summary>How to use this issue</summary>
<p>

## This Component Release Issue

This issue captures the state of the OpenSearch release, on component/plugin level; its assignee is responsible for driving the release. Please contact them or @mention them on this issue for help.
Any release related work can be linked to this issue or added as comments to create visiblity into the release status.

## Release Steps

There are several steps to the release process; these steps are completed as the whole component release and components that are behind present risk to the release. The component owner resolves the tasks in this issue and communicate with the overall release owner to make sure each component are moving along as expected.

Steps have completion dates for coordinating efforts between the components of a release; components can start as soon as they are ready far in advance of a future release. The most current set of dates is on the overall release issue linked at the top of this issue.

## The Overall Release Issue

Linked at the top of this issue, the overall release issue captures the state of the entire OpenSearch release including references to this issue, the release owner which is the assignee is responsible for communicating the release status broadly.  Please contact them or @mention them on that issue for help.

## What should I do if my plugin isn't making any changes?

If including changes in this release, increment the version on `{{RELEASE_VERSION_X}}` branch to `{{RELEASE_VERSION}}` for Min/Core, and `{{RELEASE_VERSION}}.0` for components. Otherwise, keep the version number unchanged for both.

</p>
</details>

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] All the tasks in this issue have been reviewed by the release owner.
- [ ] Create, update, triage and label all features and issues targeted for this release with `v{{RELEASE_VERSION}}`.
- [ ] Finalize the code and create the the release branch `{{RELEASE_VERSION}}` from the `{{RELEASE_VERSION_X}}` branch.

### CI/CD

- [ ] All code changes for `{{RELEASE_VERSION}}` are complete.
- [ ] Ensure working and passing CI.
- [ ] Check that this repo is included in the [distribution manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/{{RELEASE_VERSION}}).

### Pre-Release

- [ ] Update to the `{{RELEASE_VERSION}}` release branch in the [distribution manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/{{RELEASE_VERSION}}).
- [ ] Increment the version on the parent branch to the next development iteration.
- [ ] Gather, review and publish release notes following the [rules](https://github.com/opensearch-project/opensearch-plugins/blob/main/RELEASE_NOTES.md) and back port it to the release branch.[git-release-notes](https://github.com/ariatemplates/git-release-notes) may be used to generate release notes from your commit history.
- [ ] Confirm that all changes for `{{RELEASE_VERSION}}` have been merged.
- [ ] Add this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/) for the next developer iteration.

### Release Testing

- [ ] Find/fix bugs using latest tarball and docker image provided in parent release issue and update the release notes if necessary.
- [ ] Code Complete: Test within the distribution, ensuring integration, backwards compatibility, and performance tests pass.
- [ ] Sanity Testing: Sanity testing *and* fixing of critical issues found.
- [ ] File issues for all intermittent test failures.

### Release

- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website).
- [ ] Verify all issued labeled for this release are closed or labelled for the next release.
- [ ] Verify the release date mentioned in release notes is correct and matches actual release date.

### Post Release

- [ ] Prepare for an eventual security fix development iteration by incrementing the version on the release branch to the next eventual patch version.
- [ ] Add this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/) of the next eventual security patch version.
- [ ] [Suggest improvements](https://github.com/opensearch-project/opensearch-build/issues/new) to [this template](https://github.com/opensearch-project/opensearch-build/blob/main/.github/ISSUE_TEMPLATE/component_release_template.md).
- [ ] Conduct a retrospective, and publish its results.
