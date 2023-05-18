# OpenSearch and OpenSearch Dashboards 1.3.10 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.10](https://opensearch.org/versions/opensearch-1-3-10.html) includes the following bug fixes, infrastructure, enhancements and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/1.3/release-notes/opensearch.release-notes-1.3.10.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.10.md).


## ENHANCEMENTS

### Opensearch Anomaly Detection Dashboards
* Dependency updates ([#463](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/463))

### OpenSearch Security 
* Add chmod 0600 to install_demo_configuration bash script ([#2550](https://github.com/opensearch-project/security/pull/2550))
* Forcing spring-expression version ([#2711](https://github.com/opensearch-project/security/pull/2711))
## BUG FIXES

### Opensearch Index Management
* Fix 1.3.10 build issues. ([#780](https://github.com/opensearch-project/index-management/pull/780))

### Opensearch Security
* Fix lost privileges during auto initializing of the index ([#2643](https://github.com/opensearch-project/security/pull/2643))
* Fix NPE and add additional graceful error handling ([#2705](https://github.com/opensearch-project/security/pull/2705))


## MAINTENANCE

### Opensearch Observability
* CVE-2022-1471 fix:  force snakeyaml to 2.0 ([#1513](https://github.com/opensearch-project/observability/pull/1513))

### Opensearch Security
* Update the version of `json-smart` to 2.4.10 and the version of `spring-core` to 5.3.26 ([#2629](https://github.com/opensearch-project/security/pull/2629))
* Update Certs for SSL ([#2684](https://github.com/opensearch-project/security/pull/2684))
