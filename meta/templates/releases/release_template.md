Coming from [opensearch-build__REPLACE_ISSUE_NUMBER__](https://github.com/opensearch-project/opensearch-build/issues/__REPLACE_ISSUE_NUMBER__), release version __REPLACE_MAJOR_MINOR__. Please follow the following checklist.

<details><summary>How to use this issue</summary>
<p>

## This Component Release Issue

This issue captures the state of the OpenSearch release for this component, its assignee is responsible for driving the release. Please contact them or @mention them on this issue for help.  Any release related work can be linked to this issue or added as comments to create visiblity into the release status.

## The Overall Release Issue

Linked at the top of this issue, the overall release issue captures the state of the entire OpenSearch release including references to this issue, the release owner which is the assignee is responsible for communicating the release status broadly.  Please contact them or @mention them on that issue for help.

## Release Steps

There are several steps to the release process, these steps are completed as the whole release and components that are behind present risk to the release.  The component owner completes the tasks in this issue which are monitored by the overall release owner to make sure all components are moving along as expected.

Steps have completion dates for coordinating efforts between the components of a release; components can start as soon as they are ready far in advance of a future release.  The most current set of dates is on the overall release issue linked at the top of this issue.

</p>
</details>

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] Create, update, triage and label all features and issues targeted for this release with `v__REPLACE_MAJOR_MINOR_PATCH__`.

### CI/CD - __REPLACE_DATE___

- [ ] Check that the previous post-release action items incremented the version to `__REPLACE_MAJOR_MINOR_PATCH_BUILD__` and that CI is passing.
- [ ] Check that this repo is included in the [distribution manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/__REPLACE_MAJOR_MINOR_PATCH__).

### Pre-Release

- [ ] Branch and build from a `__REPLACE_MAJOR_MINOR__` branch.
- [ ] Increment the version on the parent branch to the next development iteration.
- [ ] Update your branch in the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/__REPLACE_MAJOR_MINOR_PATCH__) for this release.
- [ ] Add this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/) for the next developer iteration.
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
- [ ] Update the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/__REPLACE_MAJOR_MINOR_PATCH__) to use the release tag.
- [ ] Prepare for an eventual security fix development iteration by incrementing the version on the release branch to the next eventual patch version.
- [ ] Add this repo to the [manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/) of the next eventual security patch version.
- [ ] [Suggest improvements](https://github.com/opensearch-project/opensearch-build/issues/new) to [this template](https://github.com/opensearch-project/opensearch-build/blob/main/meta/templates/releases/release_template.md).
- [ ] Conduct a postmortem, and publish its results.
