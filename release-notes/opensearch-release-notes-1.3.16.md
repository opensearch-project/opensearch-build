# OpenSearch and OpenSearch Dashboards 1.3.16 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.16](https://opensearch.org/versions/opensearch-1-3-16.html) includes the following bug fixes, documentation and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.16.md).

## BUG FIXES


### OpenSearch Security


* Allow TransportConfigUpdateAction when security config initialization has completed ([#4115](https://github.com/opensearch-project/security/pull/4115))


### OpenSearch Security Dashboards Plugin


* Split up a value into multiple cookie payloads ([#1831](https://github.com/opensearch-project/security-dashboards-plugin/pull/1831))


## DOCUMENTATION


### OpenSearch Index Management


* Version 1.3.16 release notes ([#1156](https://github.com/opensearch-project/index-management/pull/1156))


## MAINTENANCE


### OpenSearch Index Management


* Increment version to 1.3.16 ([#1131](https://github.com/opensearch-project/index-management/pull/1131))
* Force resolve logback deps to mitigate CVE-2023-6378 ([#1125](https://github.com/opensearch-project/index-management/pull/1125))


### OpenSearch Performance Analyzer


* Bump netty to match version from core's buildSrc/version.properties and bump grpc to 1.56.1 ([#546](https://github.com/opensearch-project/performance-analyzer-rca/pull/546))


### OpenSearch Reporting


* Upgrade JSON to 20231013 to fix CVE-2023-5072 ([#986](https://github.com/opensearch-project/reporting/pull/986))


### OpenSearch Security


* Force resolution of org.apache.zookeeper:zookeeper to 3.9.2 and org.bitbucket.b\_c:jose4j to 0.9.4 ([#4136](https://github.com/opensearch-project/security/pull/4136))
* Integration Tests for Security Config Initialization ([#4134](https://github.com/opensearch-project/security/pull/4134))
* Remove and refactor console print statements ([#4206](https://github.com/opensearch-project/security/pull/4206))


