#### Generate test-report manifest for each test.
The input requires a mandatory `test-manifest-path`, `--artifact-paths`, `--base-path`, `--test-type` and `--test-run-id`, optional `--output-path` and `--component` to automatically generate the test-report manifest after testing.

*Usage*
```
./report.sh <test-manifest-path> --artifact-paths opensearch=<...> opensearch-dashboards=<...> --test-run-id <...> --test-type integ-test --base-path <...>
```
e.g.
```
./report.sh manifests/2.9.0/opensearch-2.9.0-test.yml -p opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.9.0/8172/linux/x64/tar --test-run-id 5328 --test-type integ-test --base-path https://ci.opensearch.org/ci/dbc/integ-test/2.9.0/8172/linux/x64/tar
```
The following options are available.

| name                            | description                                                                    |
|---------------------------------|--------------------------------------------------------------------------------|
| test-manifest-path   <required> | Specify a test manifest path.                                                  |
| -p, --artifact-paths <required> | Artifact paths of distributions used for testing.                              |
| --base-path          <required> | Base paths of testing logs.                                                    |
| --test-type          <required> | Type of tests report generates on.                                             |
| --output-path        <optional> | Specify the path location for the test-report manifest.                        |
| --test-run-id        <required> | Specify the unique execution id for the test.                                  |
| --component          <optional> | Specify a specific component or components instead of the entire distribution. |
| --verbose            <optional> | Show more verbose output.                                                      |

