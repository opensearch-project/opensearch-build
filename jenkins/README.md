- [Jenkinsfiles](#jenkinsfiles)
  - [Check for Build](#check-for-build)
    - [Add Periodically Run Jobs](#add-periodically-run-jobs)
  - [Jenkins Shared Library](#jenkins-shared-library)

## Jenkinsfiles

* [OpenSearch](./opensearch)
* [OpenSearch Dashboards](./opensearch)
* [Docker](./docker)
* [Test](./test)


### Check for Build

To ensure that builds are trigger as changes come in the [Check-for-build](check-for-build.jenkinsfile) job is setup with a cron schedule to check manifests and run them at the appropriate build job.  From in a manifest a stable build version can be created and reference against uploaded versions.  If there is an exist match the build will be skipped, if not the job will be triggered in its own build workflow.

For concurrent builds the Check-for-build job has an internal locks to prevent interruption for the same manifest and target job name, any requests that match an existing lock will be skipped to prevent a backup of queued build jobs.

#### Add Periodically Run Jobs 

* Set cron to `H/10 * * * *` for jobs that are in active development.
* Set cron to `H 1 * * *` for all other jobs.

### Jenkins Shared Library

This project contains a Jenkins global shared library used extensively in the Jenkinsfile's in this folder.

* [Global Shared Functions](../vars)
* [Common Classes](../src/jenkins)
