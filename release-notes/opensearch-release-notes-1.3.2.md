# OpenSearch and OpenSearch Dashboards 1.3.2 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 1.3.2 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.2.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/1.3/release-notes/opensearch-dashboards.release-notes-1.3.2.md).

## Bug fixes

### OpenSearch Anomaly Detection
* Restart bug fix [#496](https://github.com/opensearch-project/anomaly-detection/pull/496)
* Empty search results bug fix [#522](https://github.com/opensearch-project/anomaly-detection/pull/522)


### OpenSearch Security
* Updates dependency vulnerabilities versions in 1.3 ([#1807](https://github.com/opensearch-project/security/pull/1807))
* Fix 'openserach' typo in roles.yml (#1770) ([#1793](https://github.com/opensearch-project/security/pull/1793))
* Switch to log4j logger (#1751) [([#1791](https://github.com/opensearch-project/security/pull/1791))
* Fix data-stream name resolution for wild-cards ([#1725](https://github.com/opensearch-project/security/pull/1725))
* Revert "Fix data-stream name resolution for wild-cards" ([#1719](https://github.com/opensearch-project/security/pull/1719))
* Fix data-stream name resolution for wild-cards ([#1716](https://github.com/opensearch-project/security/pull/1716))


### OpenSearch Security Dashboards Plugin
* Fix 'openserach' typo in constants.tsx (#953) ([#959](https://github.com/opensearch-project/security-dashboards-plugin/pull/959))


## Maintenance

### OpenSearch Ml Commons
* Bump to 1.3.2 ([#270](https://github.com/opensearch-project/ml-commons/pull/270))


### OpenSearch Security
* Keep jackson-databind in alignment with OpenSearch ([#1817](https://github.com/opensearch-project/security/pull/1817))
* Add custom build script to ignore standalone admin ([#1811](https://github.com/opensearch-project/security/pull/1811))
* Incremented version to 1.3.2. ([#1733](https://github.com/opensearch-project/security/pull/1733))


### OpenSearch Security Dashboards Plugin
* Incremented version to 1.3.2. ([#978](https://github.com/opensearch-project/security-dashboards-plugin/pull/978))
* Remove redundant DCO check in favor of the GitHub app ([#972](https://github.com/opensearch-project/security-dashboards-plugin/pull/972))


## Enhancements

### OpenSearch Ml Commons
* Support dispatching execute task; don't dispatch ML task again ([#279](https://github.com/opensearch-project/ml-commons/pull/279))


## Infrastructure

### OpenSearch Anomaly Detection
* Removing job-scheduler zip for 1.3 branch [#475](https://github.com/opensearch-project/anomaly-detection/pull/475)
* Version bump to 1.3.2 [#485](https://github.com/opensearch-project/anomaly-detection/pull/485)
* Fixed to check if build is a snapshot [#531](https://github.com/opensearch-project/anomaly-detection/pull/531)
