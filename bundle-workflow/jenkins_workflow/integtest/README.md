- [Integration Tests Jenkins Job](#integration-tests-jenkins-job)
  - [Job Parameters](#job-parameters)
### Integration Tests Jenkins Job

This job runs integration tests for a bundle via `test_integration.sh` in Jenkins.

#### Job Parameters
| name        | description                                                |
|-------------|------------------------------------------------------------|
| ARTIFACT_BUCKET_NAME |  Artifact S3 bucket in Jenkins ENV                |
| AWS_ACCOUNT_PUBLIC |  AWS Account ID to read S3 bucket in Jenkins ENV    |
| BUNDLE_TEST_ID |  Unique identifier for a bundle test suite run          |
| bundle_manifest |  Path to bundle manifest in Artifact S3 bucket         |
| build_manifest |  Path to build manifest in Artifact S3 bucket           |
| architecture | CPU Architecture of bundle                                |
 