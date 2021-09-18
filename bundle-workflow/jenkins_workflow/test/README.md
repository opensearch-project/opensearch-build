- [Orchestrator](#orchestrator)
  - [Input Parameters](#input-parameters)
- [Testsuite](#testsuite)
  - [Input Parameters](#input-parameters)

### Orchestrator

This is a jenkins pipeline that kicks off all long running test jobs on a given build artifact. It accepts `build_id`, `opensearch_version` and `architecture` as input parameters to uniquely identify a build artifact. It kicks off `integ-test`, `bwc-test`, `perf-test` jobs in parallel and notifies the designated channels when the workflow finishes. 
 
#### Input parameters

| name        | description                                                |
|-------------|------------------------------------------------------------|
| opensearch_version |  OpenSearch version                                 |
| build_id |  Unique identifier for a bundle build                         |
| architecture | CPU Architecture of bundle                                |


### Testsuite 

This job runs integration/bwc/perf tests for a bundle via `test.sh` in Jenkins.

#### Job Parameters
| name        | description                                                |
|-------------|------------------------------------------------------------|
| ARTIFACT_BUCKET_NAME |  Artifact S3 bucket in Jenkins ENV                |
| opensearch_version |  OpenSearch version                                 |
| build_id |  Unique identifier for a bundle build                         |
| architecture | CPU Architecture of bundle                                |
| test_run_id | Unique identifier for a test run                           |
