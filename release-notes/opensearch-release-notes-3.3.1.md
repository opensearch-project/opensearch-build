# OpenSearch 3.3.1 and OpenSearch Dashboards 3.3.0 Release Notes

## Release Highlights
Fixes OpenSearch Core Engine backward compatibility handling of date fields while maintaining performance optimizations. The `skip_list` parameter is now automatically set to `true` for new `@timestamp` fields created since 3.3.0, while preserving `skip_list=false` for existing indexes with `@timestamp` or index sort date fields. This approach ensures date histogram aggregation performance benefits for new indexes while maintaining compatibility with existing workloads.

## Release Details
[OpenSearch 3.3.1](https://opensearch.org/artifacts/by-version/#release-3-3-1) includes the following bug fix updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.3.1.md).

## Bug Fixes

### OpenSearch

* Fix issue with updating core with a patch number other than 0 ([#19377](https://github.com/opensearch-project/OpenSearch/pull/19377))
* [Star Tree] Fix sub-aggregator casting for search with profile=true ([#19652](https://github.com/opensearch-project/OpenSearch/pull/19652))
* Fix bwc @timestamp upgrade issue by adding a version check on skip_list param ([#19671](https://github.com/opensearch-project/OpenSearch/pull/19671))
