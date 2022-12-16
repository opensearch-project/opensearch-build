# OpenSearch and OpenSearch Dashboards 2.4.1 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.4.1 includes the following bug fixes, infrastructure, documentation and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.4.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.4.1.md).

## BUG FIXES

### OpenSearch ML Commons
* Wait for upload task to complete in security tests ([#551](https://github.com/opensearch-project/ml-commons/pull/551))
* Fix running task when reload loaded model on single node cluster ([#561](https://github.com/opensearch-project/ml-commons/pull/561))
* Change model state to UPLOADED when all chunks uploaded ([#573](https://github.com/opensearch-project/ml-commons/pull/573))
* Set model state as unloaded when call unload model API ([#580](https://github.com/opensearch-project/ml-commons/pull/580))


### OpenSearch Neural Search
* Change the behavior when embedding fields are not present ([#72](https://github.com/opensearch-project/neural-search/pull/72))


### OpenSearch Dashboards Reporting Plugin
* Upgrade loader-utils ([#542](https://github.com/opensearch-project/dashboards-reports/pull/542))
* Upgrade decode-uri-component and qs ([#567](https://github.com/opensearch-project/dashboards-reports/pull/567))


### OpenSearch SQL
* Integration tests fix for arm64 ([#1069](https://github.com/opensearch-project/sql/pull/1069))
* Upgrade jackson to 2.14.1 ([#1146](https://github.com/opensearch-project/sql/pull/1146))


### OpenSearch Security Analytics
* Fix for running windows integration tests ([#176](https://github.com/opensearch-project/security-analytics/pull/176))


### OpenSearch Observability
* QS upgraded to 6.5.3 ([#1334](https://github.com/opensearch-project/dashboards-observability/pull/1334))


## INFRASTRUCTURE

### OpenSearch Anomaly Detection
* Windows CI for AD ([#703](https://github.com/opensearch-project/anomaly-detection/pull/703))


### OpenSearch Anomaly Detection
* AD model performance benchmark ([#729](https://github.com/opensearch-project/anomaly-detection/pull/729))


## MAINTENANCE

### OpenSearch Security
* Username validation for special characters ([#2277](https://github.com/opensearch-project/security/pull/2277))
* Fixes CVE-2022-42920 by forcing bcel version to resovle to 6.6 ([#2303](https://github.com/opensearch-project/security/pull/2303))


### OpenSearch Anomaly Detection
* Increment version to 2.4.1-SNAPSHOT ([#733](https://github.com/opensearch-project/anomaly-detection/pull/733))


### OpenSearch ML Commons
* Increment version to 2.4.1-SNAPSHOT ([#560](https://github.com/opensearch-project/ml-commons/pull/560))
* Force protobuf-java version as 3.21.9 ([#588](https://github.com/opensearch-project/ml-commons/pull/588))
* Fix junit version ([#597](https://github.com/opensearch-project/ml-commons/pull/597))
* Update dependency junit:junit to v4.13.1 ([#629](https://github.com/opensearch-project/ml-commons/pull/629))


### OpenSearch Dashboards Reporting Plugin
* Bump verison to 2.4.1 ([#540](https://github.com/opensearch-project/dashboards-reports/pull/540))

### OpenSearch Observability
* Increment version to 2.4.1-SNAPSHOT ([#1278](https://github.com/opensearch-project/dashboards-observability/pull/1278))


### OpenSearch Alerting Dashboards Plugin
* Bumped version to 2.4.1. ([#409](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/409))
* Adjust OpenSearch-Dashboards version used by test workflows. ([#363](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/363))
* Fixed throttling settings for bucket level trigger actions. ([#328](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/328))


## DOCUMENTATION

### OpenSearch Alerting Dashboards Plugin
* Add 2.4.1 release notes ([#420](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/420))