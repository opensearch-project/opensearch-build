# OpenSearch and OpenSearch Dashboards 2.19.1 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 2.19.1](https://opensearch.org/versions/opensearch-2-19-1.html) includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.1.md).


## BUG FIXES


### Opensearch Job Scheduler


* Only download demo certs when integTest run with `-Dsecurity.enabled=true` ([#737](https://github.com/opensearch-project/job-scheduler/pull/737)) ([#740](https://github.com/opensearch-project/job-scheduler/pull/740)).


### Opensearch ML Commons


* Fix ignoreFailure flag in ml inference search processors ([#3570](https://github.com/opensearch-project/ml-commons/pull/3570))
* Updating bulk update to use sdkclient ([#3546](https://github.com/opensearch-project/ml-commons/pull/3546))
* Add interface for no postprocessing function case ([#3553](https://github.com/opensearch-project/ml-commons/pull/3553))
* Add edge case for models that are marked as not found in cache ([#3523](https://github.com/opensearch-project/ml-commons/pull/3523))
* Applying sdkclient changes to config index ([#3521](https://github.com/opensearch-project/ml-commons/pull/3521))
* Remainig sdk client changes for search ([#3522](https://github.com/opensearch-project/ml-commons/pull/3522))
* Adding tenantId for inline connector in model registration ([#3531](https://github.com/opensearch-project/ml-commons/pull/3531))
* Remove the integ test case cause cohere classify is deprecated in its llm service ([#3513](https://github.com/opensearch-project/ml-commons/pull/3513))
* Fix null decrypted credential while getting batch predict job status ([#3518](https://github.com/opensearch-project/ml-commons/pull/3518))


### Opensearch Observability


* Bump logback to 1.5.16 ([#1074](https://github.com/opensearch-project/reporting/pull/1074))


### Opensearch Query Insights Dashboards


* Fix buggy grouping cypress tests ([#106](https://github.com/opensearch-project/query-insights-dashboards/pull/106))
* Fix: Query Insights Dashboards style integration - Group Query Details ([#70](https://github.com/opensearch-project/query-insights-dashboards/pull/70))
* Fix: Query Insights Dashboards style integration - Configuration Page ([#68](https://github.com/opensearch-project/query-insights-dashboards/pull/68))
* Fix: Query Insights Dashboards style integration - QueryDetails ([#69](https://github.com/opensearch-project/query-insights-dashboards/pull/69))


### Opensearch Remote Metadata SDK


* Improve exception unwrapping flexibility for SdkClientUtils
* Add util methods to handle ActionListeners in whenComplete
* Refactor SDKClientUtil for better readability, fix javadocs
* Make DynamoDBClient fully async


### Opensearch Reporting


* Bump logback to 1.5.16 ([#1905](https://github.com/opensearch-project/observability/pull/1905))


### Opensearch Security


* Fix ssl hot reload settings ([#5117](https://github.com/opensearch-project/security/pull/5117))


## DOCUMENTATION


### Opensearch Alerting


* Added 2.19.1.0 release notes. ([#804](https://github.com/opensearch-project/common-utils/pull/1804))


### Opensearch Common Utils


* Added 2.19.1.0 release notes. ([#797](https://github.com/opensearch-project/common-utils/pull/797))


### Opensearch Query Insights Dashboards


* 2.19.1 Release Notes ([#119](https://github.com/opensearch-project/query-insights-dashboards/pull/119))


### Opensearch Security Analytics


* Added 2.19.1 release notes. ([#1489](https://github.com/opensearch-project/security-analytics/pull/1489))


## MAINTENANCE


### Dashboards Assistant


* Increment version to 2.19.1.0([#451](https://github.com/opensearch-project/dashboards-assistant/pull/451))


* Remove dompurify and use dompurify 3.2.4 from OSD ([#469](https://github.com/opensearch-project/dashboards-assistant/pull/469))([#465](https://github.com/opensearch-project/dashboards-assistant/pull/465))


### Opensearch Alerting


* Increment version to 2.19.1-SNAPSHOT ([#1797](https://github.com/opensearch-project/common-utils/pull/1797))
* Upgrade logback to 1.5.16 ([#1802](https://github.com/opensearch-project/common-utils/pull/1802))


### Opensearch Asynchronous Search


* Increment version to 2.19.1 ([#706](https://github.com/opensearch-project/asynchronous-search/pull/706))
* Remove unused compile time dependency `transport-netty4-client` ([#710](https://github.com/opensearch-project/asynchronous-search/pull/710))


### Opensearch Common Utils


* Increment version to 2.19.1-SNAPSHOT ([#792](https://github.com/opensearch-project/common-utils/pull/792))
* Upgrade logback to 1.5.16 and Cron Utils to 9.1.8 ([#796](https://github.com/opensearch-project/common-utils/pull/796))


### Opensearch Dashboards Reporting


* Bump jspdf to 3.0 to fix CVE-2025-26791 ([#530](https://github.com/opensearch-project/dashboards-reporting/pull/530))


### Opensearch Index Management


* CVE fix - Bump logback to 1.5.16 ([#1383](https://github.com/opensearch-project/index-management/pull/1383/files))


### Opensearch Index Management Dashboards Plugin


* Upgrade Micromatch to new version ([#1277](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1277))


### Opensearch Job Scheduler


* Increment version to 2.19.1 [#732](https://github.com/opensearch-project/job-scheduler/pull/732).


### Opensearch Remote Metadata SDK


* Fix CVE-2025-24970 ([93](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/93))


### Opensearch Security Analytics


* Incremented version to 2.19.1 ([#1480](https://github.com/opensearch-project/security-analytics/pull/1480))
* Updated commons jar to fix CVE-2025-24970, and CVE-2025-25193. ([#1484](https://github.com/opensearch-project/security-analytics/pull/1484))


