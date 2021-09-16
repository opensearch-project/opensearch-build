- [Tests Jenkins Job](#tests-jenkins-job)
  - [Job Parameters](#job-parameters)
### Tests Jenkins Job

This job runs integration/bwc tests for a bundle via `test.sh` in Jenkins.

#### Job Parameters
| name        | description                                                |
|-------------|------------------------------------------------------------|
| ARTIFACT_BUCKET_NAME |  Artifact S3 bucket in Jenkins ENV                |
| opensearch_version |  OpenSearch version                                 |
| build_id |  Unique identifier for a bundle build                         |
| architecture | CPU Architecture of bundle                                |
| test_run_id | Unique identifier for a test run                           |
| test_suite | Run a specific test suite. [integ-test, bwc-test]      |
