# OpenSearch and OpenSearch Dashboards 2.19.3 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 2.19.3](https://opensearch.org/versions/opensearch-2-19-3.html) includes the following bug fixes, infrastructure, documentation and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.3.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.3.md).


## BUG FIXES


### OpenSearch Alerting


* Backports #1850, #1854, #1856 to 2.19 ([#1858](https://github.com/opensearch-project/common-utils/pull/1858))


### Opensearch Common Utils


* Validate that index patterns are not allowed in create/update doc level monitor ([#829](https://github.com/opensearch-project/common-utils/pull/829))
* Fix isDocLevelMonitor check to account for threat intel monitor ([#835](https://github.com/opensearch-project/common-utils/pull/835))
* Updating PublishFindingsRequest to use a list of findings rather than... ([#832](https://github.com/opensearch-project/common-utils/pull/832))
* Revert "updating PublishFindingsRequest to use a list of findings" ([#842](https://github.com/opensearch-project/common-utils/pull/842))


### OpenSearch Flow Framework


* Fix ApiSpecFetcher Memory Issues and Exception Handling ([#1192](https://github.com/opensearch-project/flow-framework/pull/1192))
* Better handling of Workflow Steps with Bad Request status ([#1191](https://github.com/opensearch-project/flow-framework/pull/1191))


### OpenSearch Query Insights


* Asynchronous search operations in reader ([#363](https://github.com/opensearch-project/query-insights/pull/363))


### OpenSearch Query Insights Dashboards


* [BUG FIX] Enable Correct Sorting for Metrics in Query Insights Dashboard + dependent PRs ([#201](https://github.com/opensearch-project/query-insights-dashboards/pull/201))
* [Bug Fix] Window size changing unexpectedly ([#203](https://github.com/opensearch-project/query-insights-dashboards/pull/203))
* [Fix] Ensure accurate time filtering for Top Queries in OpenSearch 2.19+ ([#249](https://github.com/opensearch-project/query-insights-dashboards/pull/249))
* Ensure accurate time filtering for Top Queries in OpenSearch 2.19 + revert [#219](https://github.com/opensearch-project/query-insights-dashboards/pull/219) ([#274](https://github.com/opensearch-project/query-insights-dashboards/pull/274))
* Search bar fix ([#277](https://github.com/opensearch-project/query-insights-dashboards/pull/277))
* [Fix] Explicitly match query by id and fix q scope in retrieveQueryById ([#269](https://github.com/opensearch-project/query-insights-dashboards/pull/269))


### OpenSearch Remote Metadata Sdk


* Make generated responses robust to URL encoded id and index values ([#156](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/156))
* Validate request fields in DDB Put and Update implementations ([#157](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/157))
* Properly handle remote client search failures with status codes ([#158](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/158))


### OpenSearch SQL


* Fix: Date field format parsing for legacy query engine ([#3160](https://github.com/opensearch-project/sql/pull/3160))


## DOCUMENTATION


## ENHANCEMENTS


## INFRASTRUCTURE


## MAINTENANCE


### Opensearch Alerting Dashboards Plugin


* Fix CVE ([#1268](https://github.com/OpenSearch-project/alerting-dashboards-plugin/pull/1268))


### Opensearch Anomaly Detection


* Migrating from commons-lang2.6 to commons-lang3.18 ([#1526](https://github.com/OpenSearch-project/anomaly-detection/pull/1526))


### Opensearch Anomaly Detection Dashboards


* Bump elliptic to 6.6.1 ([#1062](https://github.com/OpenSearch-project/anomaly-detection-dashboards-plugin/pull/1062))


### Opensearch Common Utils


* Pinned the commons-beanutils dependency to fix CVE-2025-48734 ([#850](https://github.com/opensearch-project/common-utils/pull/850))


### OpenSearch Index Management Dashboards Plugin


* Fixed CVE: babel dependencies & elliptic dependency ([#1329](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1329))


### OpenSearch ML Commons


* Force commons-beanutils to 1.11.0 ([#4000](https://github.com/opensearch-project/ml-commons/pull/4000))
* Force runtime class path commons-beanutils:commons-beanutils:1.11.0 to avoid transitive dependency ([#3935](https://github.com/opensearch-project/ml-commons/pull/3935))
* Fix commons-beanutils ([#3996](https://github.com/opensearch-project/ml-commons/pull/3996))
* Exclude commons-beanutils ([#3991](https://github.com/opensearch-project/ml-commons/pull/3991))
* Fix CVE-2025-48734 ([#3986](https://github.com/opensearch-project/ml-commons/pull/3986))
* Fix CVE-2025-48924 ([#3985](https://github.com/opensearch-project/ml-commons/pull/3985))
* Fix CVE-2025-27820 ([#3984](https://github.com/opensearch-project/ml-commons/pull/3984))
* Update the maven snapshot publish endpoint and credential ([#3955](https://github.com/opensearch-project/ml-commons/pull/3955))
* Adds Json Parsing to nested object during update Query step in ML Inference Request processor ([#3868](https://github.com/opensearch-project/ml-commons/pull/3868))


### OpenSearch Neural Search


* Use latest json-smart lib ([#1223](https://github.com/opensearch-project/neural-search/pull/1223))


### OpenSearch Performance Analyzer


* Java version bump ([#828](https://github.com/opensearch-project/performance-analyzer/pull/828))
* Spotbug version bump ([#828](https://github.com/opensearch-project/performance-analyzer/pull/828))
* Checkstyle version bump ([#828](https://github.com/opensearch-project/performance-analyzer/pull/828))


### OpenSearch Query Insights


* Fix CVE-2025-27820 and CVE-2025-48734 ([#383](https://github.com/opensearch-project/query-insights/pull/383))


### OpenSearch Query Insights Dashboards


* Increment version to 2.19.3.0 ([#207](https://github.com/opensearch-project/query-insights-dashboards/pull/207))
* Fix CVE-2024-21538 & CVE-2025-27789 on 2.19 ([#260](https://github.com/opensearch-project/query-insights-dashboards/pull/260))
* CVE-2020-28469 updated package.json and yarn.lock ([#272](https://github.com/opensearch-project/query-insights-dashboards/pull/272))


### OpenSearch Security


* Bump `com.nimbusds:nimbus-jose-jwt:9.48` from 9.48 to 10.0.2 ([#5480](https://github.com/opensearch-project/security/pull/5480))
* Bump `checkstyle` from 10.3.3 to 10.26.1 ([#5480](https://github.com/opensearch-project/security/pull/5480))


### OpenSearch SQL


* Remove unneeded dependency on commons-validator ([#3887](https://github.com/opensearch-project/sql/pull/3887))
