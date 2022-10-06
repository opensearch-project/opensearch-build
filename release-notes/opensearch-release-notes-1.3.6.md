# OpenSearch and OpenSearch Dashboards 1.3.6 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 1.3.6 includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.6.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.6.md).

## BUG FIXES

### OpenSearch Alerting
* Update ktlint and force common-codec version ([#575](https://github.com/opensearch-project/alerting/pull/575))
* Upgrade kotlin to 1.16.10 ([#567](https://github.com/opensearch-project/alerting/pull/567))

### OpenSearch Anomaly Detection
* Update jackson dependency version ([#678](https://github.com/opensearch-project/anomaly-detection/pull/678))

### OpenSearch Common Utils
* Bump kotlin version ([#266](https://github.com/opensearch-project/common-utils/pull/266))
* Disable detekt ([#266](https://github.com/opensearch-project/common-utils/pull/266))

### OpenSearch Dashboards Reports
* Updated Kotlin to 1.6.0 and jsoup to 1.15.3 ([#472](https://github.com/opensearch-project/dashboards-reports/pull/472))
* Update jackson to 2.13.4 ([#479](https://github.com/opensearch-project/dashboards-reports/pull/479))

### OpenSearch Index Management
* Re-enabled detekt and fixed issues; Upgraded snakeyml version 1.32 and Kotlin version to 1.6.10 to fix CVE issues; Upgraded Jackson version align with upstream ([#535](https://github.com/opensearch-project/index-management/pull/535))

### OpenSearch Ml Commons
* Fix jackson databind version: use same version as OpenSearch core ([#381](https://github.com/opensearch-project/ml-commons/pull/381))

### OpenSearch Observability
* Updated Kotlin to 1.6.0 ([#1052](https://github.com/opensearch-project/observability/pull/1052))
* Update Jackson to 2.13.4 ([#1066](https://github.com/opensearch-project/observability/pull/1066))

### Opensearch Security
* Scope updateVersion to only build.gradle ([#2121](https://github.com/opensearch-project/security/pull/2121))

### Opensearch Security Dashboards Plugin
* Fix for Tenancy info getting lost on re-login in SAML Authentication flow ([#1125](https://github.com/opensearch-project/security-dashboards-plugin/pull/1125))
* Fixed the tenant switching after timeout ([#1090](https://github.com/opensearch-project/security-dashboards-plugin/pull/1090))
* Select tenant popup only appears when mutli-tenacy is enabled ([#965](https://github.com/opensearch-project/security-dashboards-plugin/pull/965))

## DOCUMENTATION

### OpenSearch Index Management
* Added 1.3.6 release note ([#536](https://github.com/opensearch-project/index-management/pull/536))

## MAINTENANCE

### OpenSearch Cross Cluster Replication
* Upgrade Snakeyml version to 1.32 and Jackson version to 2.13.4 ([#573](https://github.com/opensearch-project/cross-cluster-replication/pull/573))

### OpenSearch Dashboards Reports
* Bump version to 1.3.6 ([#473](https://github.com/opensearch-project/dashboards-reports/pull/473))

### OpenSearch Ml Commons
* Increment version to 1.3.6 and remove jackson force version ([#454](https://github.com/opensearch-project/ml-commons/pull/454))

### OpenSearch Observability
* Bump version to 1.3.6 ([#1059](https://github.com/opensearch-project/observability/pull/1059))

### Opensearch Security
* Update jackson version to 2.13.4 ([#2128](https://github.com/opensearch-project/security/pull/2128))
* Update Kafka Client to 3.0.2 ([#2129](https://github.com/opensearch-project/security/pull/2129))
* Staging for version increment automation  ([#2029](https://github.com/opensearch-project/security/pull/2029))
