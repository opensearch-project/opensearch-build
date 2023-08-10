# OpenSearch and OpenSearch Dashboards 1.3.12 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.12](https://opensearch.org/versions/opensearch-1-3-12.html) includes the following bug fixes, infrastructure, enhancements and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.12.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.12.md).

## BUG FIXES

### OpenSearch Dashboards Observability
* CVE fixes for tough-cookie, sem-ver, word-wrap ([#776](https://github.com/opensearch-project/dashboards-observability/pull/776))

### OpenSearch Dashboards Query Workbench
* Bump dependencies for tough-cookie, semver, word-wrap ([#101](https://github.com/opensearch-project/dashboards-query-workbench/pull/101))

### OpenSearch Dashboards Reporting
* Bump dependencies to fix cve ([#155](https://github.com/opensearch-project/dashboards-reporting/pull/155))

### Opensearch Dashboards Security 
* Switch to new tenant after loading a copied long URL ([#1450](https://github.com/opensearch-project/security-dashboards-plugin/pull/1450))
* Add the tenant into the short URL once the short URL is resolved ([#1462](https://github.com/opensearch-project/security-dashboards-plugin/pull/1462)) [#1516](https://github.com/opensearch-project/security-dashboards-plugin/pull/1516)

### OpenSearch Dashboards Visualizations
* Fix CVEs Tough Cookie, Semver, word-wrap ([#219](https://github.com/opensearch-project/dashboards-visualizations/pull/219))

### OpenSearch Observability
* Bump guava version for cve ([#1559](https://github.com/opensearch-project/observability/pull/1559))

## MAINTENANCE

### OpenSearch Dashboards Observability
* Remove unused files ([#650](https://github.com/opensearch-project/dashboards-observability/pull/650))
* Update tests and snapshots ([#612](https://github.com/opensearch-project/dashboards-observability/pull/612))

### Opensearch Security
* Bump BouncyCastle from jdk15on to jdk15to18 ([#2901](https://github.com/opensearch-project/security/pull/2901)) ([#2931](https://github.com/opensearch-project/security/pull/2931))
* Update guava to address CVE-2023-2976 ([#3060](https://github.com/opensearch-project/security/pull/3060))
* Bump the version of kafka and spring-kafka-test (CVE Related) ([#3087](https://github.com/opensearch-project/security/pull/3087))
