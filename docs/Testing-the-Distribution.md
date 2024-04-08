# Testing a Distribution

The OpenSearch and OpenSearch-Dashboards run Integration, Backward Compatibility tests at the distribution level. Along with this, OpenSearch also runs Performance tests at the distribution level.
Just like build, the distribution testing framework also depends on manifest. In this case, a test manifest. See sample test manifests for [OpenSearch](https://github.com/opensearch-project/opensearch-build/blob/main/legacy-manifests/2.11.1/opensearch-2.11.1-test.yml) and [OpenSearch-Dashboards](https://github.com/opensearch-project/opensearch-build/blob/main/legacy-manifests/2.11.1/opensearch-dashboards-2.11.1-test.yml).

## Test Manifest

The test manifest consist of the details of running the tests at the distribution such as, docker image to run tests on, component details such as name, configuration and what kind of tests to run, testing configuration such as with or without secutity as well as any additional configuration to be added other than default to the test cluster, etc. See the [schema](https://github.com/opensearch-project/opensearch-build/blob/main/src/manifests/test_manifest.py#L14-L38) for test manifest.

## Testing in local

The [test-workflow](https://github.com/opensearch-project/opensearch-build/tree/main/src/test_workflow) hosts the source code for distribution test framework. 

```
./test.sh integ-test manifests/1.3.5/opensearch-1.3.5-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.5/latest/linux/x64/tar
```

Additional arguments:

| name                   | description                                                             |
|------------------------|-------------------------------------------------------------------------|
| test-type              | Run tests of a test suite. [integ-test, bwc-test, perf-test]            |
| test-manifest-path     | Specify a test manifest path.                                           |
| --paths                | Location of manifest(s).                                                |
| --test-run-id          | Unique identifier for a test run.                                       |
| --component [name ...] | Test a subset of specific components.                                   |
| --keep                 | Do not delete the temporary working directory on both success or error. |
| -v, --verbose          | Show more verbose output.                                               |

### Integration Tests
In order to run the tests in your local, you can avoid installing the packages with right version by using a docker image. Each test manifest consist of the docker image to run tests on. 

```
  docker run -u root -it opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v3 /bin/bash
```

Set up the right JAVA_HOME version or node version as per the distribution version and clone this repository to start using testing framework.


To run integration tests locally, use below command. This pulls down the built bundle and its manifest file, reads all components of the distribution, and runs integration tests against each component.
 
Usage:

```bash
./test.sh integ-test <test-manifest-path> <target>
```

For example, build locally and run integration tests.

```bash
./build.sh manifests/1.3.5/opensearch-1.3.5.yml
./assemble.sh builds/opensearch/manifest.yml
./test.sh integ-test manifests/1.3.5/opensearch-1.3.5-test.yml . # looks for "./builds/opensearch/manifest.yml" and "./dist/opensearch/manifest.yml"
```

Or run integration tests against an existing build.

```bash
./test.sh integ-test manifests/1.3.5/opensearch-1.3.5-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.5/5960/linux/x64/tar # looks for https://.../builds/opensearch/manifest.yml and https://.../dist/opensearch/manifest.yml
```

To run OpenSearch Dashboards integration tests.

```bash
./test.sh integ-test manifests/1.3.0/opensearch-dashboards-1.3.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.5/5960/linux/x64/tar
opensearch-dashboards=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/1.3.5/4056/linux/x64/tar
```

To run OpenSearch Dashboards integration tests with local artifacts on different distributions
```bash
./test.sh integ-test manifests/2.0.0/opensearch-dashboards-2.0.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0-rc1/latest/linux/x64/tar opensearch-dashboards=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/2.0.0-rc1/latest/linux/x64/tar
./test.sh integ-test manifests/2.0.0/opensearch-dashboards-2.0.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0-rc1/latest/linux/x64/rpm opensearch-dashboards=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/2.0.0-rc1/latest/linux/x64/rpm
```

:warning: RPM Test requires user to run the `./test.sh` command with sudo permission, as rpm requires root to install and start the service.


### Backwards Compatibility Tests

The BWC tests running on distribution level are using the same framework from OpenSearch. The test cluster is spin up with the `latest` distribution bundle of provided version exclusively when the project is initialized with property `-PcustomDistributionDownloadType=bundle`. In this repo, the test workflow will be enable this gradle property by default.[BWC test script](https://github.com/opensearch-project/opensearch-build/blob/edffab782abf96390b3993ccc92425c63ab77884/scripts/default/bwctest.sh#L38)

Example distribution bundle URL: `https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.2/latest/linux/x64/tar/dist/opensearch/opensearch-1.3.2-linux-x64.tar.gz`
This feature for BWC testing is supported for distribution versions starting `v1.3.2`.

On CI level for plugins, security certificates need to be manually imported when spinning up the test cluster as security plugin is included in the distribution bundle. When upgrading the version within the test cluster, `nextNodeToNextVersion` is used for a single node upgrade and `goToNextVersion` is for a full restart upgrade.

See [anomaly-detection#766](https://github.com/opensearch-project/anomaly-detection/pull/766) or [observability#1366](https://github.com/opensearch-project/observability/pull/1366) for more information.

Runs backward compatibility invoking `run_bwc_test.py` in each component from a distribution manifest.

Usage:

```bash
./test.sh bwc-test <test-manifest-path> <target>
```

For example, build locally and run BWC tests.

```bash
./build.sh manifests/1.3.0/opensearch-1.3.0.yml
./assemble.sh builds/opensearch/manifest.yml
./test.sh bwc-test manifests/1.3.0/opensearch-1.3.0-test.yml . # looks for "./builds/opensearch/manifest.yml" and "./dist/opensearch/manifest.yml"
```

Or run BWC tests against an existing build.

```bash
./test.sh bwc-test manifests/1.3.0/opensearch-1.3.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0-rc1/latest/linux/x64/tar # looks for https://.../builds/opensearch/manifest.yml and https://.../dist/opensearch/manifest.yml
```

To run OpenSearch Dashboards BWC tests.

```bash
./test.sh bwc-test manifests/1.3.0/opensearch-dashboards-1.3.0-test.yml --paths 
opensearch-dashboards=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/1.3.5/4056/linux/x64/tar
```

### Performance Tests

Runs benchmarking tests on a remote opensource OpenSearch cluster, uses [OpenSearch Benchmark](https://github.com/opensearch-project/OpenSearch-Benchmark).
At a high-level the benchmarking test workflow uses [opensearch-cluster-cdk](https://github.com/opensearch-project/opensearch-cluster-cdk.git) to first set-up an OpenSearch cluster (single/multi-node) and then executes `opensearch-benchmark` to run benchmark test against that cluster. The performance metric that opensearch-benchmark generates during the run are ingested into another OS cluster for further analysis and dashboarding purpose.

The benchmarking tests will be run nightly and if you have a feature in any released/un-released OpenSearch version that you want to benchmark periodically please create an issue and the team will reach out to you. In case you want to run the benchmarking test locally you can use `opensearch-cluster-cdk` repo to spin up an OS cluster in your personal AWS account and then use `opensearch-benchmark` to run performance test against it. The detailed instructions are available on respective GitHub repositories.

#### Onboard feature for nightly benchmark runs:

1. Checkout [opensearch-build](https://github.com/opensearch-project/opensearch-build) repo and open `jenkins/opensearch/benchmark-test.jenkinsfile` file.
2. You will then need add an entry in `parameterizedCron` section of the jenkinsfile.
3. The structure of the `parameterizedCron` section as follows:   
   1. Schedule: `H <HOUR> * * *`, edit the `HOUR` section to any hour of the day, 0-24. `H` adds a jitter to the cron to make sure multiple crons are not started together.   
   2. BUNDLE_MANIFEST_URL: The distribution manifest URL that contains the artifact details such as tar location, arch, build id, commit-id, etc. 
   3. TEST_WORKLOAD: This could be any workload that [opensearch-benchmark-workload](https://github.com/opensearch-project/opensearch-benchmark-workloads) repo provides, if not provided `nyc-taxis` is used as default.   
   4. SINGLE_NODE_CLUSTER: Values are `true/false`. Do you want to run the benchmark against a single-node cluster or multi-node.    
   5. USE_50_PERCENT_HEAP: Values are `true/false`. Recommended to use 50 percent physical memory as heap. Keep this `true`.   
   6. MIN_DISTRIBUTION: Values are `true/false`. If the `BUNDLE_MANIFEST_URL` you provided is for a min/snapshot distribution then set this as `true` else don't provide this parameter.    
   7. ADDITIONAL_CONFIG: The configuration that needs to be added to `opensearch.yml` to enable your feature.   
   8. USER_TAGS: The metadata that needs to be added to the benchmark metrics ingested in datastore, this helps filter out the metrics for each use-case. Mandatory tags are `run-type:nightly,segrep:<disabled|enabled>,arch:<arm64|x64>,instance-type:<instance-type>,major-version:<3x|2x>,cluster-config:<arch>-<instance-type>-<string that will help identify the feature>`
   9. WORKLOAD_PARAMS: Additional parameters that need to be passed to opensearch-benchmark workload.
   10. To get more information on each parameter and explore more options please visit [here](https://github.com/opensearch-project/opensearch-build/blob/main/jenkins/opensearch/benchmark-test.jenkinsfile#L140-L247)    

Here's the sample entry for enabling nightly runs for `remote-store` feature   
```
H 9 * * * %BUNDLE_MANIFEST_URL=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.10.0/latest/linux/arm64/tar/dist/opensearch/manifest.yml;TEST_WORKLOAD=http_logs;SINGLE_NODE_CLUSTER=false;DATA_NODE_COUNT=3;USE_50_PERCENT_HEAP=true;ENABLE_REMOTE_STORE=true;CAPTURE_SEGMENT_REPLICATION_STAT=true;USER_TAGS=run-type:nightly,segrep:enabled-with-remote-store,arch:arm64,instance-type:r6g.xlarge,major-version:2x,cluster-config:arm64-r6g.xlarge-3-data-3-shards;ADDITIONAL_CONFIG=opensearch.experimental.feature.remote_store.enabled:true cluster.remote_store.enabled:true opensearch.experimental.feature.segment_replication_experimental.enabled:true cluster.indices.replication.strategy:SEGMENT;WORKLOAD_PARAMS={"number_of_replicas":"2","number_of_shards":"3"}
```

Once you have added the configuration in the jenkinsfile please raise the PR and opensearch-infra team will review it.   

## Testing in CI/CD

The `build` workflow automates the process to generate all OpenSearch and OpenSearch Dashboards artifacts, and provide them as distributions to the `test` workflow, which runs exhaustive testing on the artifacts based on the artifact type. The next section talks in detail about the test workflow. See the details below for each type of tests run at the distribution level. All the distribution level test workflows (integ tests, BWC tests and perfomance tests) are run on jenkins.

### Integration tests

The integration tests for OpenSearch are run via [integ-test](https://build.ci.opensearch.org/view/Test/job/integ-test/) job and for OpenSearch-Dashboards via [integ-test-opensearch-dashboards](https://build.ci.opensearch.org/view/Test/job/integ-test-opensearch-dashboards/) job. These jobs are mainly triggered via distribution build jobs after a distribution is created successfully. They are also triggered manually when required such as during releases or via cronjobs.
The job reads the build artifact composition from the associated manifest files and spins up parallel, independent integrationTest runs for each component built inside the artifact. For instance, if the artifact is a full distribution, which has all OpenSearch plugins, the job will kick off integration test suite for each individual plugin. Each plugin is run on an independent cluster and in independent container. After the test runs are complete, a test-report is generated using [report-workflow](https://github.com/opensearch-project/opensearch-build/tree/main/src/report_workflow). 


### Backward Comaptibility tests

The BWC tests for OpenSearch are run via [bwc-test](https://build.ci.opensearch.org/view/Test/job/bwc-test/) job and for OpenSearch-Dashboards via [bwc-test-opensearch-dashboards](https://build.ci.opensearch.org/view/Test/job/bwc-test-opensearch-dashboards/) job. These jobs that runs bwc tests on the current version and compatible bwc versions of the artifact. The core engines and respective plugins would have their backwards compatibility tests and a `bwctest.sh` which will be used to trigger the bwc tests.

### Performance test

The Performance tests for OpenSearch are run using [benchmark-test](https://build.ci.opensearch.org/view/Test/job/benchmark-test/) job. This job is triggered via cronjob for recently release, upcoming release versions of OpenSearch. See the jenkins file configutaion [here](https://github.com/opensearch-project/opensearch-build/blob/main/jenkins/opensearch/benchmark-test.jenkinsfile).
