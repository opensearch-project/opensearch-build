# OpenSearch and OpenSearch Dashboards 2.4.1 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.4.1 includes the following enhancements, bug fixes, infrastructure, and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.4.1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.4.1.md).


## ENHANCEMENTS

### Opensearch Anomaly Detection
* AD model performance benchmark ([#729](https://github.com/opensearch-project/anomaly-detection/pull/729))


## BUG FIXES

### Opensearch Ml Commons
* Wait for upload task to complete in security tests ([#551](https://github.com/opensearch-project/ml-commons/pull/551))
* Fix running task when reload loaded model on single node cluster ([#561](https://github.com/opensearch-project/ml-commons/pull/561))
* Change model state to UPLOADED when all chunks uploaded ([#573](https://github.com/opensearch-project/ml-commons/pull/573))
* Set model state as unloaded when call unload model API ([#580](https://github.com/opensearch-project/ml-commons/pull/580))


### OpenSearch Neural Search
* Change the behavior when embedding fields are not present ([#72](https://github.com/opensearch-project/neural-search/pull/72))


### Opensearch Dashboards Reporting Plugin
* Fixed high severity security issue :  RCE vector in bundled Headless Chromium -[Issue](https://github.com/opensearch-project/dashboards-reports/security/advisories/GHSA-pm2x-4c64-x8g7) ([#431](https://github.com/opensearch-project/dashboards-reports/pull/431))


### OpenSearch SQL
* Integration tests fix for arm64 ([#1069](https://github.com/opensearch-project/sql/pull/1069))
* Upgrade jackson to 2.14.1 ([#1146](https://github.com/opensearch-project/sql/pull/1146))


## INFRASTRUCTURE

### Opensearch Anomaly Detection
* Windows CI for AD ([#703](https://github.com/opensearch-project/anomaly-detection/pull/703))


## MAINTENANCE

### Opensearch Security
* Username validation for special characters ([#2277](https://github.com/opensearch-project/security/pull/2277))
* Fixes CVE-2022-42920 by forcing bcel version to resovle to 6.6 ([#2303](https://github.com/opensearch-project/security/pull/2303))


### Opensearch Anomaly Detection
* Increment version to 2.4.1-SNAPSHOT ([#733](https://github.com/opensearch-project/anomaly-detection/pull/733))


### Opensearch Ml Commons
* Increment version to 2.4.1-SNAPSHOT ([#560](https://github.com/opensearch-project/ml-commons/pull/560))
* force protobuf-java version as 3.21.9 ([#588](https://github.com/opensearch-project/ml-commons/pull/588))
* fix junit version ([#597](https://github.com/opensearch-project/ml-commons/pull/597))
* Update dependency junit:junit to v4.13.1 ([#629](https://github.com/opensearch-project/ml-commons/pull/629))

