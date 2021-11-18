This is a component issue for release 1.1.1.
Coming from [release issue 1.1.1](https://github.com/opensearch-project/opensearch-build/issues/870), release version 1.1.1. Please follow the following checklist.

<details><summary>How to use this component issue</summary>
<p>

## This Component Issue
This component issue captures the state of the OpenSearch release, on component/plugin level, its assignee is responsible for driving the release of the component.  Please contact them or @mention them on this issue for help. 

## Release Steps
There are several steps to the release process, these steps are completed as the whole release and components that are behind present risk to the release.  The release owner completes the tasks in this ticket, whereas component owners resolve tasks on their ticket in their repositories.

Steps have completion dates for coordinating efforts between the components of a release; components can start as soon as they are ready far in advance of a future release.

You can find all the corresponding dates of each step in the release issue above.

### Component List
To aid in understanding the state of the release there is a table with status indicating each component state in the release issue.  This is updated based on the status of the component issues.

</p>
</details>


### You can find all the date in above issue 
### (We only make changes to OpenSearch-Dashboards to 1.1.1, therefore, OpenSearch stays 1.1.0.)

### Preparation

- [ ] Assign this issue to a release owner.
- [ ] Finalize scope and feature set and update [the Public Roadmap](https://github.com/orgs/opensearch-project/projects/1).
- [ ] Create, update, triage and label all features and issues targeted for this release with v1.1.1.

### CI/CD

- [ ] Increment plugin version on 1.1 branch to `1.1.1.0` (Only if you have any code changes, else, stay on 1.1.0.0 for your plugin).
- [ ] Make necessary code change if you have any patch for 1.1.1.
- [ ] Ensure working and passing CI.
- [ ] Re(add) this repo to the (if not exist) [opensearch-dashboards input manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/1.1.1/opensearch-dashboards-1.1.1.yml).

### Pre-Release

- [ ] Update your branch in the [opensearch-dashboards input manifest](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/1.1.1/opensearch-dashboards-1.1.1.yml).
- [ ] Merge any changes to 1.1 you need for the patch
- [ ] Complete integration tests, and update results in the comment, contact corresponding assigner in meta issue above if needed.
- [ ] Fix bugs that you find during the integration test, wait for a new build and test again.
- [ ] All intermittent test failures have issues filed

### Release

- [ ] Complete [documentation](https://github.com/opensearch-project/documentation-website).
- [ ] Gather, review and publish release notes.
- [ ] Verify all issued labeled for this release are closed or labelled for the next release.

### Post Release

- [ ] Create [a release tag](https://github.com/opensearch-project/.github/blob/main/RELEASING.md#tagging).
- [ ] Suggest improvements to [this template](https://github.com/opensearch-project/opensearch-plugins/templates/release.md).
- [ ] Conduct a postmortem, and publish its results.
