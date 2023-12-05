# OpenSearch and OpenSearch Dashboards 2.11.1 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 2.11.1](https://opensearch.org/versions/opensearch-2-11-1.html) includes the following bug fixes, infrastructure, enhancements, maintenance and documentation updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.11.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.11.1.md).

## BUG FIXES

### OpenSearch Cross Cluster Replication
* Fix CCR compatibility with remote translogs ([#1276](https://github.com/opensearch-project/cross-cluster-replication/pull/1276))

### OpenSearch Alerting
* Fix for ConcurrentModificationException with linkedHashmap. ([#1255](https://github.com/opensearch-project/alerting/pull/1255))

### OpenSearch Dashboards Alerting
* Removed "last updated by" sections from the UI. ( ([#767](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/767))
* Fixed bucket monitor groupBy/aggregation display bug. ([#827](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/827))

### OpenSearch Dashboards Observability
* Switch heading types on integrations setup page by @opensearch-trigger-bot in ([#1137](https://github.com/opensearch-project/dashboards-observability/pull/1137))

### OpenSearch Dashboards Query Workbench
* Add materlized views, manual refresh option and minor fixes by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/161
* Fixed create table async query bug by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/163
* Added changes for making tree view persistent, made changes for bugs for loading screen by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/167
* Support dark mode and session for sql, minor bug fixes by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/169
* Make checkpoint mandatory, add watermark delay, minor UI fixes by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/175
* UI fixes for loading state, empty tree, added toast for error, fixed no indicies error by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/178
* Session update, minor fixes for acceleration flyout by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/181
* Add backticks and remove ckpt for manual refresh in acceleration flyout by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/185
* UI-bug fixes, added create query for MV by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/188
* added fix for loading spinner issue for other database by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/192
* Fix error handling for user w/o proper permissions by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/197
* Revert commits back to after 2.11 release by @mengweieric in https://github.com/opensearch-project/dashboards-query-workbench/pull/211
* Revert "Add materlized views, manual refresh option and minor fixes (… by @mengweieric in https://github.com/opensearch-project/dashboards-query-workbench/pull/212

### OpenSearch Dashboards Reporting
* Use core navigation instead of hard coding URLs ([#229](https://github.com/opensearch-project/dashboards-reporting/pull/229)) ([#231](https://github.com/opensearch-project/dashboards-reporting/pull/231))

### OpenSearch Dashboards Security Analytics 
* Omit field from mapping payload if it matches index field; Abort detector creation when mapping has failed. ([#752](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/752))

### OpenSearch Geospatial
* Add default value in denylist ([#583](https://github.com/opensearch-project/geospatial/pull/583))
* Add denylist ip config for datasource endpoint ([#573](https://github.com/opensearch-project/geospatial/pull/573))

### OpenSearch Index Management
* Add more error notification at fail points ([#1013](https://github.com/opensearch-project/index-management/pull/1013))
* Set the rollover action to idempotent ([#1012](https://github.com/opensearch-project/index-management/pull/1012))

### OpenSearch ML Commons
* Fix multiple docs support ([#1516](https://github.com/opensearch-project/ml-commons/pull/1516))
* Support step size for embedding model which outputs less embeddings ([#1586](https://github.com/opensearch-project/ml-commons/pull/1586))
* Validate step size ([#1587](https://github.com/opensearch-project/ml-commons/pull/1587))
* Return parsing exception 400 for parsing errors ([#1603](https://github.com/opensearch-project/ml-commons/pull/1603))
* Read function Name from pretrained model ([#1529](https://github.com/opensearch-project/ml-commons/pull/1529))
* Bump json version to address CVE-2023-5072 ([#1551](https://github.com/opensearch-project/ml-commons/pull/1551))

### OpenSearch Observability
* Upgrade JSON to 20231013 to fix CVE-2023-5072 ([#1750](https://github.com/opensearch-project/observability/pull/1750))

### OpenSearch Reporting
* Upgrade JSON to 20231013 to fix CVE-2023-5072 ([#912](https://github.com/opensearch-project/reporting/pull/912))

### Opensearch Security
* Fix regression on concurrent gzipped requests ([#3599](https://github.com/opensearch-project/security/pull/3599))
* Fix issue with response content-types changed in 2.11 ([#3721](https://github.com/opensearch-project/security/pull/3721))

### OpenSearch Security Analytics
* add rollover & archival mechanism for correlation history indices ([#670](https://github.com/opensearch-project/security-analytics/pull/670))
* Return rule fields which do not have aliases ([#652](https://github.com/opensearch-project/security-analytics/pull/652))
* Fix detector writeTo() method missing fields ([#695](https://github.com/opensearch-project/security-analytics/pull/695))

## INFRASTRUCTURE

### OpenSearch Observability
* Updates demo certs used in integ tests ([#1626](https://github.com/opensearch-project/observability/pull/1626))

### OpenSearch Performance Analyzer
* Set Autopublish to true in Jenkins publish for performance-analyzer-commons repo [#45](https://github.com/opensearch-project/performance-analyzer-commons/pull/45)
* Upgrade performance-analyzer-commons version to 1.2.0 [#598](https://github.com/opensearch-project/performance-analyzer/pull/598)

### OpenSearch k-NN
* Make sure not hardcoding user name when switching to uid 1000 on CI.yml ([#1252](https://github.com/opensearch-project/k-NN/pull/1252))

## MAINTENANCE

### OpenSearch Alerting
* Increment version to 2.11.1-SNAPSHOT. ([#1274](https://github.com/opensearch-project/alerting/pull/1274))

### OpenSearch Dashboards Alerting
* Incremented version to 2.11.1. ([#788](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/788))

### OpenSearch Dashboards Query Workbench
* Design changes for loading tree elements, changed the banner, updated tests by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/172

### OpenSearch Dashboards Reporting
* Resolve traverse and debug ([#223](https://github.com/opensearch-project/dashboards-reporting/pull/223))

### OpenSearch Performance Analyzer
* Update build.gradle to use isSnapshot logic [#521](https://github.com/opensearch-project/performance-analyzer-rca/pull/521)
* Add separate metric for cluster manager service events and metrics [#579](https://github.com/opensearch-project/performance-analyzer/pull/579)
* Add separate metric in commons repo for cluster manager service events and metrics [#51](https://github.com/opensearch-project/performance-analyzer-commons/pull/51)

### OpenSearch Reporting
* Increment version to 2.11.1-SNAPSHOT ([#923](https://github.com/opensearch-project/reporting/pull/923))

### OpenSearch Dashboards Security Analytics
* Increment version to 2.11.1.0. ([#771](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/771))

## DOCUMENTATION

### OpenSearch Dashboards Alerting
* Add 2.11.1 release notes. ([#828](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/828))

### OpenSearch Alerting
* Added 2.11.1 release notes. ([#1306](https://github.com/opensearch-project/alerting/pull/1306))

### OpenSearch Index Management
* Increment version to 2.11.1-SNAPSHOT. ([#1016](https://github.com/opensearch-project/index-management/pull/1016))

### OpenSearch Security Analytics
* Added 2.11.1 release notes.([#727](https://github.com/opensearch-project/security-analytics/pull/727))

### OpenSearch Dashboards Security Analytics 
* Added release notes for 2.11.1 ([#785](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/785))
