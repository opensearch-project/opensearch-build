# OpenSearch and OpenSearch Dashboards 1.3.5 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 1.3.5 includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.5.md).
## BUG FIXES

### Opensearch
* OpenSearch crashes on closed client connection before search reply when total ops higher compared to expected ([#4143](https://github.com/opensearch-project/OpenSearch/pull/4143))
* gradle check failing with java heap OutOfMemoryError ([#4150](https://github.com/opensearch-project/OpenSearch/pull/4150))

### Opensearch Security
* Triple audit logging fix ([#1996](https://github.com/opensearch-project/security/pull/1996))
* Cluster permissions evaluation logic will now include index_template type action ([#1885](https://github.com/opensearch-project/security/pull/1885))

### Opensearch Security Dashboards Plugin
* Get security_tenant search param from URL ([#1043](https://github.com/opensearch-project/security-dashboards-plugin/pull/1043))

### Opensearch Reporting Dashboards Plugin
* Fixed high severity security issue :  RCE vector in bundled Headless Chromium -[Issue](https://github.com/opensearch-project/dashboards-reports/security/advisories/GHSA-pm2x-4c64-x8g7) ([#424](https://github.com/opensearch-project/dashboards-reports/pull/424))

## INFRASTRUCTURE
### Opensearch Cross Cluster Replication
* Added build.sh compatible with 1.3.x release ([#483](https://github.com/opensearch-project/cross-cluster-replication/pull/483))
## MAINTENANCE
### Opensearch Security
* Upgrade jackson-databind from 2.13.2 to 2.13.2.2 to match core's version.properties and upgrade kafka dependencies ([#2000](https://github.com/opensearch-project/security/pull/2000))