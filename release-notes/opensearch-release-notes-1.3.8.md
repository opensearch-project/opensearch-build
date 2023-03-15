# OpenSearch and OpenSearch Dashboards 1.3.8 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.8](https://opensearch.org/versions/opensearch-1-3-8.html) includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.8.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.8.md).

## FEATURE

### OpenSearch Performance Analyzer
* Enhance the cluster config fields for PA([#342](https://github.com/opensearch-project/performance-analyzer/pull/342))

## ENHANCEMENTS

### OpenSearch Security
* Username validation for special characters ([#2277](https://github.com/opensearch-project/security/pull/2277))
* Tool scripts are updated to run on Windows ([#2371](https://github.com/opensearch-project/security/pull/2371))
* Exclude the term + .keyword when excluding fields ([2375](https://github.com/opensearch-project/security/pull/2375))

## BUG FIXES

### OpenSearch Anomaly Detection
* Fixed DLS/FLS logic around numeric aggregations ([#789](https://github.com/opensearch-project/anomaly-detection/pull/789))

## INFRASTRUCTURE

### OpenSearch Anomaly Detection
* Added Windows and Mac CI to 1.3 ([#745](https://github.com/opensearch-project/anomaly-detection/pull/745))

## MAINTENANCE

### OpenSearch Security Dashboards Plugin
* Upgrade loader-utils to 2.0.4, glob-parent to 6.0.0 and decode-uri-component to 0.2.2([#1308](https://github.com/opensearch-project/security-dashboards-plugin/pull/1308))

### OpenSearch Security
* Update cxf-core to 3.5.5 ([#2349](https://github.com/opensearch-project/security/pull/2349))

### OpenSearch Performance Analyzer
* Upgrade guava, protobuf minor versions. ([#374](https://github.com/opensearch-project/performance-analyzer/pull/374))

## DOCUMENTATION

### OpenSearch Performance Analyzer
* Added MAINTAINERS.md file. ([#359](https://github.com/opensearch-project/performance-analyzer/pull/359))
