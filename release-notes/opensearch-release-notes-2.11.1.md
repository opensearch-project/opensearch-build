# OpenSearch and OpenSearch Dashboards 2.11.1 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 2.11.1](https://opensearch.org/versions/opensearch-2.11.1.html) includes the following bug fixes, infrastructure, enhancements, maintenance and documentation updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.11.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.11.1.md).

## BUG FIXES

### Cross-Cluster-Replication
* Fix CCR compatibility with remote translogs ([#1276](https://github.com/opensearch-project/cross-cluster-replication/pull/1276))

### OpenSearch Alerting
* Fix for ConcurrentModificationException with linkedHashmap. ([#1255](https://github.com/opensearch-project/alerting/pull/1255))

### OpenSearch Alerting Dashboards
* Removed "last updated by" sections from the UI. ( ([#767](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/767))
* Fixed bucket monitor groupBy/aggregation display bug. ([#827](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/827))

### OpenSearch Dashboards Observability
* Fix for explorer data grid not paginating by @opensearch-trigger-bot in ([#1141](https://github.com/opensearch-project/dashboards-observability/pull/1141)
* Allow patch on allowedRoles by @opensearch-trigger-bot in ([#1145](https://github.com/opensearch-project/dashboards-observability/pull/1145)
* Update URL of create datasources, fix spacing by @opensearch-trigger-bot in ([#1154](([#1154](https://github.com/opensearch-project/dashboards-observability/pull/1154))
* Disable integration set up button if invalid by @opensearch-trigger-bot in ([#1161](https://github.com/opensearch-project/dashboards-observability/pull/1161)
* Switch from toast to callout for integration set up failures by @opensearch-trigger-bot in ([#1159](https://github.com/opensearch-project/dashboards-observability/pull/1159)
* Remove loading progress for integration setup by @opensearch-trigger-bot in ([#1162](https://github.com/opensearch-project/dashboards-observability/pull/1162)
* Fix integration labeling to identify S3 integrations by @opensearch-trigger-bot in ([#1164](https://github.com/opensearch-project/dashboards-observability/pull/1164)
* Quiet react-dnd draggableId/droppableId warnings. by @opensearch-trigger-bot in ([#1166](https://github.com/opensearch-project/dashboards-observability/pull/1166)
* Fix events home table and toast life time by @kavithacm in ([#1170](https://github.com/opensearch-project/dashboards-observability/pull/1170)
* Fixed Visualization Config Panel dark mode by @opensearch-trigger-bot in ([#1176](https://github.com/opensearch-project/dashboards-observability/pull/1176)
* Bug fixes for observability count distribution and application analytics by @opensearch-trigger-bot in ([#1189](https://github.com/opensearch-project/dashboards-observability/pull/1189)
* Correct query schema for ELB mview generation by @opensearch-trigger-bot in ([#1199](https://github.com/opensearch-project/dashboards-observability/pull/1199)
* [Explorer] Fixes for cancel button and saved object loading by @opensearch-trigger-bot in ([#1201](https://github.com/opensearch-project/dashboards-observability/pull/1201)
* Saved object datasource backward compatibility fixes by @opensearch-trigger-bot in ([#1210](https://github.com/opensearch-project/dashboards-observability/pull/1210)
* disabling inspect and default pattern/timestamp buttons when using async data sources by @opensearch-trigger-bot in ([#1212](https://github.com/opensearch-project/dashboards-observability/pull/1212)

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
* Fix for doc level query constructor change ([#651](https://github.com/opensearch-project/security-analytics/pull/651))
* Return rule fields which do not have aliases ([#652](https://github.com/opensearch-project/security-analytics/pull/652))
* Fix detector writeTo() method missing fields ([#695](https://github.com/opensearch-project/security-analytics/pull/695))

## ENHANCEMENTS

### OpenSearch Geospatial
* Add default value in denylist ([#583](https://github.com/opensearch-project/geospatial/pull/583))
* Add denylist ip config for datasource endpoint ([#573](https://github.com/opensearch-project/geospatial/pull/573))

### OpenSearch Security Analytics
* Add rollover & archival mechanism for correlation history indices ([#670](https://github.com/opensearch-project/security-analytics/pull/670))

### OpenSearch Security Analytics-Dashboards
* Omit field from mapping payload if it matches index field; Abort detector creation when mapping has failed. ([#752](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/752))

## FEATURES

### OpenSearch Common Utils
* Adds fields param in toxcontent() for doc level query ([#549](https://github.com/opensearch-project/common-utils/pull/549))
* Adds 'fields' parameter in doc level query object ([#546](https://github.com/opensearch-project/common-utils/pull/546))
Footer

## INFRASTRUCTURE

### OpenSearch Observability
* Updates demo certs used in integ tests ([#1626](https://github.com/opensearch-project/observability/pull/1626))

### OpenSearch Performance Analyzer
* Set Autopublish to true in Jenkins publish for performance-analyzer-commons repo [#45](https://github.com/opensearch-project/performance-analyzer-commons/pull/45)
Member
* Upgrade performance-analyzer-commons version to 1.2.0 [#598](https://github.com/opensearch-project/performance-analyzer/pull/598)

### OpenSearch k-NN
* Make sure not hardcoding user name when switching to uid 1000 on CI.yml ([#1252](https://github.com/opensearch-project/k-NN/pull/1252))

## MAINTENANCE

### OpenSearch Alerting
* Increment version to 2.11.1-SNAPSHOT. ([#1274](https://github.com/opensearch-project/alerting/pull/1274))

### OpenSearch Alerting Dashboards
* Incremented version to 2.11.1. ([#788](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/788))

### OpenSearch Dashboards Observability
* Switch heading types on integrations setup page by @opensearch-trigger-bot in ([#1137](https://github.com/opensearch-project/dashboards-observability/pull/1137)
* Remove husky pre-commit checks (#1192) by @ps48 in ([#1193](https://github.com/opensearch-project/dashboards-observability/pull/1193)
* Revert commits back to after 2.11 release by @mengweieric in ([#1231](https://github.com/opensearch-project/dashboards-observability/pull/1231)

### OpenSearch Dashboards Query Workbench
* Design changes for loading tree elements, changed the banner, updated tests by @opensearch-trigger-bot in https://github.com/opensearch-project/dashboards-query-workbench/pull/172

### OpenSearch Dashboards Reporting
* Resolve traverse and debug ([#223](https://github.com/opensearch-project/dashboards-reporting/pull/223))

### OpenSearch Performance Analyzer
* Update build.gradle to use isSnapshot logic [#521](https://github.com/opensearch-project/performance-analyzer-rca/pull/521)
* Add separate metric for cluster manager service events and metrics [#579](https://github.com/opensearch-project/performance-analyzer/pull/579)
* Add separate metric in commons repo for cluster manager service events and metrics [#51](https://github.com/opensearch-project/performance-analyzer-commons/pull/51)
Member

### OpenSearch Reporting
* Increment version to 2.11.1-SNAPSHOT ([#923](https://github.com/opensearch-project/reporting/pull/923))

### OpenSearch Security Analytics-Dashboards
* Increment version to 2.11.1.0. ([#771](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/771))

## REFACTORING

### OpenSearch Alerting
* Handle Doc level query 'fields' param for query string query. ([#1240](https://github.com/opensearch-project/alerting/pull/1240))
* Add nested fields param mapping findings index for doc level queries. ([#1276](https://github.com/opensearch-project/alerting/pull/1276))

### OpenSearch Dashboards Observability
* [Explorer] Modify text in empty prompt by @opensearch-trigger-bot in ([#1182](https://github.com/opensearch-project/dashboards-observability/pull/1182)
* [Explorer] Supports session for s3 direct query by @opensearch-trigger-bot in ([#1183](https://github.com/opensearch-project/dashboards-observability/pull/1183)
* Support cancellation of async queries by @opensearch-trigger-bot in ([#1186](https://github.com/opensearch-project/dashboards-observability/pull/1186)
* Add integrations queries for Flint by @opensearch-trigger-bot in ([#1195](https://github.com/opensearch-project/dashboards-observability/pull/1195)
* Link integrations from datasources UI by @opensearch-trigger-bot in ([#1207](https://github.com/opensearch-project/dashboards-observability/pull/1207)
* Add S3 integration for Nginx and VPC by @opensearch-trigger-bot in ([#1216](https://github.com/opensearch-project/dashboards-observability/pull/1216)
* Update empty allowed roles to admin only by @opensearch-trigger-bot in ([#1220](https://github.com/opensearch-project/dashboards-observability/pull/1220)

## DOCUMENTATION

### OpenSearch Alerting Dashboards
* Added 2.11.1 release notes. ([#1306](https://github.com/opensearch-project/alerting/pull/1306))

### OpenSearch Dashboards Observability
* Add 2.11.1 release notes. ([#828](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/828))

### OpenSearch Index Management
* Increment version to 2.11.1-SNAPSHOT. ([#1016](https://github.com/opensearch-project/index-management/pull/1016))

### OpenSearch Security Analytics
* Added 2.11.1 release notes.([#727](https://github.com/opensearch-project/security-analytics/pull/727))

### OpenSearch Security Analytics-Dashboards
* Added release notes for 2.11.1 ([#785](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/785))
