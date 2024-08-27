# OpenSearch and OpenSearch Dashboards 1.3.19 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 1.3.19](https://opensearch.org/versions/opensearch-1-3-19.html) includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.19.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.19.md).


## BUG FIXES


### Opensearch Security Dashboards Plugin


* Update nextUrl validation to incorporate serverBasePath ([#2066](https://github.com/opensearch-project/security-dashboards-plugin/pull/2066))
* Fix a bug where basepath nextUrl is invalid when it should be valid ([#2098](https://github.com/opensearch-project/security-dashboards-plugin/pull/2098))


## INFRASTRUCTURE


### Opensearch Anomaly Detection


* Removed support for JDK8 ([#1279](https://github.com/opensearch-project/anomaly-detection/pull/1279))


## MAINTENANCE


### Opensearch Security


* Bump org.apache.cxf:cxf-rt-rs-security-jose from 3.5.8 to 3.5.9 ([#4579](https://github.com/opensearch-project/security/pull/4579))


