- [Orchestrator](#orchestrator)
  - [Input parameters](#input-parameters)

### Orchestrator

This is a jenkins pipeline that kicks off all long running test jobs on a given build artifact. It kicks off `integ-test`, `bwc-test`, `perf-test` jobs in parallel and notifies the designated channels when the workflow finishes.

This is a work in progress. Currently `integ-test` is the only completed and working test job as part of [#1429](https://github.com/opensearch-project/opensearch-build/pull/1429).
 
#### Input parameters

| name               | description                |
| ------------------ | -------------------------- |
| TEST_MANIFEST      | File path to test manifest |
| BUILD_MANIFEST_URL | URL to dist build manifest |

