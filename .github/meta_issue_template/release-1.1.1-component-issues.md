This is a component issue for release 1.1.1.
Coming from [release issue 1.1.1](https://github.com/opensearch-project/opensearch-build/issues/870), release version 1.1.1. Please follow the following checklist.

<details><summary>How to use this component issue</summary>
<p>

## This Component Issue
This component issue captures the state of the OpenSearch release, on component/plugin level, its assignee is responsible for driving the release of the component.  Please contact them or @mention them on this issue for help. 

## Release Steps
There are several steps to the release process, components that are behind present risk to the release.  Component owners resolve tasks on this ticket to communicate with the overall release owner.

Steps have completion dates for coordinating efforts between the components of a release; components can start as soon as they are ready far in advance of a future release.

You can find all the corresponding dates of each step in the release issue above.

## What should I do if my plugin isn't making any changes?
If including changes in this release, increment the version on 1.1 branch to `1.1.1` for Min/Core, and `1.1.1.0` for components. Otherwise, keep the version number unchanged for both.

</p>
</details>


### You can find all the date in above issue 

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] All the tasks in this issue have been reviewed by the release owner.
- [ ] Create, update, triage and label all features and issues targeted for this release with v1.1.1.


### CI/CD

- [ ] All code changes for 1.1.1 are complete.
- [ ] Ensure working and passing CI.

### Pre-Release

- [ ] Confirm that all changes for 1.1.1 have been merged.
- [ ] Complete integration and sanity tests, and update results in the comment, [example](https://github.com/opensearch-project/opensearch-build/issues/1118).
- [ ] Find/fix bugs using latest tarball and docker image provided in meta issue.
- [ ] Completed release candidate testing build #TBD.
- [ ] All intermittent test failures have issues filed.

### Release

- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website).
- [ ] Gather, review and publish release notes.
- [ ] Verify all issued labeled for this release are closed or labelled for the next release.

### Post Release

- [ ] Create [a release tag](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging).
- [ ] Suggest improvements to [this template](https://github.com/opensearch-project/opensearch-build/blob/main/.github/ISSUE_TEMPLATE/release_template.md).
- [ ] Conduct a retrospect, and publish its results.
