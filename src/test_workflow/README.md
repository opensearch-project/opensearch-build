- [Testing a Distribution](#testing-a-distribution)
  - [Test.sh Options](#testsh-options)
  - [Integration Tests](#integration-tests)
  - [Backwards Compatibility Tests](#backwards-compatibility-tests)
  - [Performance Tests](#performance-tests)
    - [Identifying Regressions in Performance Tests](#identifying-regressions-in-performance-tests)
      - [Identifying Regressions in Nightly Performance Tests](#identifying-regressions-in-nightly-performance-tests)
    - [Identifying Issues in Longevity Tests](#identifying-issues-in-longevity-tests)
- [Testing in CI/CD](#testing-in-cicd)
  - [Test Workflow (in development)](#test-workflow-in-development)
  - [Component-Level Details](#component-level-details)
    - [test-orchestrator pipeline](#test-orchestrator-pipeline)
    - [integTest job](#integtest-job)
    - [bwcTest job](#bwctest-job)
    - [perfTest job](#perftest-job)
- [Manifest Files](#manifest-files)
- [Dependency Management](#dependency-management)
- [S3 Permission Model](#s3-permission-model)
- [Appendix](#appendix)

## Testing a Distribution

Testing is run via `./test.sh`.

### Test.sh Options

The following options are available.

| name                   | description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| test-type              | Run tests of a test suite. [integ-test, bwc-test, perf-test]            |
| test-manifest-path     | Specify a test manifest path.                                           |
| --paths                | Location of manifest(s).                                                |
| --test-run-id          | Unique identifier for a test run.                                       |
| --component [name ...] | Test a subset of specific components.                                   |
| --keep                 | Do not delete the temporary working directory on both success or error. |
| -v, --verbose          | Show more verbose output.                                               |

### Integration Tests

Runs integration tests invoking `run_integ_test.py` in each component from distribution manifest.

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

TODO: Add instructions for running performance tests with `test.sh`


Performance tests from `test.sh` are executed using an internal service which automatically provisions hosts that run [OpenSearch Benchmark](https://github.com/opensearch-project/OpenSearch-Benchmark). Work to open source these internal features is being tracked in [opensearch-benchmark#97](https://github.com/opensearch-project/opensearch-benchmark/issues/97).

Comparable performance data can be generated by directly using OpenSearch Benchmark, assuming that the same cluster and workload setups are used. More details on the performance testing configuration used for the nightly runs can be found in [OpenSearch#2461](https://github.com/opensearch-project/OpenSearch/issues/2461).

In addition to the standard performance tests that run on the order of hours, longevity tests are run which load to a cluster for days or weeks. These tests are meant to validate cluster stability over a longer timeframe.
Longevity tests are also executed using OpenSearch Benchmark, using a modified version of the [nyc_taxis workload](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/nyc_taxis) that repeats the schedule for hundreds of iterations.

#### Identifying Regressions in Performance Tests

Before trying to identify a performance regression a set of baseline tests should be run, in order to establish expected values for performance metrics and to understand the variance between tests for the same configuration. Performance regressions are primarily determined based on decreased indexing throughput and/or increased query latency. 
There is some amount of variance expected between any two tests. Empirically it has been found that generally tests for the same configuration can differ by about 5% of the mean for average indexing throughput and by about 10% of the mean for p90 or p99 query latency. Note that these values may vary depending on the underlying hardware of the cluster and the workload being used. 

If performance metrics for a certain testing configuration consistently fall outside the range created by the expected value for a metric +/- the standard deviation for the metric in the baseline tests then there is likely a performance regression. 

The nightly performance runs use the nyc_taxis workload with 2 warmup and 3 test iterations; tests using this configuration can also use the particular values defined in [this section](#identifying-regressions-in-nightly-performance-tests) for identifying performance regression.

Additionally, error rates can be indicative of a performance regression. Error rates on the order of 0.01% are acceptable, though higher values are cause for concern. High error rates may point to issues with cluster availability or a change in the logic for processing a specific operation. 
For tests using OpenSearch Benchmark with an external OpenSearch cluster configured as the data store, more details on the cause of the errors can be found by searching for the test execution ID in the `benchmark-metrics-*` index of the metrics data store.


##### Identifying Regressions in Nightly Performance Tests

Using the aggregate results from the nightly performance test runs, compare indexing and query metrics to the specifications laid out in the table below. 
The data for this table came from tests using OpenSearch 1.2 build #762 ([arm64](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.2.4/762/linux/arm64/dist/opensearch/manifest.yml
)/[x64](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.2.4/762/linux/x64/dist/opensearch/manifest.yml)), more details on the test setup can be found in [OpenSearch#2461](https://github.com/opensearch-project/OpenSearch/issues/2461).

Please keep in mind the following:

1. Changing the number of iterations or the workload type for a test can drastically change performance characteristics. This table is not necessarily applicable to other workload configurations.
2. StDev% Mean is the standard deviation as a percentage of the mean. It is expected that metrics for a test will be +/- this value relative to the expected value. If the average of several tests consistently falls outside this bound relative to the expected value there may be a performance regression (or improvement). 
3. MinMax% Diff is the worst case variance between any two tests with the same configuration. If there is a difference greater than this value than there is likely a performance regression or an issue with the test setup. In general, comparing one off test runs should be avoided if possible.


|Instance Type|Security|Expected Indexing Throughput Avg (req/s)|Expected Indexing Error Rate|Indexing StDev% Mean|Indexing MinMax% Diff|Expected Query Latency p90 (ms)|Expected Query Latency p99 (ms)|Expected Query Error Rate|Query StDev% Mean|Query MinMax% Diff|
|---|---|---|---|---|---|---|---|---|---|---|
|m5.xlarge|Enabled|30554|0|~5%|~12%|431|449|0|~10%|~23%|
|m5.xlarge|Disabled|34472|0|~5%|~15%|418|444|0|~10%|~25%|
|m6g.xlarge|Enabled|38625|0|~3%|~8%|497|512|0|~8%|~23|
|m6g.xlarge|Disabled|45447|0|~2%|~3%|470|480|0|~5%|~15%|

#### Identifying Issues in Longevity Tests
 
Longevity tests are long running performance tests meant to measure the stability of a cluster over the course of several days or weeks.
Internal tools provide dashboards for monitoring cluster behavior during these tests. Use the following steps to spot issues in automated longevity tests:

1. Navigate to the Jenkins build for a longevity test. 
2. In the Console Output search for ``` INFO:root:Test can be monitored on <link>```
3. Navigate to that link then click the link for "Live Dashboards"
4. Use the table below to monitor metrics for the test:

|Metric|Health Indicators / Expected Values|Requires investigations / Cause for concerns|
|---|---|---|
|Memory|saw tooth graph|upward trends|
|CPU| |upward trends or rising towards 100%|
|Threadpool|0 rejections|any rejections|
|Indexing Throughput|Consistent rate during each test iteration|downward trends|
|Query Throughput|Varies based on the query being issued|downward trends between iterations|
|Indexing Latency|Consistent during each test iteration|upward trends|
|Query Latency|Varies based on the query being issued|upward trends|

## Testing in CI/CD

The CI/CD infrastructure is divided into two main workflows - `build` and `test`. The `build` workflow automates the process to generate all OpenSearch and OpenSearch Dashboards artifacts, and provide them as distributions to the `test` workflow, which runs exhaustive testing on the artifacts based on the artifact type. The next section talks in detail about the test workflow.

### Test Workflow (in development)

The test workflow development is in progress. To see a previously-unfinished prototype design, see [#609](https://github.com/opensearch-project/opensearch-build/pull/609).

The progress of this design is tracked in meta issue [#123](https://github.com/opensearch-project/opensearch-build/issues/123).

### Component-Level Details

#### test-orchestrator pipeline

This pipeline is in development. To see a previously-unfinished prototype design, see [#423](https://github.com/opensearch-project/opensearch-build/pull/423), [#523](https://github.com/opensearch-project/opensearch-build/pull/523).

The development of `test-orchestration-pipeline` is tracked by meta issue [#123](https://github.com/opensearch-project/opensearch-build/issues/123) 

#### integTest job

It is a Jenkins job that runs integration tests on a build artifact. It reads the build artifact composition from the associated manifest files and spins up parallel, independent integrationTest runs for each component built inside the artifact. For instance, if the artifact is a full distribution, which has all OpenSearch plugins, the job will kick off integration test suite for each individual plugin. Each plugin integration tests would run against a dedicated single node cluster, which is created from the built artifact. Once all integration tests complete, this job publishes the test results to an S3 bucket.

See the integration test [configuration file](jenkins/opensearch/integ-test.jenkinsfile) and related [jenkins job](https://build.ci.opensearch.org/job/integ-test/)

The development of `integTest` job is tracked by meta issue [#818](https://github.com/opensearch-project/opensearch-build/issues/818)

#### bwcTest job 

It is a Jenkins job that runs bwc tests on the current version and compatible bwc versions of the artifact. OpenSearch core and each plugin would have their backwards compatibility tests and a `bwctest.sh` which will be used to trigger the bwc tests. Currently, only core and anomaly-detection bwc tests run and the other plugins can be added once they have their bwc tests ready. For example, for anomaly-detection, the job currently runs bwc tests for current version 1.1.0.0 and bwc version 1.13.0.0.

When the bwc test is triggered for a particular component, the tests set up their own cluster and test the required functionalities in the upgrade paths, for the example above, a multi-node cluster starts with bwc versions of OpenSearch and AD installed on it, one or more nodes are upgraded to the current version of OpenSearch and AD installed on it and backwards compatibility is tested. The plugins would add tests for all bwc versions (similar to OpenSearch core) and they can be triggered from the bwcTest job.

See the bwc test [configuration file](jenkins/opensearch/bwc-test.jenkinsfile) and related [jenkins job](https://build.ci.opensearch.org/job/bwc-test/)

The development of the bwc test automation is tracked by meta issue [#90](https://github.com/opensearch-project/opensearch-build/issues/90).

#### perfTest job

It is a Jenkins job that runs performance tests on the bundled artifact using [OpenSearch Benchmark](https://github.com/opensearch-project/OpenSearch-Benchmark) (Mensor). It reads the bundle-manifest, config files and spins up a remote cluster with the bundled artifact installed on it. It will run performance test with and without security for specified architecture of the opensearch bundle. The job will kick off the single node cdk that sets up a remote cluster. It will then run the performance tests on those cluster using the mensor APIs from the whitelisted account and remote cluster endpoint(accessible to mensor system). These tests are bundle level tests. Any plugin on-boarding does not need to be a separate process. If the plugin is a part of the bundle, it is already onboarded. 

Once the performance tests completes (usually takes 5-8 hours for nyc_taxis track), it will report the test results and publish a human readable report in S3 bucket.

See the performance test [configuration file](jenkins/opensearch/perf-test.jenkinsfile) and related [jenkins job](https://build.ci.opensearch.org/job/perf-test/)

You can download the test results report using below url:

```
https://ci.opensearch.org/ci/dbc/perf-test/<version>/<distribution-build-number>/linux/x64/tar/test-results/<job-build-number>/perf-test/<with/without-security>/perf-test.html
```
You can download the json format for above results using same url and replacing `.html` with `.json`

Example:
https://ci.opensearch.org/ci/dbc/perf-test/1.3.6/6041/linux/x64/tar/test-results/678/perf-test/without-security/perf-test.html

_Note: The without security test results might be not present for distribution that lacks the security plugin. As of now we only run performance tests on tarballs._

Conversion of Performance Test results to HTML file and JSON file:

The result conversion of the perf-test is as follows-
After the performance test completes, it will report back the test results as well as the test-id. The results here will be in JSON format where they are converted into a tabular HTML string using a template library which is json2html. They will be then written to a HTML file where the file-name’s format is in <test-id>.html. Along with generating a HTML file, a JSON file having the raw JSON data will also be generated whose filename’s format is in <test-id>.json. The reason for creating a JSON file is to give the user the option to view both the JSON data in tabular format in the HTML file and the raw JSON data in the JSON file. The .html as well as .json file generated, will be stored in the path given by the user during the test-suite flow as a command-line args. These will be then taken and published in the S3 bucket.   

The development is tracked by meta issue [#126](https://github.com/opensearch-project/opensearch-build/issues/126)

## Manifest Files

Manifest files are configurations for a particular bundle. `test-workflow` uses three types of manifest files to run test suites. 

1. `test-manifest.yml` provides a list of test configurations to run against a given component in the bundle. An example of a configuration would be, integration test `index-management` plugin `with-security` and `without-security`. This manifest file serves as a support matrix config for the testing and should be updated by plugins if new components or test suites are to be added as part of the release workflow. See [here](manifests/1.3.0/opensearch-1.3.0-test.yml)
2. `build-manifest.yml` created by the build-workflow and provides a list of artifacts built as part of the build-workflow. It assists `test-workflow` pull the maven and build dependencies to run the test suites.
3. `bundle-manfest.yml` created by the build-workflow and provides a list of components packaged in a given bundle.  It assists `test-workflow` to identify what components should be tested for a given bundle.

## Dependency Management 

This section talks about how the `test-workflow` gets the dependencies required by plugins for running integration test suite (and will be extended to backward compatibility in future). There are two types of dependencies - 

1. `maven` - maven artifacts required by plugins
2. `build` - assembled zip artifacts required by plugins, e.g. job-scheduler zip required by index-management plugin.

Plugins depend on a bunch of maven artifacts to successfully run integration tests. Normally the plugin build system pulls these maven artifacts from maven central repository. However, when testing on unreleased candidates, these maven dependencies are not yet available in maven central repo. 

In order to get around this issue, the instrumentation logic in `test-workflow` provides these dependencies into maven local repo, before kicking off the integration test for plugins. The test workflow installs these maven dependencies from the s3 bucket where the build-workflow publishes them during bundle creation phase. Once these dependencies are available in maven local, the plugin build system can use them to run integration tests.

Similarly, some plugins have dependency on other plugins and require their zip artifacts for running integration tests. Example, `index-management` requires `job-scheduler zip` artifacts. These are referred to as build dependencies and are made available by the `test-workflow` to the plugins before the test is started. 

## S3 Permission Model

This section defines how the permissions are configured for reading bundle, tarball, maven dependencies etc. from S3 and writing the results log back to s3 once the tests complete.

The Jenkins infrastructure is setup in an AWS account via cdk. The account provides a `test-orchestrator-role` with permission policy to read and write from s3, see [[1] test-orchestrator-role policy](#appendix) . The `instance-profile` role has `assume-role` permissions on this `test-orchestrator role` which allows the jenkins instance to read and write from required s3 locations.

## Appendix

[1] test-orchestrator-role policy 

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "<S3 bucket arn>"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "<S3 bucker arn>/builds/*"
            ]
        },
        {
            "Action": "s3:GetObject",
            "Resource": [
            "<S3 bucket arn>/bundles/*"
            ],
            "Effect": "Allow"
        },
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "<S3 bucket arn>/bundles/*/tests/*"
        }
    ]
}
```
